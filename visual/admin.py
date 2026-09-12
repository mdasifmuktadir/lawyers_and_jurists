
from unfold.admin import ModelAdmin
from django.contrib import admin
from tinymce.models import HTMLField
from tinymce.widgets import TinyMCE
from .models import (
    Services,
    Articles,
    DocumentationsAndLitigations,
    Digest,
    Law,
    Case,
    LegalCourses,
    CourseMaterials,
    ConventionAndTreaties,
    Books,
    AboutUs,
    Career,
    Journal
  
)


@admin.register(Services)
class ServicesAdmin(ModelAdmin):
    formfield_overrides = {
            HTMLField: {"widget": TinyMCE},
        }
    list_display = ("title",)
    search_fields = ("title", "document")


@admin.register(Articles)
class ArticlesAdmin(ModelAdmin):

    formfield_overrides = {
        HTMLField: {"widget": TinyMCE},
    }
    list_display = ("title", "category", "id", "published_date")
    list_filter = ("category",)
    search_fields = ("title", "category", "document")
    list_editable = ['category']



@admin.register(DocumentationsAndLitigations)
class DocumentationsAndLitigationsAdmin(ModelAdmin):
    formfield_overrides = {
            HTMLField: {"widget": TinyMCE},
        }
    list_display = ("title", "type", "category")
    list_filter = ("type", "category")
    search_fields = ("title", "category", "document")





@admin.register(LegalCourses)
class LegalCoursesAdmin(ModelAdmin):
    formfield_overrides = {
            HTMLField: {"widget": TinyMCE},
        }    
    list_display = ("title", "type")
    search_fields = ("title", "document")


@admin.register(CourseMaterials)
class CourseMaterialsAdmin(ModelAdmin):
    formfield_overrides = {
            HTMLField: {"widget": TinyMCE},
        }
    list_display = ("title", "type")
    search_fields = ("title", "document")


@admin.register(ConventionAndTreaties)
class ConventionAndTreatiesAdmin(ModelAdmin):
    formfield_overrides = {
            HTMLField: {"widget": TinyMCE},
        }
    list_display = ("title", "type")
    list_filter = ("type",)
    search_fields = ("title", "type", "document")


@admin.register(Books)
class BooksAdmin(ModelAdmin):
    formfield_overrides = {
            HTMLField: {"widget": TinyMCE},
        }
    list_display = ("title", "author")
    search_fields = ("title", "author", "document")
    
    
@admin.register(AboutUs)
class AboutUsAdmin(ModelAdmin):
    formfield_overrides = {
            HTMLField: {"widget": TinyMCE},
        }
    list_display = ("id", "document")
    
    
@admin.register(Career)
class CareerAdmin(ModelAdmin):
    formfield_overrides = {
            HTMLField: {"widget": TinyMCE},
        }
    list_display = ("id", "title")




@admin.register(Law)
class LawAdmin(ModelAdmin):
    formfield_overrides = {
            HTMLField: {"widget": TinyMCE},
        }    
    list_display = ("title", "year", "subject", "section", "delivery_date")
    list_filter = ("year", "subject")
    search_fields = ("title", "subject", "section", "document")
    ordering = ("-year", "title")


@admin.register(Case)
class CaseAdmin(ModelAdmin):
    formfield_overrides = {
            HTMLField: {"widget": TinyMCE},
        }   
    list_display = (
        "title",
        "case_no",
        "case_year",
        "court",
        "division",
        "delivery_date",
    )
    list_filter = ("court", "division", "case_year")
    search_fields = (
        "title",
        "case_no",
        "judge",
        "advocate",
        "citation",
        "appellant",
        "respondent",
        "subject",
        "document",
    )
    ordering = ("-case_year", "-delivery_date")


@admin.register(Digest)
class DigestAdmin(ModelAdmin):

    formfield_overrides = {
            HTMLField: {"widget": TinyMCE},
        }
    list_display = (
        "title",
        "type",
        "subtype",
        "case_no",
        "case_year",
        "court",
        "delivery_date",
    )
    list_filter = ("type", "subtype", "court", "case_year")
    search_fields = (
        "title",
        "case_no",
        "type",
        "subtype",
        "judge",
        "advocate",
        "citation",
        "appellant",
        "respondent",
        "subject",
        "document",
    )
    ordering = ("-case_year", "-delivery_date")



@admin.register(Journal)
class JournalAdmin(ModelAdmin):
    formfield_overrides = {
            HTMLField: {"widget": TinyMCE},
        }
    list_display = (
        "title",
        "case_no",
        "case_year",
        "court",
        "division",
        "delivery_date",
    )
    list_filter = ("court", "division", "case_year")
    search_fields = (
        "title",
        "case_no",
        "judge",
        "advocate",
        "citation",
        "appellant",
        "respondent",
        "subject",
        "document",
    )
    ordering = ("-case_year", "-delivery_date")

