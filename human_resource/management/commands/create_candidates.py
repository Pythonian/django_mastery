from django.core.management.base import BaseCommand
from faker import Faker
from faker.providers import DynamicProvider
from random import choice
from human_resource.models import Candidate

university_provider = DynamicProvider(
     provider_name="university",
     elements=["University of Lagos", "University of Ibadan", "University of Benin", "University of Nigeria"],
)

job_code_provider = DynamicProvider(
    provider_name="job_code",
    elements=["FE-22", "BE-22", "FS-22"]
)

fake = Faker()

# then add new provider to faker instance
fake.add_provider(university_provider)
fake.add_provider(job_code_provider)

class Command(BaseCommand):
    # In the shell: python manage.py create_users 5
    help = 'Create random candidates'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of candidates to be created')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        candidate_status = [Candidate.APPROVED, Candidate.DISAPPROVED, Candidate.PENDING]
        personality_choices = [x[0] for x in Candidate.PERSONALITY_CHOICES]
        smoker_choices = [x[0] for x in Candidate.SMOKER_CHOICES]
        languages = [x[0] for x in Candidate.LANGUAGES]
        frameworks = [x[0] for x in Candidate.FRAMEWORKS]
        databases = [x[0] for x in Candidate.DATABASES]
        libraries = [x[0] for x in Candidate.LIBRARIES]
        mobile = [x[0] for x in Candidate.MOBILE]
        others = [x[0] for x in Candidate.OTHERS]
        gender_choices = [x[0] for x in Candidate.GENDER_CHOICES]

        for i in range(total):
            Candidate.objects.create(
                status=choice(candidate_status),
                firstname=fake.unique.first_name(),
                lastname=fake.unique.last_name(),
                email=fake.email(),
                birth_date=fake.date_of_birth(minimum_age=18, maximum_age=65),
                phonenumber=fake.phone_number(),
                job=fake.job_code(),
                personality=choice(personality_choices),
                salary=fake.random_int(),
                gender=choice(gender_choices),
                experience=fake.boolean(),
                smoker=choice(smoker_choices),
                file=fake.file_name(category='text'),
                note=fake.text(),
                message=fake.text(),
                languages=choice(languages),
                frameworks=choice(frameworks),
                databases=choice(databases),
                libraries=choice(libraries),
                mobile=choice(mobile),
                others=choice(others),
                institution=fake.university(),
                course=fake.job(),
                started_course=fake.date_this_decade(),
                finished_course=fake.date_this_decade(),
                course_description=fake.text(),
                course_status=choice(Candidate.COURSE_STATUS_CHOICES)[0],
                company=fake.company(),
                position=fake.catch_phrase(),
                started_job=fake.date_this_year(),
                finished_job=fake.date_this_month(),
                about_job=fake.text(),
                employed=fake.boolean(),
                remote=fake.boolean(),
                travel=fake.boolean(),
                created=fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None)
            )
        self.stdout.write(self.style.SUCCESS(f'{total} candidates created successfully'))
