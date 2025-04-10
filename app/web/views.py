import os
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import Categoria, Producto, Cliente, Pedido, PedidoDetalle

from django.conf import settings
from django import template
from .forms import ClienteForm

from django.http import HttpResponse, FileResponse
from django.http import HttpResponseForbidden

from django.core.exceptions import PermissionDenied

register = template.Library()


# Create your views here.
""" VISTAS PARA EL CATALOGO DE PRODUCTOS """

def index(request):
    listaProductos = Producto.objects.all()
    listaCategorias = Categoria.objects.all()

    context = {
        'productos':listaProductos,
        'categorias':listaCategorias
    }
    return render(request,'index.html',context)

def productosPorCategoria(request,categoria_id):
    """ Vista para filtrar productos por categoria """
    objCategoria = Categoria.objects.get(pk=categoria_id)
    listaProductos = objCategoria.producto_set.all()

    listaCategorias = Categoria.objects.all()

    context = {
        'categorias':listaCategorias,
        'productos':listaProductos
    }

    return render(request,'index.html',context)

def productosPorNombre(request):
    """ Vista para filtrado de productos por nombre """
    nombre = request.POST['nombre']

    listaProductos = Producto.objects.filter(nombre__contains=nombre)
    listaCategorias = Categoria.objects.all()

    context = {
        'categorias':listaCategorias,
        'productos':listaProductos
    }

    return render(request,'index.html',context)

def productoDetalle(request,producto_id):
    """ Vista para el detalle de producto """
    
    #objProducto = Producto.objects.get(pk=producto_id)
    objProducto = get_object_or_404(Producto,pk=producto_id)
    context = {
        'producto':objProducto
    }

    return render(request,'producto.html',context)

""" VISTAS PARA EL CARRITO DE COMPRAS """

from .carrito import Cart

def carrito(request):
    return render(request,'carrito.html')

def agregarCarrito(request,producto_id):
    if request.method == 'POST':
        cantidad = int(request.POST['cantidad'])
    else:
        cantidad = 1
    
    objProducto = Producto.objects.get(pk=producto_id)
    carritoProducto = Cart(request)
    carritoProducto.add(objProducto,cantidad)

    #print(request.session.get("cart"))

    if request.method == 'GET':
        return redirect('/')

    return render(request,'carrito.html')

def limpiarCarrito(request):
    carritoProducto = Cart(request)
    carritoProducto.clear()

    return render(request,'carrito.html')

def eliminarProductoCarrito(request,producto_id):
    objProducto = Producto.objects.get(pk=producto_id)
    carritoProducto = Cart(request)
    carritoProducto.delete(objProducto)

    return render(request,'carrito.html')

""" VISTAS PARA CLIENTES Y USUARIOS """

from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required  # funcion para agregar propiedades a las funciones

from .forms import ClienteForm

def crearUsuario(request):

    if request.method == 'POST':
        dataUsuario = request.POST['nuevoUsuario']
        dataPassword = request.POST['nuevoPassword']

        nuevoUsuario = User.objects.create_user(username=dataUsuario,password=dataPassword)
        if nuevoUsuario is not None:  # si no es vacio, si tiene un valor
            login(request,nuevoUsuario)
            return redirect('/cuenta')

# <!-- {% load crispy_forms_tags %}  -->   linea 2 de cuenta.html

    return render(request,'login.html')

def cuentaUsuario(request):

    try:

        clienteEditar = Cliente.objects.get(usuario = request.user)
        
        dataCliente = {
            'nombre':request.user.first_name,
            'apellidos':request.user.last_name,
            'email':request.user.email,
            'rfc':clienteEditar.rfc,
            'sexo':clienteEditar.sexo,
            'telefono':clienteEditar.telefono,
            'fecha_nacimiento':clienteEditar.fecha_nacimiento,
            'direccion':clienteEditar.direccion,
            'codigo_postal':clienteEditar.codigo_postal,
            'ciudad':clienteEditar.ciudad,
            'direccion_entrega':clienteEditar.direccion_entrega,
            'codigo_postal_entrega':clienteEditar.codigo_postal_entrega,
            'ciudad_entrega':clienteEditar.ciudad_entrega,
            'campo_libre':clienteEditar.campo_libre,
            'comentarios':clienteEditar.comentarios
        }
    except:
        dataCliente = {
            'nombre':request.user.first_name,
            'apellidos':request.user.last_name,
            'email':request.user.email
        }

    frmCliente = ClienteForm(dataCliente)
    context = {
        'frmCliente':frmCliente
    }

    return render(request,'cuenta.html',context)

