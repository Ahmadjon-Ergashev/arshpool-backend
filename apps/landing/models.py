from django.db import models
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator

# Create your models here.


class Project(models.Model):
    name_uz = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)
    description_uz = models.TextField()
    description_ru = models.TextField()
    slug = models.SlugField(max_length=255)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name_uz

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name_uz)
        return super().save(*args, **kwargs)


def project_image_path(instance, filename):
    return f"project/{instance.project.slug}/{filename}"


class ProjectImage(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="images"
    )
    source = models.FileField(
        upload_to=project_image_path,
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png", "gif", "webp", "heic", "mp4", "mov"]
            )
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Image - {self.pk}"
