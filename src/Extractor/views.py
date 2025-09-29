import os
import requests
from django.shortcuts import redirect, render
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.core.files.storage import FileSystemStorage 
from pdf2image import convert_from_path 

def index(request):
    if request.user.is_authenticated:
        return redirect('Extractor:extractor_view')
    return render(request, 'Extractor/index.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('Extractor:extractor_view')

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('Extractor:extractor_view')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    else:
        form = AuthenticationForm()

    return render(request, 'Extractor/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('Extractor:index')

@login_required(login_url='Extractor:login_view')
def extractor_view(request):
    if request.method == "POST" and request.FILES.get("pdf_file"):
        pdf_file = request.FILES["pdf_file"]

        # Guardar el PDF en media/
        fs = FileSystemStorage()
        filename = fs.save(pdf_file.name, pdf_file)
        uploaded_pdf_path = fs.path(filename)

        # Preparar directorio para las imágenes
        output_dir = os.path.join(settings.MEDIA_ROOT, "temp_images")
        os.makedirs(output_dir, exist_ok=True)

        # Convertir PDF a imágenes
        images = convert_from_path(uploaded_pdf_path)
        image_urls = []
        file_payload = {}

        for i, img in enumerate(images):
            image_filename = f"page_{i+1}.png"
            image_path = os.path.join(output_dir, image_filename)
            img.save(image_path, "PNG")
            image_urls.append(settings.MEDIA_URL + "temp_images/" + image_filename)

            # Agregá el archivo para enviar a n8n
            file_payload[f"file_{i+1}"] = open(image_path, "rb")

        # Hacer el POST al webhook de n8n con todas las imágenes
        webhook_url = "https://javi9420.app.n8n.cloud/webhook-test/a36ce4cf-c90e-477a-942a-b34615f97965"
        try:
            response = requests.post(
                webhook_url,
                files=file_payload,
                data={
                    "pdf_name": pdf_file.name,
                    "total_pages": len(images),
                    "user": request.user.username,
                    "token": settings.N8N_TOKEN,
                },
                timeout=30,
            )
            # Podés chequear status, loguear fallas, etc.
            print("Webhook response:", response.status_code, response.text)
        except Exception as e:
            print("Error al enviar webhook a n8n:", e)
        finally:
            # Cerrá los archivos abiertos
            for f in file_payload.values():
                f.close()

        # Renderizar galería para el usuario (UI)
        return render(request, "Extractor/galeria.html", {"images": image_urls})

    return render(request, "Extractor/extractor_view.html")

@login_required(login_url='Extractor:login_view')
def galeria_view(request):
    return render(request, 'Extractor/galeria.html')