from django.contrib import admin

# Register your models here.
from .models import Categoria, Proveedor, Producto, Giro, Cliente, ComunicaCliente, Pedido, PedidoDetalle

admin.site.register(Categoria)
admin.site.register(Proveedor)
#admin.site.register(Producto)
admin.site.register(Giro)
admin.site.register(Cliente)
admin.site.register(ComunicaCliente)
admin.site.register(Pedido)
admin.site.register(PedidoDetalle)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre','precio','categoria')
    list_editable = ('precio','categoria')