from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Model(models.Model):
    id = models.AutoField(primary_key=True)
    nama_cabang = models.CharField(max_length=100, unique=True)
    deskripsi = models.TextField()
    sejarah = models.TextField()

    def __str__(self):
        return str(self.id) + " | "+self.nama_cabang