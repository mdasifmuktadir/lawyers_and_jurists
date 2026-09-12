import random
import factory
from factory.django import DjangoModelFactory, ImageField
from faker import Faker

from .models import (
    LawyerProfile
)

fake = Faker()


def generate_html_content():
    return f"<h3>{fake.sentence()}</h3><p>{fake.paragraph()}</p><ul><li>{fake.word()}</li><li>{fake.word()}</li></ul>"





class LawyerProfileFactory(DjangoModelFactory):
    class Meta:
        model = LawyerProfile

    # Automatically creates a User with the LAWYER role
   
    full_name = factory.Faker('name')
    specialty = factory.Faker(
        'random_element', 
        elements=['Criminal Law', 'Corporate Law', 'Family Law', 'Intellectual Property', 'Real Estate Law']
    )
    bio = factory.Faker('paragraph', nb_sentences=3)
    hourly_rate = factory.Faker('pydecimal', left_digits=3, right_digits=2, positive=True)
    years_of_experience = factory.Faker('random_int', min=1, max=35)
    office_location = factory.Faker('address')
    lawyer_photo = ImageField(filename='lawyer_photo.jpg', width=200, height=200)
    designation = factory.Faker(
        'random_element', 
        elements=['Associate', 'Senior Associate', 'Partner', 'Managing Partner']
    )




ALL_FACTORIES = [
   
   LawyerProfileFactory
]