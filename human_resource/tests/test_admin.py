from datetime import date

from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory, TestCase
from django.urls import reverse

from ..admin import CandidateAdmin
from ..models import Candidate


class CandidateAdminTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.site = AdminSite()
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
        self.candidate_pending = Candidate.objects.create(
            status='P',
            firstname='John',
            lastname='Pending',
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
        self.candidate_disapproved = Candidate.objects.create(
            status='D',
            firstname='John',
            lastname='Disapproved',
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
        self.admin_user = CandidateAdmin(Candidate, admin.site)

    def test_change_view_redirect(self):
        """Test that after saving a candidate, user is redirected to the candidate detail page."""
        request = self.factory.post(reverse('admin:human_resource_candidate_change', args=[self.candidate.id]), data={
            'firstname': 'John',
            'lastname': 'Doe',
            'email': 'johndoe@example.com',
            'status': 'A'
        })
        request.user = None
        response = self.admin_user.change_view(request, str(self.candidate.id))
        self.assertEqual(response['Location'], self.candidate.get_absolute_url())

    def test_get_fields(self):
        request = self.factory.get('/admin/candidate/')
        fields = self.admin_user.get_fields(request, self.candidate)
        self.assertNotIn('firstname', fields)
        self.assertNotIn('lastname', fields)

    def test_job_status_approved(self):
        status_text = self.admin_user.job_status(self.candidate)
        self.assertIn('color: #28a745', status_text)
        self.assertIn('Approved', status_text)

    def test_job_status_pending(self):
        status_text = self.admin_user.job_status(self.candidate_pending)
        self.assertIn('color: #fea95e', status_text)
        self.assertIn('Pending', status_text)

    def test_job_status_disapproved(self):
        status_text = self.admin_user.job_status(self.candidate_disapproved)
        self.assertIn('color: red', status_text)
        self.assertIn('Disapproved', status_text)

    def test_list_display(self):
        list_display = self.admin_user.get_list_display(None)
        self.assertEqual(list_display, ['__str__', 'email', 'job', 'created', 'job_status', '_'])

    def test_boolean(self):
        value = self.admin_user._(self.candidate)
        expected_value = True
        self.assertEqual(value, expected_value)

        value_pending = self.admin_user._(self.candidate_pending)
        expected_value_pending = None
        self.assertEqual(value_pending, expected_value_pending)

        value_disapproved = self.admin_user._(self.candidate_disapproved)
        expected_value_disapproved = False
        self.assertEqual(value_disapproved, expected_value_disapproved)
