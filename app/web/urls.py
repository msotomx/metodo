from django.urls import path
from . import views

app_name = 'web'

urlpatterns = [
    path('', views.index,name='index'),
    path('entorno1',views.entorno1,name='entorno1'),
    path('entorno2',views.entorno2,name='entorno2'),
    path('entorno3',views.entorno3,name='entorno3'),
    path('entorno4',views.entorno4,name='entorno4'),
    # path('checkout',views.checkout,name='checkout'),
    path('productosPorCategoria/<int:categoria_id>',views.productosPorCategoria,name='productosPorCategoria'),
    path('productosPorNombre',views.productosPorNombre,name='productosPorNombre'),
    path('producto/<int:producto_id>',views.productoDetalle,name='producto'),
    path('carrito',views.carrito,name='carrito'),
    path('agregarCarrito/<int:producto_id>',views.agregarCarrito,name='agregarCarrito'),
    path('limpiarCarrito',views.limpiarCarrito,name='limpiarCarrito'),
    path('registrarPedido',views.registrarPedido,name='registrarPedido'),
    path('eliminarProductoCarrito/<int:producto_id>',views.eliminarProductoCarrito,name='eliminarProductoCarrito'),
    path('crearUsuario',views.crearUsuario,name='crearUsuario'),
    path('loginUsuario',views.loginUsuario,name='loginUsuario'),
    path('cuenta',views.cuentaUsuario,name='cuentaUsuario'),
    path('actualizarCliente',views.actualizarCliente,name='actualizarCliente'),
    path('login',views.loginUsuario,name='loginUsuario'),
    path('logout',views.logoutUsuario,name='logoutUsuario'),
    path('registrarPedido',views.registrarPedido,name='registrarPedido'),
    path('compra',views.compra,name='compra'),
    path('confirmarPedido',views.confirmarPedido,name='confirmarPedido'),
    path('dw',views.dw,name='dw'),
    path('gracias',views.gracias,name='gracias'),
    path('checkout', views.pagar_con_paypal, name='checkout'),
    path('paypal/success/<int:cliente_id>/', views.paypal_success, name='paypal_success'),
    path('paypal/cancel/<int:cliente_id>/', views.paypal_cancel, name='paypal_cancel'),
]
