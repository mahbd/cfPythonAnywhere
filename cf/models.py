from django.db import models


class Handle(models.Model):
    name = models.CharField(blank=True, null=True, max_length=200)
    handle = models.CharField(max_length=200, unique=True)
    batch = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-batch', '-name', 'handle']


class Problems(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True, unique=True)
    link = models.TextField(blank=True, null=True)
    solver = models.ManyToManyField(Handle, blank=True)
    num_sol = models.IntegerField(default=0)

    class Meta:
        ordering = ['-num_sol']
