import os
import re
import pdfplumber

from django.shortcuts import render, redirect
from django.http import FileResponse, HttpResponseNotAllowed
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

RUTA_CSV = r"C:\Users\PC\Desktop\FEDE\PROYECTO PORTFOLIOS\PROYECTO EXTRACTOR\CSVS"


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
            user = form.get_user()
            login(request, user)
            return redirect('Extractor:extractor_view')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    else:
        form = AuthenticationForm()

    return render(request, 'Extractor/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('Extractor:index')


def parse_line(line):
    try:
        if not re.search(r"Talle:\s*\S+", line):
            return None

        partes = line.split()

        # ID del producto
        id_producto = partes[0]

        # Índice del "Talle:"
        idx_talle = next(i for i, p in enumerate(partes) if "Talle:" in p or p == "Talle:")

        # Descripción completa con talle incluido
        descripcion = " ".join(partes[1:idx_talle + 2])

        # Color (última palabra alfabética o patrón conocido)
        color_match = re.findall(r"[A-ZÑÁÉÍÓÚÜ/-]{3,}$", line)
        color = color_match[0] if color_match else "VARIOS"

        # Todos los números enteros (stock general, depósitos, etc.)
        numeros = [int(n) for n in re.findall(r"-?\d+", line)]

        if len(numeros) < 4:
            return None

        stock_local = numeros[1]
        deposito1 = numeros[4] if len(numeros) > 4 else 0
        deposito2 = numeros[5] if len(numeros) > 5 else 0
        stock_general = numeros[-1]

        return ",".join([
            id_producto,
            descripcion,
            color,
            str(stock_local),
            str(stock_general),
            str(deposito1),
            str(deposito2)
        ])

    except Exception:
        return None


@login_required(login_url='Extractor:login_view')
def subir_pdf_view(request):
    if request.method == 'GET':
        return render(request, 'Extractor/extractor_view.html')

    if request.method == 'POST' and request.FILES.get('archivo_pdf'):
        archivo = request.FILES['archivo_pdf']

        resultados = []
        with pdfplumber.open(archivo) as pdf:
            for pagina in pdf.pages:
                texto = pagina.extract_text()
                if not texto:
                    continue
                for linea in texto.split("\n"):
                    fila = parse_line(linea)
                    if fila:
                        resultados.append(fila)

        os.makedirs(RUTA_CSV, exist_ok=True)
        nombre_csv = archivo.name.replace(".pdf", ".csv")
        ruta_csv = os.path.join(RUTA_CSV, nombre_csv)

        with open(ruta_csv, "w", encoding="utf-8") as f:
            f.write("id_producto,descripcion,color,stock_local,stock_general,deposito1,deposito2\n")
            for fila in resultados:
                f.write(fila + "\n")

        messages.success(request, f'Archivo generado correctamente en: {ruta_csv}')
        return render(request, 'Extractor/extractor_view.html')

    return HttpResponseNotAllowed(['GET', 'POST'])