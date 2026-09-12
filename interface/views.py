from django.db.models.aggregates import Max
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.viewsets import ReadOnlyModelViewSet
import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
from rest_framework.response import Response


from .models import (
  
    Clients,
    Contact,
    MembersOf,
    FeedBack,
 
    SocialMedia,
    Videos,
    Carousel,
    Gallery,
  
)
from .serializers import (

    ClientsSerializer,
    ContactSerializer,
  
    FeedBackSerializer,

    SocialMediaSerializer,
    VideosSerializer,
    CarouselSerializer,
    GallerySerializer,
    MembersOfSerializer
   
)


class BaseReadOnlyViewSet(ReadOnlyModelViewSet):
    """Base ViewSet providing list, filtered list, and detail retrieval by ID."""

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]



class FeedBackViewSet(BaseReadOnlyViewSet):
    queryset = FeedBack.objects.all().order_by("-id")
    serializer_class = FeedBackSerializer
    search_fields = ["client_description", "message"]
    ordering_fields = ["id", "client_description"]


class VideosViewSet(BaseReadOnlyViewSet):
    queryset = Videos.objects.all().order_by("-id")[:10]
    serializer_class = VideosSerializer
    search_fields = ["title", "description"]
    ordering_fields = ["id", "title"]

    @action(detail=False, methods=['get'], pagination_class=None)
    def all(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ClientsViewSet(BaseReadOnlyViewSet):
    queryset = Clients.objects.all().order_by("-id")
    serializer_class = ClientsSerializer
    search_fields = ["name"]
    ordering_fields = ["id", "name"]
    
    @action(detail=False, methods=['get'], pagination_class=None)
    def all(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SocialMediaViewSet(BaseReadOnlyViewSet):
    queryset = SocialMedia.objects.all().order_by("-id")
    serializer_class = SocialMediaSerializer
    filterset_fields = ["platform"]
    search_fields = ["platform"]
    ordering_fields = ["id", "platform"]


class ContactViewSet(BaseReadOnlyViewSet):
    queryset = Contact.objects.all().order_by("-id")
    serializer_class = ContactSerializer
    search_fields = ["name", "email", "telephones", "cell"]
    ordering_fields = ["id", "name", "email"]
    
    
class CarouselViewSet(BaseReadOnlyViewSet):
    queryset = Carousel.objects.all().order_by("-id")
    serializer_class = CarouselSerializer
    filterset_fields = ["title"]
    ordering_fields = ["id", "title"]
    
    
class GalleryViewSet(BaseReadOnlyViewSet):
    queryset = Gallery.objects.all().order_by("-id")
    serializer_class = GallerySerializer
    filterset_fields = ["category"]
    ordering_fields = ["id", "title", "category"]
    pagination_class = None
    
    @action(detail=False, methods=['get'])
    def distinct_categories(self, request):
        distinct_ids = (
            Gallery.objects.values('category')
            .annotate(max_id=Max('id'))
            .values_list('max_id', flat=True)
        )
        queryset = Gallery.objects.filter(id__in=distinct_ids)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    
class MembersOfViewSet(BaseReadOnlyViewSet):
    queryset = MembersOf.objects.all().order_by("-id")
    serializer_class = MembersOfSerializer
    filterset_fields = ["title"]
    ordering_fields = ["id", "title"]
    
    
@csrf_exempt
def tinymce_image_upload(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        
        file_path = os.path.join('uploads', file.name)
        saved_path = default_storage.save(file_path, file)
        
        # Generates relative segment: /media/uploads/filename.jpg
        relative_url = settings.MEDIA_URL + saved_path
        
        # --- FIX: Force the Android emulator IP instead of using request host ---
        emulator_domain = "http://10.0.2.2:8000"
        absolute_url = f"{emulator_domain}{relative_url}"
        
        return JsonResponse({'location': absolute_url})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)