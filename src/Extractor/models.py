from django.db import models

class ProductoExtraido(models.Model):
    id_producto = models.CharField(max_length=50)
    descripcion = models.TextField()
    talle = models.CharField(max_length=50, null=True, blank=True)
    color = models.CharField(max_length=50, default='VARIOS')
    unidades_vendidas = models.IntegerField(default=0)
    stock_general = models.IntegerField(default=0)
    deposito1 = models.IntegerField(default=0)
    deposito2 = models.IntegerField(default=0)
    fecha_carga = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "productos_extraidos"

    def __str__(self):
        return f"{self.id_producto} - {self.descripcion}"