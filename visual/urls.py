from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    ArticlesViewSet,
    BooksViewSet,
    JournalViewSet,

    CourseMaterialsViewSet,
    DocumentationsAndLitigationsViewSet,

    LegalCoursesViewSet,
    ServicesViewSet,
    ConventionAndTreatiesViewSet,
    LatestAboutUsViewSet,
    CareerViewSet,
    LawViewSet,
    DigestViewSet,
    CaseViewSet,
  
)

router = DefaultRouter()
router.register(r"services", ServicesViewSet)
router.register(r"articles", ArticlesViewSet)
router.register(
    r"documentations-and-litigations", DocumentationsAndLitigationsViewSet
)

router.register(r"legal-courses", LegalCoursesViewSet)
router.register(r"course-materials", CourseMaterialsViewSet)
router.register(r"books", BooksViewSet)
router.register(r"laws", LawViewSet)
router.register(r"digests", DigestViewSet)
router.register(r"cases", CaseViewSet)
router.register(r"conventions-and-treaties", ConventionAndTreatiesViewSet)
router.register(r"about-us", LatestAboutUsViewSet)
router.register(r"career", CareerViewSet)
router.register(r"journals", JournalViewSet)


urlpatterns = [
    path("", include(router.urls)),
]