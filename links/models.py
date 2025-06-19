from django.db import models
from django.conf import settings

class Link(models.Model):
    url = models.URLField()
    nombre = models.TextField(blank=True)
    creador = models.TextField(blank=True)
    plataforma = models.TextField(blank=True)
    genero = models.TextField(blank=True)
    fecha_lanzamiento = models.PositiveIntegerField(blank=True, null=True)  
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)

class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    link = models.ForeignKey('links.Link', related_name='votes', on_delete=models.CASCADE)


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    link = models.ForeignKey('links.Link', related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

