from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
   
    ClientsViewSet,
    ContactViewSet,
    SocialMediaViewSet,
    VideosViewSet,
    FeedBackViewSet,
    CarouselViewSet,
    GalleryViewSet,
    MembersOfViewSet,
    
    tinymce_image_upload,

  
)

router = DefaultRouter()

router.register(r"feedback", FeedBackViewSet)
router.register(r"videos", VideosViewSet)
router.register(r"clients", ClientsViewSet)
router.register(r"social-media", SocialMediaViewSet)
router.register(r"contact", ContactViewSet)
router.register(r"carousel", CarouselViewSet)
router.register(r"gallery", GalleryViewSet)
router.register(r"members-of", MembersOfViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path('upload-image/', tinymce_image_upload, name='tinymce_image_upload'),
]