def actualizarCliente(request):
    mensaje = ""
    if request.method == 'POST':
        frmCliente = ClienteForm(request.POST)
        if frmCliente.is_valid():
            dataCliente = frmCliente.cleaned_data
            
            # actualizar tabla de usuario
            actUsuario = User.objects.get(pk=request.user.id)
            actUsuario.first_name = dataCliente["nombre"]
            actUsuario.last_name = dataCliente["apellidos"]
            actUsuario.email = dataCliente["email"]
            actUsuario.save()
            
            #registrar al Cliente - tabla Cliente
            nuevoCliente = Cliente()
            nuevoCliente.usuario = actUsuario
            nuevoCliente.rfc = dataCliente["rfc"]
            nuevoCliente.direccion = dataCliente["direccion"]
            nuevoCliente.telefono = dataCliente["telefono"]
            nuevoCliente.sexo = dataCliente["sexo"]
            nuevoCliente.fecha_nacimiento = dataCliente["fecha_nacimiento"]
            nuevoCliente.codigo_postal = dataCliente["codigo_postal"]
            nuevoCliente.ciudad = dataCliente["ciudad"]
            nuevoCliente.direccion_entrega = dataCliente["direccion_entrega"]
            nuevoCliente.codigo_postal_entrega = dataCliente["codigo_postal_entrega"]
            nuevoCliente.ciudad_entrega = dataCliente["ciudad_entrega"]
            nuevoCliente.campo_libre = dataCliente["campo_libre"]
            nuevoCliente.comentarios = dataCliente["comentarios"]
            nuevoCliente.save()

            mensaje = "Datos Actualizados"

    context = {
         'mensaje':mensaje,
         'frmCliente':frmCliente
    }

    return render(request,'cuenta.html',context)


def loginUsuario(request):
    paginaDestino = request.GET.get('next',None)
    
    context = {
        'destino':paginaDestino
    }

    if request.method == 'POST':
        dataUsuario = request.POST['usuario']
        dataPassword = request.POST['password']
        dataDestino = request.POST['destino']

        usuarioAuth = authenticate(request,username=dataUsuario,password=dataPassword)
        if usuarioAuth is not None:
            login(request,usuarioAuth)

            if dataDestino != 'None':
                return redirect(dataDestino)
        
            return redirect('/cuenta')
        else:
            context = {
                'mensajeError':'Datos Incorrectos'
            }

    return render(request,'login.html',context)

def logoutUsuario(request):
    logout(request)
    return render(request,'login.html')

""" VISTAS PARA EL PROCESO DE COMPRA """
@login_required(login_url='/login')
def registrarPedido(request):
    try:

        clienteEditar = Cliente.objects.get(usuario = request.user)
        
        dataCliente = {
            'nombre':request.user.first_name,
            'apellidos':request.user.last_name,
            'email':request.user.email,
            'direccion':clienteEditar.direccion,
            'telefono':clienteEditar.telefono,
            'rfc':clienteEditar.rfc,
            'sexo':clienteEditar.sexo,
            'fecha_nacimiento':clienteEditar.fecha_nacimiento,
            'codigo_postal' :clienteEditar.codigo_postal,
            'ciudad':clienteEditar.ciudad,
            'direccion_entrega':clienteEditar.direccion_entrega,
            'codigo_postal_entrega':clienteEditar.codigo_postal_entrega,
            'ciudad_entrega':clienteEditar.ciudad_entrega,
            'campo_libre':clienteEditar.campo_libre,
            'comentarios':clienteEditar.comentarios
        }
    except:
        dataCliente = {
            'nombre':request.user.first_name,
            'apellidos':request.user.last_name,
            'email':request.user.email
        }

    frmCliente = ClienteForm(dataCliente)
    context = {
        'frmCliente':frmCliente
    }

    return render(request,'pedido.html',context)

