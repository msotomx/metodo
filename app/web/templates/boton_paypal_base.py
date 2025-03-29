# 1) INSTALAR DJANGO-PAYPAL

pip install django-paypal


# 2) CONFIGURAR DJANGO PARA IPN en el archivo settings.py 

INSTALLED_APPS = [
    ...
    'paypal.standard.ipn',
]

PAYPAL_RECEIVER_EMAIL = "tu-email@paypal.com"
PAYPAL_TEST = True  # Cambia a False en producción


# 3) EN EL ARCHIVO urls.py agregar el path de paypal 

from django.urls import path, include

urlpatterns = [
    path('paypal/', include('paypal.standard.ipn.urls')),
]

# 4) CREAR UNA VISTA PARA GUARDAR LOS DATOS
#    Django-PayPal enviará notificaciones IPN cuando una transacción sea completada. 
 
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.models import PayPalIPN
from django.http import HttpResponse
from .models import Cliente

@csrf_exempt
def paypal_ipn_receiver(request):
    if request.method == "POST":
        ipn_obj = PayPalIPN.objects.create(**request.POST.dict())

        if ipn_obj.payment_status == "Completed":
            Cliente.objects.create(
                nombre=ipn_obj.first_name + " " + ipn_obj.last_name,
                email=ipn_obj.payer_email,
                ciudad=ipn_obj.address_city,
                transaction_id=ipn_obj.txn_id,
                monto=ipn_obj.mc_gross,
            )
            return HttpResponse("OK")
    return HttpResponse("FAIL")

# 5) Configurar PayPal IPN
#    En la configuración de tu cuenta de PayPal, 
#    activa IPN Notifications y coloca la URL de tu vista de Django.

https://tu-dominio.com/paypal-ipn/

# 6) Agregar el Formulario de Pago en HTML
#    En tu plantilla de HTML, agrega el formulario de PayPal:

<form action="https://www.paypal.com/cgi-bin/webscr" method="post">
    <input type="hidden" name="cmd" value="_xclick">
    <input type="hidden" name="business" value="tu-email@paypal.com">
    <input type="hidden" name="item_name" value="Producto o servicio">
    <input type="hidden" name="amount" value="10.00">
    <input type="hidden" name="currency_code" value="USD">
    <input type="hidden" name="return" value="https://tu-dominio.com/gracias">
    <input type="hidden" name="notify_url" value="https://tu-dominio.com/paypal-ipn/">
    <input type="submit" value="Pagar con PayPal">
</form>

🏆 Con esto:
✔️ PayPal enviará los datos del pago a notify_url.
✔️ Django guardará los datos en la base de datos.
✔️ Tu aplicación registrará cada compra realizada.