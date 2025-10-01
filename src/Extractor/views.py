import os
import json
import uuid
from django.shortcuts import redirect, render
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse, HttpResponseForbidden
from django.utils import timezone
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
    """
    View que procesa el PDF, guarda las imágenes en MEDIA_ROOT/temp_images
    y registra (append) un objeto JSON en temp_images/processed_items.json
    con metadata e image_urls. NO intenta enviar nada por HTTP a n8n.
    """
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

        for i, img in enumerate(images):
            image_filename = f"page_{i+1}.png"
            image_path = os.path.join(output_dir, image_filename)
            img.save(image_path, "PNG")

            # URL absoluta (ej: https://tu-dominio/media/temp_images/page_1.png)
            image_url = request.build_absolute_uri(
                settings.MEDIA_URL + "temp_images/" + image_filename
            )
            image_urls.append(image_url)

        # Crear metadata del item procesado
        metadata_item = {
            "id": str(uuid.uuid4()),
            "pdf_name": pdf_file.name,
            "total_pages": len(images),
            "user": request.user.username,
            "image_urls": image_urls,
            "created_at": timezone.now().isoformat(),
        }

        # Guardar/append en processed_items.json
        processed_file = os.path.join(output_dir, "processed_items.json")
        try:
            if os.path.exists(processed_file):
                with open(processed_file, "r", encoding="utf-8") as f:
                    items = json.load(f)
            else:
                items = []
        except Exception:
            items = []

        # Insertar primero (último procesado al principio)
        items.insert(0, metadata_item)
        with open(processed_file, "w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=2)

        # Mostrar galería como antes
        return render(request, "Extractor/galeria.html", {"images": image_urls})

    return render(request, "Extractor/extractor_view.html")


def processed_list(request):
    """
    Endpoint que devuelve JSON con los items procesados.
    Se accede con: GET /api/processed/?api_key=MI_CLAVE
    """
    # Validar API key
    provided_key = request.GET.get("api_key")
    expected_key = getattr(settings, "N8N_PULL_API_KEY", None)

    if not expected_key or provided_key != expected_key:
        return HttpResponseForbidden("Invalid API key")

    processed_file = os.path.join(settings.MEDIA_ROOT, "temp_images", "processed_items.json")
    if not os.path.exists(processed_file):
        return JsonResponse({"items": []})

    try:
        with open(processed_file, "r", encoding="utf-8") as f:
            items = json.load(f)
    except Exception:
        items = []

    # Permitir limitar resultados (opcional)
    limit = request.GET.get("limit")
    if limit:
        try:
            limit = int(limit)
            items = items[:limit]
        except Exception:
            pass

    return JsonResponse({"items": items})

@login_required(login_url='Extractor:login_view')
def galeria_view(request):
    return render(request, 'Extractor/galeria.html')