def compra(request):
    return render(request,'compra.html')

# Paypal de prueba
from paypal.standard.forms import PayPalPaymentsForm

def view_that_asks_for_money(request):

    # What you want the button to do.
    paypal_dict = {
        "business": "sb-nc043e38051110@business.example.com",  # modificar el correo
        "amount": "7.00",
        "item_name": "ebook Hijos Felices",
        "invoice": "100-HF",
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri('/'),
        "cancel_return": request.build_absolute_uri('/logout'),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "payment.html", context)

# confirmar pedido: registra el pedido y detalle de pedido en la base de datos
# manda el flujo al boton de pago de paypal

@login_required(login_url='/login')
def confirmarPedido(request):
    context = {}
    if request.method == 'POST':
        #actualizar usuario
        actUsuario = User.objects.get(pk=request.user.id)
        actUsuario.first_name = request.POST['nombre']
        actUsuario.last_name = request.POST['apellidos']
        actUsuario.save()
        #registramos o actualizamos Cliente
        try:
            clientePedido = Cliente.objects.get(usuario=request.user)
            clientePedido.telefono = request.POST['telefono']
            clientePedido.direccion = request.POST['direccion']
            clientePedido.save()
        except:   # si el cliente no existe
            clientePedido = Cliente()
            clientePedido.usuario = actUsuario
            clientePedido.direccion = request.POST['direccion']
            clientePedido.telefono = request.POST['telefono']
            clientePedido.save()

        # #registramos nuevo pedido
        numPedido = ''
        montoTotal = float(request.session.get('cartMontoTotal'))
        nuevoPedido = Pedido()
        nuevoPedido.cliente = clientePedido
        nuevoPedido.save()

        #registramos el detalle del pedido
        carritoPedido = request.session.get('cart')
        for key, value in carritoPedido.items():
            productoPedido = Producto.objects.get(pk=value['producto_id'])
            detalle = PedidoDetalle()
            detalle.pedido = nuevoPedido
            detalle.producto = productoPedido
            detalle.cantidad = int(value['cantidad'])
            detalle.subtotal = float(value['subtotal'])
            detalle.save()
        
        #actualizar el pedido
        numPedido = 'HF-'+nuevoPedido.fecha_registro.strftime('%Y')+str(nuevoPedido.id)
        nuevoPedido.numero_pedido = numPedido
        nuevoPedido.monto_total = montoTotal
        nuevoPedido.save()

        # registrar variable de sesion para el pedido
        request.session['pedidoId'] = nuevoPedido.id   # se crea la variable pedidoID en la session se usa en 'gracias'

        #Creamos boton de paypal
        paypal_dict = {
            "business": 'sb-nc043e38051110@business.example.com', # settings.PAYPAL_BUSINESS_EMAIL,  # modificar el correo
            "amount": montoTotal,
            "item_name": "eBook Hijos Felices"+numPedido,
            "invoice": numPedido,
            "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
            "return": request.build_absolute_uri('/gracias'),
            "cancel_return": request.build_absolute_uri('/')
        }

        # Create the instance.
        formPaypal = PayPalPaymentsForm(initial=paypal_dict)

        context = {
            'pedido':nuevoPedido,
            'formPaypal':formPaypal
        }

        #limpiamos carrito de compras
        carrito = Cart(request)
        carrito.clear

    return render(request,'compra.html',context)

from django.core.mail import send_mail   # para enviar el correo

@login_required(login_url='/login')
def gracias(request):
    paypalId = request.GET.get('PayerID',None)
    print("paypalId antes del IF: ",paypalId)
    context = {}
    if paypalId is not None:
        print("paypalId: ",paypalId)
        pedidoId = request.session.get('pedidoId')
        pedido = Pedido.objects.get(pk=pedidoId)
        pedido.estado = '1'
        pedido.save()

        send_mail(
            "Gracias por tu Compra",
            "Tu numero de pedido es " + pedido.numero_pedido,
            settings.ADMIN_USER_EMAIL,   # de donde se envia
            [request.user.email, 'msotomx@gmail.com'],  # correos a los que se envia, separados por comas
            fail_silently=False,
        )
        context = {
            'pedido':pedido
        }
    else:
        return redirect('/')

    return render(request,'gracias.html',context)

