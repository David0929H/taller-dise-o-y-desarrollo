from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Pedido, Plato

def admin_required(login_url='login_admin'):
    return user_passes_test(lambda u: u.is_staff, login_url=login_url)

def mostrar_inicio(request):
    menu_items = Plato.objects.all() 
    
    return render(request, 'inicio.html', {'menu_items': menu_items})


def login_cliente(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and not user.is_staff:
            login(request, user)
            return redirect('perfil_cliente')
    return render(request, 'login_cliente.html')

def login_admin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('ordenes') 
    return render(request, 'login_admin.html')


def registro_cliente(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('perfil_cliente')
    else:
        form = UserCreationForm()
    return render(request, 'registro_cliente.html', {'form': form})

@login_required
def perfil_cliente(request):
    return render(request, 'perfil_cliente.html', {'user': request.user})


def carrito_view(request):
    carrito_items = request.session.get('carrito_items', [])
    subtotal = sum(item['precio'] * item['cantidad'] for item in carrito_items)
    impuestos = subtotal * 0.19
    total = subtotal + impuestos

    context = {
        'carrito_items': carrito_items,
        'subtotal': subtotal,
        'impuestos': impuestos,
        'total': total,
    }
    return render(request, 'carrito.html', context)

@login_required
def finalizar_pedido(request):
    carrito_items = request.session.get('carrito_items', [])
    if not carrito_items:
        return redirect('carrito')

 
    total = sum(item['precio'] * item['cantidad'] for item in carrito_items) * 1.18  # Incluye impuestos
    pedido = Pedido.objects.create(cliente=request.user, total=total, estado='pendiente')


    for item in carrito_items:
        plato = get_object_or_404(Plato, id=item['plato_id'])
        pedido.platos.add(plato)

    request.session['carrito_items'] = []
    return render(request, 'finalizar_pedido.html', {'pedido': pedido})


@admin_required()
def pantalla_admin(request):
    if request.method == "POST":
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        imagen = request.FILES.get('imagen')
        
        if nombre and descripcion and imagen:
            plato = Plato(nombre=nombre, descripcion=descripcion, imagen=imagen)
            plato.save()
            return redirect('ordenes') 
    return render(request, 'menu_admin.html')



def ordenes_admin(request):
    ordenes = Pedido.objects.all()  # NOOOOOO BORRRAR QUE LLORO
    platos = Plato.objects.all()    # NOOOOOO BORRRAR QUE LLORO

    context = {
        'ordenes': ordenes,
        'platos': platos,
    }
    return render(request, 'ordenes.html', context)


@admin_required()
def orden_actual(request):
    orden = Pedido.objects.filter(estado='en_proceso').first()
    context = {'orden': orden}
    return render(request, 'orden_actual.html', context)

@admin_required()
def todas_ordenes(request):
    ordenes = Pedido.objects.all()
    context = {'ordenes': ordenes}
    return render(request, 'ordenes.html', context)

@admin_required()
def rechazar_pedido(request, pedido_id):
    if request.method == 'POST':
        motivo = request.POST.get('motivo')
        pedido = get_object_or_404(Pedido, id=pedido_id)
        pedido.estado = 'rechazado'
        pedido.motivo_rechazo = motivo
        pedido.save()
        return redirect('ordenes')

@admin_required()
def aceptar_pedido(request, pedido_id):
    if request.method == 'POST':
        pedido = get_object_or_404(Pedido, id=pedido_id)
        pedido.estado = 'aceptado'
        pedido.save()
        return redirect('ordenes')
