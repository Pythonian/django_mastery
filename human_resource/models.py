from django.db import models
from datetime import date
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from multiselectfield import MultiSelectField


class RegisteredEmail(models.Model):
    """ Class to track and prevent duplicated email. """
    email = models.CharField(max_length=40)

    def __str__(self):  # pragma: no cover
        return self.email


class Support(models.Model):
    EMPLOYEE = 'E'
    CANDIDATE = 'C'
    PERSON_CHOICES = (
        (EMPLOYEE, 'Employee'),
        (CANDIDATE, 'Candidate'),
    )

    SUBJECT_CHOICES = (
        ('I lost my account', 'I lost my account'),
        ('My password does not work', 'My password does not work'),
        ('Update resume', 'Update resume'),
        ('Others', 'Others'),
    )

    DONE = 'D'
    PENDING = 'P'
    STATUS_CHOICES = (
        (DONE, 'Done'),
        (PENDING, 'Pending'),
    )

    terms = models.BooleanField("Took responsibility", default=False)
    message = models.TextField()
    person = models.CharField(max_length=10, choices=PERSON_CHOICES)
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES)
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default=PENDING)
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):  # pragma: no cover
        return self.person


class Message(models.Model):
    READ = 'R'
    PENDING = 'P'
    STATUS_CHOICES = (
        (READ, 'Read'),
        (PENDING, 'Pending'),
    )
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default=PENDING)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=30)
    subject = models.CharField(max_length=25)
    body = models.TextField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):  # pragma: no cover
        return self.name


class Vacancy(models.Model):
    frontend = models.PositiveIntegerField(default=0)
    backend = models.PositiveIntegerField(default=0)
    devops = models.PositiveIntegerField(default=0)
    design = models.PositiveIntegerField(default=0)
    timer = models.CharField(max_length=100)


class Candidate(models.Model):
    APPROVED = 'A'
    DISAPPROVED = 'D'
    PENDING = 'P'
    STATUS_CHOICES = (
        (APPROVED, 'Approved'),
        (DISAPPROVED, 'Disapproved'),
        (PENDING, 'Pending'))

    PERSONALITY_CHOICES = (
        ('I am outgoing', 'I am outgoing'),
        ('I am antisocial', 'I am antisocial'),
        ('I am serious', 'I am serious'))

    YES = 'Y'
    NO = 'N'
    SMOKER_CHOICES = (
        (YES, 'Yes'),
        (NO, 'No'))

    DATABASES = (
        ('PostgreSQL', 'PostgreSQL'),
        ('MySQL', 'MySQL'),
        ('Redis', 'Redis'),
        ('Cassandra', 'Cassandra'),
        ('Sqlite3', 'Sqlite3'),
        ('Oracle', 'Oracle'),
    )

    FRAMEWORKS = (
        ('Laravel', 'Laravel'),
        ('Angular', 'Angular'),
        ('Django', 'Django'),
        ('Vue', 'Vue'),
        ('Flask', 'Flask'),
        ('Others', 'Others'),
    )

    LANGUAGES = (
        ('Python', 'Python'),
        ('Javascript', 'Javascript'),
        ('Ruby', 'Ruby'),
        ('Go', 'Go'),
        ('Java', 'Java'),
        ('Haskell', 'Haskell'),
    )

    LIBRARIES = (
        ('jQuery', 'jQuery'),
        ('Bootstrap', 'Bootstrap'),
        ('Ajax', 'Ajax'),
        ('HTMX', 'HTMX'),
        ('AlpineJS', 'AlpineJS'),
        ('Tensorflow', 'Tensorflow'),
    )

    MOBILE = (
        ('React native', 'React native'),
        ('Kivy', 'Kivy'),
        ('Flutter', 'Flutter'),
        ('Dart', 'Dart'),
        ('Xamarin', 'Xamarin'),
        ('Ionic', 'Ionic'),
    )

    OTHERS = (
        ('UML', 'UML'),
        ('VScode', 'VScode'),
        ('Docker', 'Docker'),
        ('GIT', 'GIT'),
        ('GraphQL', 'GraphQL'),
        ('Linux', 'Linux'),
    )

    COURSE_STATUS_CHOICES = (
        ('', 'Select course status'),
        ('I am studying', 'I am studying'),
        ('I want to study course', 'I want to study course'),
        ('I have completed the course', 'I have completed the course'),
    )

    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )

    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default=PENDING)
    firstname = models.CharField(_('First name'), max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    birth_date = models.DateField()
    phonenumber = models.CharField(max_length=18)
    job = models.CharField(verbose_name='Job code', max_length=5)
    personality = models.CharField(
        max_length=50, choices=PERSONALITY_CHOICES, null=True)
    salary = models.CharField(verbose_name='Salary expectation', max_length=50)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    experience = models.BooleanField(null=True)
    smoker = models.CharField(max_length=1, choices=SMOKER_CHOICES, default="")
    file = models.FileField(upload_to='files')
    image = models.ImageField(upload_to='images', default='images/picture.jpg')
    note = models.TextField(blank=True)

    # Skills
    languages = MultiSelectField(choices=LANGUAGES, max_length=50)
    frameworks = MultiSelectField(choices=FRAMEWORKS, max_length=50)
    databases = MultiSelectField(choices=DATABASES, max_length=50)
    libraries = MultiSelectField(choices=LIBRARIES, max_length=50)
    mobile = MultiSelectField(choices=MOBILE, max_length=50)
    others = MultiSelectField(choices=OTHERS, max_length=50)

    # Education
    institution = models.CharField(max_length=50)
    course = models.CharField(max_length=50)
    started_course = models.DateField()
    finished_course = models.DateField(blank=True, null=True)
    course_description = models.TextField()
    course_status = models.CharField(
        max_length=50, choices=COURSE_STATUS_CHOICES)

    # Work history / Experience
    company = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    started_job = models.DateField(blank=True, null=True)
    finished_job = models.DateField(blank=True, null=True)
    about_job = models.TextField()
    employed = models.BooleanField(verbose_name='I am employed')
    remote = models.BooleanField(verbose_name='I agree to work remotely')
    travel = models.BooleanField(verbose_name='I am available for travel')

    created = models.DateTimeField(default=timezone.now)
    message = models.TextField(blank=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.firstname} {self.lastname}'

    def get_absolute_url(self):
        return reverse('candidate', args=[self.id])

    def clean(self):
        self.firstname = self.firstname.capitalize()
        self.lastname = self.lastname.capitalize()

    def fullname(self):
        return f'{self.firstname} {self.lastname}'

    def age(self):
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day)
                                                    < (self.birth_date.month,
                                                       self.birth_date.day))


class GroupChat(models.Model):
    candidate_email = models.CharField(max_length=200)
    user = models.CharField(max_length=50)
    chat = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):  # pragma: no cover
        return self.user
