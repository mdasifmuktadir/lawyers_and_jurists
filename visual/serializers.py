from rest_framework import serializers
from visual.models import (
    Services,
    Articles,
    DocumentationsAndLitigations,
    Law, 
    Case, 
    Digest,
    LegalCourses,
    CourseMaterials,
    ConventionAndTreaties,
    Books,
    AboutUs,
    Career,
    Journal

)


class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = ['id', 'title', 'document']


class ArticlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articles
        fields = '__all__'


class DocumentationsAndLitigationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentationsAndLitigations
        fields = '__all__'




class LegalCoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalCourses
        fields = '__all__'


class CourseMaterialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseMaterials
        fields = '__all__'


class ConventionAndTreatiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConventionAndTreaties
        fields = '__all__'


class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = '__all__'
        
class AboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUs
        fields = '__all__'
        
class CareerSerializer(serializers.ModelSerializer):
     class Meta:
         model = Career
         fields = '__all__'

class LawSerializer(serializers.ModelSerializer):
    """Full detail serializer for Law model."""
    class Meta:
        model = Law
        fields = "__all__"

class CaseSerializer(serializers.ModelSerializer):
    """Full detail serializer for Case model."""
    class Meta:
        model = Case
        fields = "__all__"

class DigestSerializer(serializers.ModelSerializer):
    """Full detail serializer for Digest model."""
    class Meta:
        model = Digest
        fields = "__all__"


class JournalSerializer(serializers.ModelSerializer):
    """Full detail serializer for Case model."""
    class Meta:
        model = Journal
        fields = "__all__"






