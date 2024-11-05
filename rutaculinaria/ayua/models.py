from django.db import models
from django.contrib.auth.models import User

class Plato(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='platos/')

    def __str__(self):
        return self.nombre

class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En proceso'),
        ('aceptado', 'Aceptado'),
        ('rechazado', 'Rechazado'),
    ]

    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    platos = models.ManyToManyField(Plato)  # Relación de muchos a muchos si un pedido puede incluir varios platos
    total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    motivo_rechazo = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Pedido #{self.id} de {self.cliente.username} - Estado: {self.estado}"
