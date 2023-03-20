from django.test import TestCase
from datetime import date
import datetime
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from ..models import Candidate


class CandidateModelTestCase(TestCase):
    def setUp(self):
        self.candidate = Candidate.objects.create(
            status='A',
            firstname='John',
            lastname='Doe',
            email='johndoe@example.com',
            birth_date=date(1990, 1, 1),
            phonenumber='1234567890',
            job='12345',
            personality='I am outgoing',
            salary='100000',
            gender='M',
            experience=True,
            smoker='N',
            file=SimpleUploadedFile('file.txt', b'file_content'),
            image=SimpleUploadedFile('image.jpg', b'image_content'),
            note='test note',
            languages=['Python', 'Javascript'],
            frameworks=['Django'],
            databases=['PostgreSQL', 'MySQL'],
            libraries=['Bootstrap', 'jQuery'],
            mobile=['Flutter', 'React native'],
            others=['GIT', 'Docker'],
            institution='Example University',
            course='Computer Science',
            started_course=date(2010, 1, 1),
            finished_course=date(2014, 1, 1),
            course_description='Description',
            course_status='I have completed the course',
            company='Example Company',
            position='Software Developer',
            started_job=date(2014, 1, 1),
            finished_job=date(2018, 1, 1),
            about_job='Description',
            employed=True,
            remote=True,
            travel=True,
            message='Test message'
        )

    def test_candidate_creation_and_str(self):
        self.assertTrue(isinstance(self.candidate, Candidate))
        self.assertEqual(self.candidate.__str__(), 'John Doe')

    def test_candidate_get_absolute_url(self):
        url = reverse('candidate', args=[self.candidate.id])
        self.assertEqual(self.candidate.get_absolute_url(), url)

    def test_candidate_clean_method(self):
        self.candidate.firstname = 'john'
        self.candidate.lastname = 'doe'
        self.candidate.clean()
        self.assertEqual(self.candidate.firstname, 'John')
        self.assertEqual(self.candidate.lastname, 'Doe')

    def test_candidate_fullname_method(self):
        self.assertEqual(self.candidate.fullname(), 'John Doe')

    def test_candidate_age_method(self):
        # calculate expected age based on current date
        today = datetime.date.today()
        expected_age = today.year - self.candidate.birth_date.year - ((today.month, today.day) < (self.candidate.birth_date.month, self.candidate.birth_date.day))

        # verify that age method returns expected age
        self.assertEqual(self.candidate.age(), expected_age)
