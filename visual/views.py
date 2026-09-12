from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.generics import RetrieveAPIView
from rest_framework.exceptions import NotFound
from django.utils.html import strip_tags

from .models import (
    Articles,
    Books,
    Law,
    Digest,
    Case,
    CourseMaterials,
    DocumentationsAndLitigations,
    LegalCourses,
    Services,
    ConventionAndTreaties,
    AboutUs,
    Career,
    Journal
)
from .serializers import (
    ArticlesSerializer,
    BooksSerializer,
    LawSerializer,
    DigestSerializer,
    CaseSerializer,
    CourseMaterialsSerializer,
    DocumentationsAndLitigationsSerializer,
    LegalCoursesSerializer,
    ServicesSerializer,
    ConventionAndTreatiesSerializer,
    AboutUsSerializer,
    CareerSerializer,
    JournalSerializer
)


class BaseReadOnlyViewSet(ReadOnlyModelViewSet):
    """Base ViewSet providing list, filtered list, and detail retrieval by ID."""

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]


class ServicesViewSet(BaseReadOnlyViewSet):
    queryset = Services.objects.all().order_by("-id")
    serializer_class = ServicesSerializer
    search_fields = ["title", "document"]
    ordering_fields = ["id", "title"]

    @action(detail=False, methods=['get'], pagination_class=None)
    def all(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ArticlesViewSet(BaseReadOnlyViewSet):
    queryset = Articles.objects.all().order_by("-id")
    serializer_class = ArticlesSerializer
    filterset_fields = ["category"]
    search_fields = ["title", "document", "category"]
    ordering_fields = ["id", "title", "category"]
    pagination_class = None  # Disable pagination for this viewset
    
    class LightArticlesSerializer(serializers.ModelSerializer):
        class Meta:
            model = Articles
            fields = ["id", "title", "published_date"]
    
    @action(detail=False, methods=["get"], )
    def categories(self, request):
        # Grab only distinct single values from the database
        values = self.get_queryset().order_by().values_list("category", flat=True).distinct()
        return Response(list(values))
    
    @action(detail=False, methods=["get"])
    def latest(self, request):
        top_articles = self.get_queryset().order_by("-published_date")[:3]
        serializer = self.LightArticlesSerializer(top_articles, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def get_articles(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        for item in data:
            if "document" in item and item["document"]:
                item["document"] = item["document"][:200]
        return Response(data)


class DocumentationsAndLitigationsViewSet(BaseReadOnlyViewSet):
    queryset = DocumentationsAndLitigations.objects.all().order_by("-id")
    serializer_class = DocumentationsAndLitigationsSerializer
    filterset_fields = ["type", "category"]
    search_fields = ["title", "document", "category"]
    ordering_fields = ["id", "title", "type", "category"]
    
    
    @action(detail=False, methods=["get"])
    def types(self, request):
    # .order_by() removes default ordering so .distinct() evaluates only 'type'
       values = (
           self.get_queryset()
           .order_by()
           .values_list("type", flat=True)
           .distinct()
       )
       return Response(list(values))

    @action(detail=False, methods=["get"])
    def documentations(self, request):
        # 1. Filter by type 'DOCUMENTATION' and select only 'id' and 'title'
        queryset = (
            self.get_queryset()
            .filter(type="DOCUMENTATION")
            .values("id", "title")
        )

        # 2. Disable pagination for this specific action
        self.pagination_class = None

        # 3. Return the array of dictionary objects: [{"id": 1, "title": "..."}, ...]
        return Response(list(queryset))


    @action(detail=False, methods=["get"])
    def legal_opinions(self, request):
        # 1. Filter by type 'DOCUMENTATION' and select only 'id' and 'title'
        queryset = (
            self.get_queryset()
            .filter(type="LEGAL OPINION")
            .values("id", "title", "document")
        )

        # 2. Disable pagination for this specific action
        self.pagination_class = None

        data = [
        {
            "id": item["id"],
            "title": item["title"],
            # Strips HTML tags before slicing to avoid returning broken HTML tags:
            "document": strip_tags(item["document"] or "")[:200]
        }
        for item in queryset
    ]

        # 3. Return the array of dictionary objects: [{"id": 1, "title": "..."}, ...]
        return Response(data)


    @action(detail=False, methods=["get"])
    def litigation_categories(self, request):
        # 1. Filter by type 'DOCUMENTATION' and select only 'id' and 'title'
        queryset = (
            self.get_queryset()
            .filter(type="LITIGATION")
            .order_by()
            .values_list("category", flat=True)
            .distinct()
       
        )

        # 2. Disable pagination for this specific action
        self.pagination_class = None

        # 3. Return the array of dictionary objects: [{"id": 1, "title": "..."}, ...]
        return Response(list(queryset))


    @action(
        detail=False,
        methods=["get"],
      
    )
    def litigation_list(self, request, category=None):
        # 1. Filter by type 'DOCUMENTATION' and select only 'id' and 'title'

        category = request.query_params.get("category")

        queryset = (
            self.get_queryset()
            .filter(type="LITIGATION", category=category)
            .values("id", "title", "document")
        )

        # 2. Disable pagination for this specific action
        self.pagination_class = None

        data = [
        {
            "id": item["id"],
            "title": item["title"],
            # Strips HTML tags before slicing to avoid returning broken HTML tags:
            "document": strip_tags(item["document"] or "")[:200]
        }
        for item in queryset
    ]

        # 3. Return the array of dictionary objects: [{"id": 1, "title": "..."}, ...]
        return Response(data)





class LegalCoursesViewSet(BaseReadOnlyViewSet):
    queryset = LegalCourses.objects.all().order_by("-id")
    serializer_class = LegalCoursesSerializer
    search_fields = ["title", "document"]
    ordering_fields = ["id", "title"]
    filterset_fields = ["type"]
    pagination_class = None
    
    @action(detail=False, methods=["get"], )
    def types(self, request):
        values = self.get_queryset().order_by().values_list("type", flat=True).distinct()
        return Response(list(values))

    @action(detail=False, methods=["get"], )
    def course_list(self, request, category=None):
            # 1. Filter by type 'DOCUMENTATION' and select only 'id' and 'title'
    
            type = request.query_params.get("type")
    
            queryset = (
                self.get_queryset()
                .filter(type=type)
                .values("id", "title", "document", "type")
            )
    
            # 2. Disable pagination for this specific action
            self.pagination_class = None
    
            data = [
            {
                "id": item["id"],
                "title": item["title"],
                "type":item["type"],
                # Strips HTML tags before slicing to avoid returning broken HTML tags:
                "document": strip_tags(item["document"] or "")[:200]
            }
            for item in queryset
        ]
    
            # 3. Return the array of dictionary objects: [{"id": 1, "title": "..."}, ...]
            return Response(data)


class CourseMaterialsViewSet(BaseReadOnlyViewSet):
    queryset = CourseMaterials.objects.all().order_by("-id")
    serializer_class = CourseMaterialsSerializer
    search_fields = ["title", "document"]
    ordering_fields = ["id", "title"]
    
    @action(detail=False, methods=["get"], )
    def types(self, request):
        values = self.get_queryset().order_by().values_list("type", flat=True).distinct()
        return Response(list(values))

    @action(detail=False, methods=["get"], )
    def materials_list(self, request, category=None):
                # 1. Filter by type 'DOCUMENTATION' and select only 'id' and 'title'
        
                type = request.query_params.get("type")
        
                queryset = (
                    self.get_queryset()
                    .filter(type=type)
                    .values("id", "title", "document", "type")
                )
        
                # 2. Disable pagination for this specific action
                self.pagination_class = None
        
                data = [
                {
                    "id": item["id"],
                    "title": item["title"],
                    "type":item["type"],
                    # Strips HTML tags before slicing to avoid returning broken HTML tags:
                    "document": strip_tags(item["document"] or "")[:200]
                }
                for item in queryset
            ]
        
                # 3. Return the array of dictionary objects: [{"id": 1, "title": "..."}, ...]
                return Response(data)


class ConventionAndTreatiesViewSet(BaseReadOnlyViewSet):
    queryset = ConventionAndTreaties.objects.all().order_by("-id")
    serializer_class = ConventionAndTreatiesSerializer
    pagination_class = None
    filterset_fields = ["type"]
    search_fields = ["title", "document", "type"]
    ordering_fields = ["id", "title", "type"]
    
    
    @action(detail=False, methods=["get"], )
    def types(self, request):
        values = self.get_queryset().order_by().values_list("type", flat=True).distinct()
        return Response(list(values))


    @action(detail=False, methods=["get"], )
    def type_list(self, request, category=None):
                    # 1. Filter by type 'DOCUMENTATION' and select only 'id' and 'title'
            
                    type = request.query_params.get("type")
            
                    queryset = (
                        self.get_queryset()
                        .filter(type=type)
                        .values("id", "title", "document", "type")
                    )
            
                    # 2. Disable pagination for this specific action
                    self.pagination_class = None
            
                    data = [
                    {
                        "id": item["id"],
                        "title": item["title"],
                        "type":item["type"],
                        # Strips HTML tags before slicing to avoid returning broken HTML tags:
                        "document": strip_tags(item["document"] or "")[:200]
                    }
                    for item in queryset
                ]
            
                    # 3. Return the array of dictionary objects: [{"id": 1, "title": "..."}, ...]
                    return Response(data)
    


class BooksViewSet(BaseReadOnlyViewSet):
    queryset = Books.objects.all().order_by("-id")
    serializer_class = BooksSerializer
    filterset_fields = ["author"]
    search_fields = ["title", "document", "author"]
    ordering_fields = ["id", "title", "author"]
    
    
    @action(detail=False, methods=["get"], )
    def authors(self, request):
        values = self.get_queryset().order_by().values_list("author", flat=True).distinct()
        return Response(list(values))

    
    @action(detail=False, methods=["get"], )
    def list_by_author(self, request, category=None):
                    # 1. Filter by type 'DOCUMENTATION' and select only 'id' and 'title'
            
                    author = request.query_params.get("author")
            
                    queryset = (
                        self.get_queryset()
                        .filter(author=author)
                        .values("id", "title", "document", "author")
                    )
            
                    # 2. Disable pagination for this specific action
                    self.pagination_class = None
            
                    data = [
                    {
                        "id": item["id"],
                        "title": item["title"],
                        "author":item["author"],
                        # Strips HTML tags before slicing to avoid returning broken HTML tags:
                        "document": strip_tags(item["document"] or "")[:200]
                    }
                    for item in queryset
                ]
            
                    # 3. Return the array of dictionary objects: [{"id": 1, "title": "..."}, ...]
                    return Response(data)
    
    
    
class LatestAboutUsViewSet(BaseReadOnlyViewSet):
    serializer_class = AboutUsSerializer
    queryset = AboutUs.objects.none()  # Satisfies DRF router requirements safely

    def list(self, request, *args, **kwargs):
        obj = AboutUs.objects.order_by('-id').first()
        if not obj:
            raise NotFound("No record found.")
        serializer = self.get_serializer(obj)
        return Response(serializer.data)
    
    
class CareerViewSet(BaseReadOnlyViewSet):
    queryset = Career.objects.all().order_by("-id")
    serializer_class = CareerSerializer
    filterset_fields = ["id", "title"]
    search_fields = ["title", "document", "id"]
    ordering_fields = ["id", "document", "title"]
    lookup_field = 'title'
    
    class LightCareerSerializer(serializers.ModelSerializer):
        class Meta:
            model = Career
            fields = ["id", "title"]
    
    
    
    @action(detail=False, methods=["get"])
    def all(self, request):
        all_docs = self.get_queryset().all()
        serializer = self.LightCareerSerializer(all_docs, many=True)
        return Response(serializer.data)



class LawViewSet(BaseReadOnlyViewSet):
    queryset = Law.objects.all().order_by("-year", "title")
    serializer_class = LawSerializer
    filterset_fields = ["year", "subject"]
    search_fields = ["title", "document", "subject"]
    ordering_fields = ["id", "year", "title", "subject"]


    @action(detail=False, methods=["get"])
    def years(self, _request):
        years = list(
            self.get_queryset()
            .order_by()
            .values_list("year", flat=True)
            .distinct()
        )

        if not years:
            return Response([])

        start_year = min(years)
        end_year = max(years)
        ranges = []

        while start_year <= end_year:
            range_end = min(start_year + 10, end_year)
            ranges.append(f"{start_year}-{range_end}")
            start_year = range_end + 1

        return Response(ranges)


    @action(detail=False, methods=["get"])
    def list_by_time(self, request):
        year = request.query_params.get("year")
    
        if not year:
            return Response(
                {"error": "Query parameter 'year' is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
    
        try:
            start_year_str, end_year_str = year.split("-")
            start_year = int(start_year_str)
            end_year = int(end_year_str)
        except (ValueError, AttributeError):
            return Response(
                {"error": "Query parameter 'year' must be a range like '1990-2010'."},
                status=status.HTTP_400_BAD_REQUEST,
            )
    
        # Filter by year range (inclusive) and retrieve all fields except 'document'
        queryset = (
            self.get_queryset()
            .filter(year__gte=start_year, year__lte=end_year)
            .values(
                "id",
                "year",
                "subject",
                "delivery_date",
                "title",
                "section",
            )
        )
    
        return Response(list(queryset))


class DigestViewSet(BaseReadOnlyViewSet):
    queryset = Digest.objects.all().order_by("-id")
    serializer_class = DigestSerializer
    filterset_fields = ["case_year", "subject"]
    search_fields = ["title", "document", "subject"]
    ordering_fields = ["id", "case_year", "title", "subject"]


    @action(detail=False, methods=["get"])
    def types(self, request):
        values = self.get_queryset().order_by().values_list("type", flat=True).distinct()
        return Response(list(values))



    @action(detail=False, methods=["get"])
    def subtypes(self, request):
            type = request.query_params.get("type")
            values = self.get_queryset().filter(type=type).order_by().values_list("subtype", flat=True).distinct()
            return Response(list(values))

    @action(detail=False, methods=["get"])
    def subtype_list(self, request):
        subtype = request.query_params.get("subtype")
        queryset = (self
                    .get_queryset()
                    .filter(subtype=subtype)
                    .values("id",  
                            "title", 
                            "division", 
                            "case_no", 
                            "judge", 
                            "advocate", 
                            "citation", 
                            "case_year", 
                            "appellant", 
                            "respondent", 
                            "subject", 
                            "delivery_date", 
                            "court",
                            "type",
                            "subtype"))

        return Response(list(queryset))



class CaseViewSet(BaseReadOnlyViewSet):
    pagination_class = None  # Disable pagination for this viewset
    queryset = Case.objects.all().order_by("-id")
    serializer_class = CaseSerializer
    filterset_fields = ["case_year", "subject", "division", "court"]
    search_fields = ["title", "document", "subject"]
    ordering_fields = ["id", "case_year", "title", "subject"]





    @action(detail=False, methods=["get"])
    def list_by_division(self, request):
        division = request.query_params.get("division")
    
        if not division:
            return Response(
                {"error": "Query parameter 'year' is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
    
        # Filter by year and retrieve all fields except 'document'
        queryset = (
            self.get_queryset()
            .filter(division=division)
            .values(
                "id",
                "title",
                "division",
                "case_no",
                "judge",
                "advocate",
                "citation",
                "case_year",
                "appellant",
                "respondent",
                "subject",
                "delivery_date",
                "court"
                )
        )
    
        return Response(list(queryset))



class JournalViewSet(BaseReadOnlyViewSet):
    pagination_class = None  # Disable pagination for this viewset
    queryset = Journal.objects.all().order_by("-id")
    serializer_class = JournalSerializer
    filterset_fields = ["case_year", "subject", "division", "court"]
    search_fields = ["title", "document", "subject"]
    ordering_fields = ["id", "case_year", "title", "subject"]


    @action(detail=False, methods=["get"])
    def years(self, request):
        values = self.get_queryset().order_by().values_list("case_year", flat=True).distinct()
        return Response(list(values))

    @action(detail=False, methods=["get"])
    def months_by_year(self, request):
        year = request.query_params.get("year")
        if not year:
                    return Response(
                        {"error": "Query parameter 'year' is required."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            
                # Filter by year and retrieve all fields except 'document'
        values = self.get_queryset().filter(case_year=year).order_by().values_list("month", flat=True).distinct()
                
            
        return Response(list(values))


    @action(detail=False, methods=["get"])
    def list_by_month(self, request):
        month = request.query_params.get("month")
    
        if not month:
            return Response(
                {"error": "Query parameter 'year' is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
    
        # Filter by year and retrieve all fields except 'document'
        queryset = (
            self.get_queryset()
            .filter(month=month)
            .values(
                "id",
                "title",
                "division",
                "case_no",
                "judge",
                "advocate",
                "citation",
                "case_year",
                "appellant",
                "respondent",
                "subject",
                "delivery_date",
                "court"
                )
        )
    
        return Response(list(queryset))
