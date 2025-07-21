from django.shortcuts import render
import os
import re
import pdfplumber
from django.http import FileResponse, HttpResponseNotAllowed

pdf_path = "Report.pdf"  # Reemplazá con el nombre del archivo que uses

def index (request):
    return render(request, 'Extractor/index.html')

def login_view(request):
    return render(request, 'Extractor/login.html')

RUTA_CSV = r"C:\Users\PC\Desktop\FEDE\PROYECTO PORTFOLIOS\PROYECTO EXTRACTOR\CSVS"

def parse_line(line):
    pattern = re.match(
        r"""^(?P<id>\S+)\s+
            (?P<desc>.+?Talle:\s*\S+)\s+
            (?P<local>-?\d+)\s+
            (?:-?\d+\s+){2}
            (?P<dep1>-?\d+)\s+
            (?P<dep2>-?\d+)\s+
            (?:-?\d+\s+){6}
            (?P<color>\S+)\s+
            (?P<general>-?\d+)$
        """,
        line,
        re.VERBOSE
    )
    if pattern:
        return ",".join([
            pattern["id"],
            pattern["desc"],
            pattern["color"],
            pattern["local"],
            pattern["general"],
            pattern["dep1"],
            pattern["dep2"]
        ])
    return None


def subir_pdf_view(request):
    if request.method == 'GET':
        return render(request, 'extractor_view.html')  

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

        return FileResponse(open(ruta_csv, 'rb'), as_attachment=True, filename=nombre_csv)

    
    return HttpResponseNotAllowed(['GET', 'POST'])


