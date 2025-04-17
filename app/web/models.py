from django.db import models

# Create your models here.

class Categoria(models.Model):
    nombre = models.CharField(max_length=200)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class Giro(models.Model):
    nombre = models.CharField(max_length=200)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.TextField(null=True)
    contacto = models.CharField(max_length=100)
    telefono1 = models.CharField(max_length=13)
    telefono2 = models.CharField(max_length=13)
    email = models.EmailField(null=True)
    plazo_credito = models.SmallIntegerField(default=0)
    comentarios = models.TextField(null=True)
    
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    categoria = models.ForeignKey(Categoria,on_delete=models.RESTRICT)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(null=True)
    precio = models.DecimalField(max_digits=9,decimal_places=2)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to='productos',blank=True)
    proveedor = models.ForeignKey(Proveedor,on_delete=models.RESTRICT)
    sku = models.CharField(max_length=12, default='')

    def __str__(self):
        return self.nombre

from django.contrib.auth.models import User

class Cliente(models.Model):
    nombre = models.CharField(max_length=60, null=True)
    fecha_compra = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(null=True)
    telefono = models.CharField(max_length=13)
    ciudad = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=1)
    descargas = models.IntegerField(default=0)  # Nuevo campo para contar las descargas
    
    def __str__(self):
        return self.nombre

class ComunicaCliente(models.Model):
    cliente = models.ForeignKey(Cliente,on_delete=models.RESTRICT)
    fecha_contacto = models.DateTimeField(auto_now_add=True)
    comunicacion = models.TextField(null=True)

    def __str__(self):
        return self.usuario.username

class Pedido(models.Model):
    
    ESTADO_CHOICES = (
        ('0','Solicitado'),
        ('1','Pagado')
    )

    cliente = models.ForeignKey(Cliente,on_delete=models.RESTRICT)   # ForeingKey - relacion de muchos a uno
    fecha_registro = models.DateTimeField(auto_now_add=True)
    numero_pedido = models.CharField(max_length=20,null=True)
    monto_total = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    estado = models.CharField(max_length=1,default='0',choices=ESTADO_CHOICES)   # CON Esto, solo permite 0 o 1

    def __str__(self):
        return self.numero_pedido

class PedidoDetalle(models.Model):
    pedido = models.ForeignKey(Pedido,on_delete=models.RESTRICT)
    producto = models.ForeignKey(Producto,on_delete=models.RESTRICT)
    cantidad = models.IntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return self.producto.nombre