def confirmarPedido2(request):
    context = {}
    if request.method == 'POST':
        #actualizar usuario
        actUsuario = User.objects.get(pk=request.user.id)
        actUsuario.first_name = request.POST['nombre']
        actUsuario.last_name = request.POST['apellidos']
        actUsuario.save()
        #registramos o actualizamos Cliente
        try:
            clientePedido = Cliente.objects.get(usuario=request.user)
            clientePedido.telefono = request.POST['telefono']
            clientePedido.direccion = request.POST['direccion']
            clientePedido.save()
        except:   # si el cliente no existe
            clientePedido = Cliente()
            clientePedido.usuario = actUsuario
            clientePedido.direccion = request.POST['direccion']
            clientePedido.telefono = request.POST['telefono']
            clientePedido.save()

        # #registramos nuevo pedido
        numPedido = ''
        montoTotal = float(request.session.get('cartMontoTotal'))
        nuevoPedido = Pedido()
        nuevoPedido.cliente = clientePedido
        nuevoPedido.save()

        #registramos el detalle del pedido
        carritoPedido = request.session.get('cart')
        for key, value in carritoPedido.items():
            productoPedido = Producto.objects.get(pk=value['producto_id'])
            detalle = PedidoDetalle()
            detalle.pedido = nuevoPedido
            detalle.producto = productoPedido
            detalle.cantidad = int(value['cantidad'])
            detalle.subtotal = float(value['subtotal'])
            detalle.save()
        
        #actualizar el pedido
        numPedido = 'HF-'+nuevoPedido.fecha_registro.strftime('%Y')+str(nuevoPedido.id)
        nuevoPedido.numero_pedido = numPedido
        nuevoPedido.monto_total = montoTotal
        nuevoPedido.save()

        # registrar variable de sesion para el pedido
        request.session['pedidoId'] = nuevoPedido.id   # se crea la variable pedidoID en la session se usa en 'gracias'

        #Creamos boton de paypal
        paypal_dict = {
            "business": 'sb-nc043e38051110@business.example.com', # settings.PAYPAL_BUSINESS_EMAIL,  # modificar el correo
            "amount": montoTotal,
            "item_name": "eBook Hijos Felices"+numPedido,
            "invoice": numPedido,
            "currency_code":"USD",
            "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
            "return": request.build_absolute_uri('/gracias'),
            "cancel_return": request.build_absolute_uri('/')
        }

        # Create the instance.
        formPaypal = PayPalPaymentsForm(initial=paypal_dict)

        context = {
            'pedido':nuevoPedido,
            'formPaypal':formPaypal
        }

        #limpiamos carrito de compras
        carrito = Cart(request)
        carrito.clear

    return render(request, 'compra.html',context)

def entorno1(request):
    return render(request,'entorno1.html')

def entorno2(request):
    return render(request,'entorno2.html')

def entorno3(request):
    return render(request,'entorno3.html')

def entorno4(request):
    return render(request,'entorno4.html')

