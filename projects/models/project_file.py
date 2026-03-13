from django.db import models


class ProjectFile(models.Model):
    name = models.CharField(unique=True, max_length=120)
    file = models.FileField(upload_to='projects/')
    created_at = models.DateField(
        auto_now_add=True
    )