
from unfold.admin import ModelAdmin
from django.contrib import admin
from django.utils.html import format_html
from .models import (
   FeedBack,
   MembersOf,
   Videos,
    Clients,
    SocialMedia,
    Contact,
    Carousel,
    Gallery,
    
  
)





@admin.register(FeedBack)
class FeedBackAdmin(ModelAdmin):
    list_display = ("client_description", "short_message")
    search_fields = ("client_description", "message")
    readonly_fields = ("client_description", "message")  # Helps keep feedback read-only in admin

    @admin.display(description="Message")
    def short_message(self, obj):
        return obj.message[:50] + "..." if len(obj.message) > 50 else obj.message


@admin.register(Videos)
class VideosAdmin(ModelAdmin):
    list_display = ("title", "video_url")
    search_fields = ("title", "description")


@admin.register(Clients)
class ClientsAdmin(ModelAdmin):
    list_display = ("name", "website")
    search_fields = ("name",)
 
  


@admin.register(SocialMedia)
class SocialMediaAdmin(ModelAdmin):
    list_display = ("platform", "url")
    search_fields = ("platform",)


@admin.register(Contact)
class ContactAdmin(ModelAdmin):
    list_display = ("name", "email", "telephones", "cell")
    search_fields = ("name", "email", "telephones", "cell")
    
    
@admin.register(Carousel)
class CarouselAdmin(ModelAdmin):
    list_display = ("title", "image")
    search_fields = ("title",)
    
@admin.register(Gallery)
class GalleryAdmin(ModelAdmin):
    list_display = ("title", "category", "image")
    search_fields = ("title", "category")
  
    

    
    
@admin.register(MembersOf)
class MembersOfAdmin(ModelAdmin):
    list_display = ("title", "image", "url")
    search_fields = ("title",)
  
 