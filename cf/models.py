from django.db import models


class Handle(models.Model):
    name = models.CharField(blank=True, null=True, max_length=200)
    handle = models.CharField(blank=True, null=True, max_length=200)
    batch = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.handle


class Problems(models.Model):
    name = models.TextField(blank=True, null=True)
    link = models.TextField(blank=True, null=True)
    solver = models.ManyToManyField(Handle, blank=True)
    num_sol = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-num_sol']