def checkout(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.status = '0'  # Estado inicial: no pagado
            cliente.save()
            print("ID del cliente guardado:", cliente.id)
            return redirect('web:pago_paypal', cliente_id=cliente.id) #  Redirige a la vista de pago

    else:
        form = ClienteForm()

    return render(request, 'checkout.html', {'form': form})

def pago_requerido(view_func):
    def _wrapped_view(request, *args, **kwargs):
        cliente_id = kwargs.get('cliente_id')
        cliente = get_object_or_404(Cliente, id=cliente_id)
        if cliente.status != '1':  # Si el cliente no ha pagado, redirige
            raise PermissionDenied  # O redirige a otra página (como checkout)
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# @pago_requerido
def dw(request, cliente_id):
    try:
        cliente = Cliente.objects.get(id=cliente_id)
    except Cliente.DoesNotExist:
        print(f"Cliente con id {cliente_id} no encontrado")
        return redirect('web:checkout')
    
    if cliente.status != '1':  # Si el cliente no pagó
        print(f"Cliente con id {cliente_id} no ha pagado")
        return redirect('web:checkout')  # O redirigir a una página de advertencia
    
    if cliente.descargas >= 1:  # Limita a 1 descarga
        return HttpResponseForbidden("Llegaste al numero maximo de descargas, si hay un error, puedes enviar un email a: hijosfelicesmx@gmail.com")  # Prohibir más descargas
    
    # Si es la primera descarga, incrementamos el contador
    cliente.descargas += 1
    cliente.save()

    return render(request, 'dw.html', {'cliente': cliente})

def grabar_datos(request):
    # crea registro de usuarios
    dataUsuario = 'user1'
    dataPassword = 'sotor'
    nuevoUsuario = User.objects.create_user(username=dataUsuario,password=dataPassword)
    nuevoUsuario.first_name = 'MIGUEL'
    nuevoUsuario.last_name = 'SOTO'
    nuevoUsuario.email = 'MIGUEL@gmail.com'
    nuevoUsuario.date_join = '2025/03/13'
    nuevoUsuario = User.objects.create_user(username=dataUsuario,password=dataPassword)
    nuevoUsuario.save()

    # crea registro de Clientes
    nuevoCliente = Cliente.objects.get(usuario = nuevoUsuario.user)
    
    if not Cliente.objects.filter(id=clienteEditar.usuario).exists():
        # el cliente no existe 

        nuevoCliente.nombre = nuevoUsuario.first_name
        nuevoCliente.apellidos = nuevoUsuario.last_name,
        nuevoCliente.email = nuevoUsuario.email,
        nuevoCliente.direccion = ''
        nuevoCliente.telefono = ''
        nuevoCliente.rfc = ''
        nuevoCliente.sexo = 'M'
        nuevoCliente.fecha_nacimiento = ''
        nuevoCliente.codigo_postal ='00000'
        nuevoCliente.ciudad = ''
        nuevoCliente.direccion_entrega = ''
        nuevoCliente.codigo_postal_entrega = ''
        nuevoCliente.ciudad_entrega = ''
        nuevoCliente.campo_libre = ''
        nuevoCliente.comentarios = ''
        nuevoCliente.save()

    # crea registro de pedido        
    nuevoPedido.cliente = nuevoCliente 
    
    numPedido = 'HF-'+nuevoPedido.fecha_registro.strftime('%Y')+str(nuevoPedido.id)
    nuevoPedido.numero_pedido = numPedido
    nuevoPedido.monto_total = montoTotal 
    nuevoPedido.estado = '0'
    nuevoPedido.save()
    
    return render(request)

# import paypalrestsdk
from .paypal import paypalrestsdk

# VISTA PARA INICIAR EL PAGO EN PAYPAL

#07/abril/2025

def pago_paypal(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    return render(request, 'pago_paypal.html', {
        'cliente': cliente,
        'PAYPAL_CLIENT_ID': settings.PAYPAL_CLIENT_ID
    })


# VISTAS DE EXITO Y CANCELACION
#07/abril/2025
def paypal_success(request, cliente_id):
    cliente = Cliente.objects.get(id=cliente_id)
    cliente.status = '1'  # Pagado
    cliente.save()
    return redirect('web:dw',cliente_id=cliente.id)  # Redirige a la página de descarga o gracias

def paypal_cancel(request, cliente_id):
    cliente = Cliente.objects.get(id=cliente_id)
    cliente.status = '0'  # No pagado / cancelado
    cliente.save()
    return redirect('web:checkout')

def descargar_pdf(request):
    # Define la ruta al archivo PDF
    file_path = os.path.join(settings.MEDIA_ROOT, 'Hijos_Seguros_Hijos_Felices.pdf')
    
    # Verifica si el archivo existe
    if os.path.exists(file_path):
        # Abre el archivo y lo lee en modo binario
        with open(file_path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="Hijos_Seguros_Hijos_Felices.pdf"'
            return response
    else:
        return HttpResponse("El archivo no existe", status=404)
    