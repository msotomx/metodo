from django.contrib import admin

# Register your models here.
from .models import Categoria, Proveedor, Producto

admin.site.register(Categoria)
admin.site.register(Proveedor)
#admin.site.register(Producto)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre','precio','categoria')
    list_editable = ('precio','categoria')