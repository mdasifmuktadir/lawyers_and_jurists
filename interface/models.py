from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from tinymce.models import HTMLField

# Create your models here.
class FeedBack(models.Model):
    id = models.AutoField(primary_key=True)
    client_description = models.CharField(max_length=1000, default="text client who does testing")
    message = models.TextField()
    
class MembersOf(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=1000)
    image = models.ImageField(upload_to="members_of_images/")
    url = models.URLField(blank=True)


class Videos(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=1000)
    video_url = models.URLField()
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Video"
        verbose_name_plural = "Videos"


class Clients(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1000)
    logo = models.ImageField(upload_to="client_logos/")
    website = models.URLField(blank=True)

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"


class SocialMedia(models.Model):
    id = models.AutoField(primary_key=True)
    platform = models.CharField(max_length=100)
    url = models.URLField()
    icon = models.ImageField(
        upload_to="social_media_icons/", blank=True, null=True
    )

    class Meta:
        verbose_name = "Social Media"
        verbose_name_plural = "Social Media"


class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1000)
    email = models.EmailField()
    telephones = models.TextField()
    cell = models.TextField()
    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"
class Carousel(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=1000, blank=True)
    image = models.ImageField(upload_to="carousel_images/")
    description = models.TextField(blank=True)
    class Meta:
        verbose_name = "Carousel"
        verbose_name_plural = "Carousels"
    
class Gallery(models.Model):
    class CategoryChoices(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        CHAMBER = 'CHAMBER', 'Chamber'
        CONFERENCE = 'CONFERENCE', 'Conference & Seminars'
        LNJ_TEAM = 'LNJ_TEAM', 'LNJ Team'
        OTHERS = 'OTHERS', 'Others'

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=1000, blank=True)
    category = models.CharField(
        max_length=50,
        choices=CategoryChoices.choices,
        default=CategoryChoices.OTHERS,
    )
    image = models.ImageField(upload_to="gallery_images/")
    description = models.TextField(blank=True)


    class Meta:
        verbose_name = "Gallery"
        verbose_name_plural = "Galleries"

    def __str__(self):
        return f"{self.title or 'Image'} ({self.get_category_display()})"