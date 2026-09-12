from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from tinymce.models import HTMLField


class Services(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=1000)
    document = HTMLField()


    class Meta:
                verbose_name = "Services"
                verbose_name_plural = "Services"


class Articles(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=1000)
    document = HTMLField()
    category = models.CharField(max_length=400)
    published_date = models.DateField(auto_now_add=True)


    class Meta:
            verbose_name = "Articles "
            verbose_name_plural = "Articles"


class DocumentationsAndLitigations(models.Model):
    id = models.AutoField(primary_key=True)

    class Type(models.TextChoices):
        DOCUMENTATION = "DOCUMENTATION", "documentation"
        LEGALOPINION = "LEGAL OPINION", "Legal Opinion"
        LITIGATION = "LITIGATION", "Litigation"

    title = models.CharField(max_length=1000)
    document = HTMLField()
    type = models.CharField(
        max_length=1000, choices=Type.choices, default=Type.DOCUMENTATION
    )
    category = models.CharField(max_length=400)

    class Meta:
        verbose_name = "Document and Litigation"
        verbose_name_plural = "Documents and Litigation"




class LegalCourses(models.Model):
    id = models.AutoField(primary_key=True)

   

    title = models.CharField(max_length=1000)
    document = HTMLField()
    type = models.CharField(max_length=400, default="none")


    class Meta:
            verbose_name = "Legal Courses"
            verbose_name_plural = "Legal Courses"


class CourseMaterials(models.Model):
    id = models.AutoField(primary_key=True)

 
    type = models.CharField(max_length=400, default="none")
    title = models.CharField(max_length=1000)
    document = HTMLField()

    class Meta:
                verbose_name = "Course Materials"
                verbose_name_plural = "Course Materials"


class ConventionAndTreaties(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=1000)
    title = models.CharField(max_length=1000)
    document = HTMLField()


    class Meta:
                    verbose_name = "Conventions and Treaties"
                    verbose_name_plural = "Conventions and Treaties"


class Books(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=1000)
    document = HTMLField()
    author = models.CharField(max_length=400)


    class Meta:
                verbose_name = "Books "
                verbose_name_plural = "Books"
    
    
class AboutUs(models.Model):
    id = models.AutoField(primary_key=True)
    document = HTMLField()

    class Meta:
            verbose_name = "About Us"
            verbose_name_plural = "About Us"
          
    
    
class Career(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=1000)
    document = HTMLField()




class Law(models.Model):
    year = models.PositiveIntegerField(help_text="Year the law was enacted")
    subject = models.CharField(max_length=255)
    delivery_date = models.DateField(blank=True, null=True)
    title = models.CharField(max_length=500)
    document = HTMLField()
    section = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "Law"
        verbose_name_plural = "Laws"
        ordering = ["-year", "title"]

    def __str__(self):
        return f"{self.title} ({self.year})"


class Case(models.Model):
    title = models.CharField(max_length=500)
    division = models.CharField(max_length=255, default="")
    case_no = models.CharField(max_length=100)
    judge = models.CharField(max_length=255, blank=True, null=True)
    advocate = models.CharField(max_length=255, blank=True, null=True)
    citation = models.CharField(max_length=255, blank=True, null=True)
    case_year = models.PositiveIntegerField()
    appellant = models.CharField(max_length=255, verbose_name="Appellant")
    respondent = models.CharField(max_length=255)
    subject = models.CharField(max_length=255, blank=True, null=True)
    delivery_date = models.DateField(blank=True, null=True)
    court = models.CharField(max_length=255)
    document = HTMLField()

    class Meta:
        verbose_name = "Case"
        verbose_name_plural = "Cases"
        ordering = ["-case_year", "-delivery_date"]

    def __str__(self):
        return f"{self.title} - {self.case_no} ({self.case_year})"


class Digest(models.Model):
    title = models.CharField(max_length=500)
    division = models.CharField(max_length=255, blank=True, null=True)
    case_no = models.CharField(max_length=100, blank=True, null=True)
    judge = models.CharField(max_length=255, blank=True, null=True)
    advocate = models.CharField(max_length=255, blank=True, null=True)
    citation = models.CharField(max_length=255, blank=True, null=True)
    case_year = models.PositiveIntegerField(blank=True, null=True)
    appellant = models.CharField(max_length=255, verbose_name="Appellant", blank=True, null=True)
    respondent = models.CharField(max_length=255, blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    delivery_date = models.DateField(blank=True, null=True)
    court = models.CharField(max_length=255, blank=True, null=True)
    document = HTMLField()
    
    # Digest-specific fields
    type = models.CharField(max_length=100)
    subtype = models.CharField(max_length=100, default="")

    class Meta:
        verbose_name = "Digest"
        verbose_name_plural = "Digests"
        ordering = ["-case_year", "-delivery_date"]

    def __str__(self):
        return f"[Digest] {self.title} - {self.type}"\


class Journal(models.Model):


    class Months(models.TextChoices):
      JANUARY = "JANUARY", "January"
      FEBRUARY = "FEBRUARY", "February"
      MARCH = "MARCH", "March"
      APRIL = "APRIL", "April"
      MAY = "MAY", "May"
      JUNE = "JUNE", "June"
      JULY = "JULY", "July"
      AUGUST = "AUGUST", "August"
      SEPTEMBER = "SEPTEMBER", "September"
      OCTOBER = "OCTOBER", "October"
      NOVEMBER = "NOVEMBER", "November"
      DECEMBER = "DECEMBER", "December"


    title = models.CharField(max_length=500)
    division = models.CharField(max_length=255, blank=True, null=True)
    case_no = models.CharField(max_length=100)
    judge = models.CharField(max_length=255, blank=True, null=True)
    advocate = models.CharField(max_length=255, blank=True, null=True)
    citation = models.CharField(max_length=255, blank=True, null=True)
    case_year = models.PositiveIntegerField()
    appellant = models.CharField(max_length=255, verbose_name="Appellant")
    respondent = models.CharField(max_length=255)
    subject = models.CharField(max_length=255, blank=True, null=True)
    delivery_date = models.DateField(blank=True, null=True)
    court = models.CharField(max_length=255)
    document = HTMLField()
    month = models.CharField(max_length=1000, choices=Months.choices, default=Months.JANUARY)

    class Meta:
        verbose_name = "Journal"
        verbose_name_plural = "Journals"
        ordering = ["-case_year", "-delivery_date"]

    def __str__(self):
        return f"{self.title} - {self.case_no} ({self.case_year})"


