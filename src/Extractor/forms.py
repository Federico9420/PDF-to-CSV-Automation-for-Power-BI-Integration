from django import forms

class UploadPDFForm(forms.Form):
    pdf_file = forms.FileField(label='Seleccionar archivo PDF')