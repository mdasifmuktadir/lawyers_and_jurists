import random
import factory
from factory.django import DjangoModelFactory, ImageField
from faker import Faker
from factory.fuzzy import FuzzyChoice

from .models import (
    FeedBack, Videos, Clients, SocialMedia, Contact, Gallery
)

fake = Faker()


def generate_html_content():
    return f"<h3>{fake.sentence()}</h3><p>{fake.paragraph()}</p><ul><li>{fake.word()}</li><li>{fake.word()}</li></ul>"





class FeedBackFactory(DjangoModelFactory):
    class Meta:
        model = FeedBack

    name = factory.Faker('name')
    message = factory.Faker('paragraph')


class VideosFactory(DjangoModelFactory):
    class Meta:
        model = Videos

    title = factory.Faker('sentence', nb_words=6)
    video_url = factory.Faker('url')
    description = factory.Faker('paragraph')


class ClientsFactory(DjangoModelFactory):
    class Meta:
        model = Clients

    name = factory.Faker('company')
    logo = ImageField(filename='client_logo.jpg', width=200, height=200, color='blue')
    website = factory.Faker('url')


class SocialMediaFactory(DjangoModelFactory):
    class Meta:
        model = SocialMedia

    platform = factory.Faker('word')
    url = factory.Faker('url')
    icon = ImageField(filename='social_icon.png', width=32, height=32, color='red')


class ContactFactory(DjangoModelFactory):
    class Meta:
        model = Contact

    name = factory.Faker('name')
    email = factory.Faker('email')
    telephones = factory.Faker('phone_number')
    cell = factory.Faker('phone_number')


class GalleryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Gallery

    title = factory.Faker('sentence', nb_words=4)
    # Pick a random valid value directly from your model choices
    category = FuzzyChoice([choice[0] for choice in Gallery.CategoryChoices.choices])
    # Generates a dummy image file in memory without needing actual image assets
    image = factory.django.ImageField(color='blue', width=800, height=600)
    description = factory.Faker('paragraph', nb_sentences=3)

ALL_FACTORIES = [
    GalleryFactory,
    FeedBackFactory,
    VideosFactory,
    ClientsFactory,
    SocialMediaFactory,
    ContactFactory,
]