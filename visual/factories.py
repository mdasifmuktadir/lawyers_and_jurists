import random
import factory
from factory.django import DjangoModelFactory, ImageField
from faker import Faker

from .models import (
    Services, Articles, DocumentationsAndLitigations,
    LegalCourses, CourseMaterials, ConventionAndTreaties, Books, Digest, Law, Case, Journal
)

fake = Faker()


def generate_html_content():
    return f"<h3>{fake.sentence()}</h3><p>{fake.paragraph()}</p><ul><li>{fake.word()}</li><li>{fake.word()}</li></ul>"


class ServicesFactory(DjangoModelFactory):
    class Meta:
        model = Services

    title = factory.Faker('sentence', nb_words=6)
    document = factory.LazyFunction(generate_html_content)


class ArticlesFactory(DjangoModelFactory):
    class Meta:
        model = Articles

    title = factory.Faker('sentence', nb_words=6)
    document = factory.LazyFunction(generate_html_content)
    category = factory.Faker('word')


class DocumentationsAndLitigationsFactory(DjangoModelFactory):
    class Meta:
        model = DocumentationsAndLitigations

    title = factory.Faker('sentence', nb_words=6)
    document = factory.LazyFunction(generate_html_content)
    type = factory.LazyFunction(lambda: random.choice(DocumentationsAndLitigations.Type.values))
    category = factory.Faker('word')




class LegalCoursesFactory(DjangoModelFactory):
    class Meta:
        model = LegalCourses

    title = factory.Faker('sentence', nb_words=6)
    document = factory.LazyFunction(generate_html_content)


class CourseMaterialsFactory(DjangoModelFactory):
    class Meta:
        model = CourseMaterials

    title = factory.Faker('sentence', nb_words=6)
    document = factory.LazyFunction(generate_html_content)


class ConventionAndTreatiesFactory(DjangoModelFactory):
    class Meta:
        model = ConventionAndTreaties

    type = factory.Faker('word')
    title = factory.Faker('sentence', nb_words=6)
    document = factory.LazyFunction(generate_html_content)


class BooksFactory(DjangoModelFactory):
    class Meta:
        model = Books

    title = factory.Faker('sentence', nb_words=5)
    document = factory.LazyFunction(generate_html_content)
    author = factory.Faker('name')


class LawFactory(DjangoModelFactory):
    class Meta:
        model = Law

    year = factory.LazyFunction(lambda: random.randint(1950, 2024))
    subject = factory.Faker("word")
    delivery_date = factory.Faker("date_object")
    title = factory.LazyAttribute(lambda o: f"The {o.subject.title()} Act of {o.year}")
    
    # FIX: Use factory.Faker directly without lambdas or .generate()
    document = factory.Faker("paragraph", nb_sentences=5)
    section = factory.LazyFunction(lambda: f"Section {random.randint(1, 150)}")


class CaseFactory(DjangoModelFactory):
    class Meta:
        model = Case

    title = factory.LazyAttribute(lambda o: f"{o.appellant} v. {o.respondent}")
    division = factory.Iterator(["Appellate Division", "High Court Division", "Civil Division"])
    case_no = factory.LazyFunction(lambda: f"Civil Appeal No. {random.randint(100, 999)} of {random.randint(2010, 2024)}")
    judge = factory.Faker("name")
    advocate = factory.Faker("name")
    citation = factory.LazyFunction(lambda: f"{random.randint(10, 50)} DLR ({random.randint(2000, 2023)}) {random.randint(100, 900)}")
    case_year = factory.LazyFunction(lambda: random.randint(2000, 2024))
    appellant = factory.Faker("company")
    respondent = factory.Faker("company")
    subject = factory.Faker("word")
    delivery_date = factory.Faker("date_object")
    court = factory.Iterator(["Supreme Court", "High Court", "District Court"])
    
    # FIX: Clean paragraph generator for HTML output
    document = factory.Faker("paragraph", nb_sentences=5)


class DigestFactory(DjangoModelFactory):
    class Meta:
        model = Digest

    title = factory.LazyAttribute(lambda o: f"{o.appellant} v. {o.respondent}")
    division = factory.Iterator(["Appellate Division", "High Court Division"])
    case_no = factory.LazyFunction(lambda: f"Writ Petition No. {random.randint(1000, 9999)} of {random.randint(2015, 2024)}")
    judge = factory.Faker("name")
    advocate = factory.Faker("name")
    citation = factory.LazyFunction(lambda: f"{random.randint(50, 80)} BLC ({random.randint(2010, 2023)}) {random.randint(1, 300)}")
    case_year = factory.LazyFunction(lambda: random.randint(2010, 2024))
    appellant = factory.Faker("name")
    respondent = factory.Faker("company")
    subject = factory.Faker("word")
    delivery_date = factory.Faker("date_object")
    court = factory.Iterator(["Supreme Court", "High Court"])
    
    # FIX: Clean paragraph generator
    document = factory.Faker("paragraph", nb_sentences=5)
    type = factory.Iterator(["CONSTITUTIONAL", "CRIMINAL", "CIVIL", "COMMERCIAL"])
    subtype = factory.Iterator(["Writ", "Appeal", "Revision", "Review"])


class JournalFactory(DjangoModelFactory):
    class Meta:
        model = Journal

    title = factory.LazyAttribute(lambda o: f"{o.appellant} v. {o.respondent}")
    division = factory.Iterator(["Appellate Division", "High Court Division", "Civil Division"])
    case_no = factory.LazyFunction(lambda: f"Civil Appeal No. {random.randint(100, 999)} of {random.randint(2010, 2024)}")
    judge = factory.Faker("name")
    advocate = factory.Faker("name")
    citation = factory.LazyFunction(lambda: f"{random.randint(10, 50)} DLR ({random.randint(2000, 2023)}) {random.randint(100, 900)}")
    case_year = factory.LazyFunction(lambda: random.randint(2000, 2024))
    appellant = factory.Faker("company")
    respondent = factory.Faker("company")
    subject = factory.Faker("word")
    delivery_date = factory.Faker("date_object")
    court = factory.Iterator(["Supreme Court", "High Court", "District Court"])
    month = factory.LazyFunction(lambda: random.choice(Journal.Months.values))

    # FIX: Clean paragraph generator for HTML output
    document = factory.Faker("paragraph", nb_sentences=5)


ALL_FACTORIES = [
    ServicesFactory,
    ArticlesFactory,
    DocumentationsAndLitigationsFactory,
    DigestFactory,
    LawFactory,
    CaseFactory,
  
    LegalCoursesFactory,
    CourseMaterialsFactory,
    ConventionAndTreatiesFactory,
    BooksFactory,
 
]