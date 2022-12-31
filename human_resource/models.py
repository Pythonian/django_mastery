from email.policy import default
from django.db import models
from django.utils.html import format_html
from datetime import date

from multiselectfield import MultiSelectField


class RegisteredEmail(models.Model):
    """ Class to track and prevent duplicated email. """
    email = models.CharField(max_length=40)

    def __str__(self):
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

    def __str__(self):
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

    def __str__(self):
        return self.name

    def report(self):
        """
        Function to color the status text.
        """
        if self.status == self.READ:
            color = '#28a745'
        else:
            color = 'red'
        return format_html(
            f"<span style='color: {color}'>{self.status}</span>")
    report.allow_tags = True


class Vacancy(models.Model):
    frontend = models.PositiveIntegerField(default=0)
    backend = models.PositiveIntegerField(default=0)
    devops = models.PositiveIntegerField(default=0)
    design = models.PositiveIntegerField(default=0)
    timer = models.CharField(max_length=100)


class Waiting(models.Model):
    JOB = (
        ('Frontend', 'Frontend'),
        ('Backend', 'Backend'),
    )

    job = models.CharField(max_length=100, choices=JOB)
    email = models.EmailField(max_length=100)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    resume = models.FileField(upload_to='resume')
    company_note = models.TextField(blank=True)

    def __str__(self):
        return self.job


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

    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=PENDING)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    # age = models.CharField(max_length=3)
    birth_date = models.DateField()
    phonenumber = models.CharField(max_length=18)
    job = models.CharField(verbose_name='Job code', max_length=5)
    personality = models.CharField(max_length=50, choices=PERSONALITY_CHOICES, null=True)
    salary = models.CharField(verbose_name='Salary expectation', max_length=50)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    experience = models.BooleanField(null=True)
    smoker = models.CharField(max_length=1, choices=SMOKER_CHOICES, default="")
    message = models.TextField() # Professional summary
    file = models.FileField(upload_to='files')
    image = models.ImageField(upload_to='images')
    note = models.TextField(blank=True)
    # address/location; certifications; interests; Languages; social media profiles
    
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
    course_status = models.CharField(max_length=50, choices=COURSE_STATUS_CHOICES)

    # Work history / Experience
    # If finished date is not provided, then it should be marked as 'Current'
    company = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    started_job = models.DateField(blank=True, null=True)
    finished_job = models.DateField(blank=True, null=True)
    about_job = models.TextField()
    employed = models.BooleanField(verbose_name='I am employed')
    remote = models.BooleanField(verbose_name='I agree to work remotely')
    travel = models.BooleanField(verbose_name='I am available for travel')
    
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.firstname} {self.lastname}'

    def clean(self):
        self.firstname = self.firstname.capitalize()
        self.lastname = self.lastname.capitalize()

    def age(self):
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))


# from django.db import models
# from django.utils.translation import gettext_lazy as _
# from django.contrib.auth.models import AbstractUser, BaseUserManager
# from django.db.models.signals import post_save
# from django.dispatch import receiver


# class User(AbstractUser):
    # class Role(models.TextChoices):
    #     ADMIN = 'ADMIN', 'Admin'
    #     COMPANY = 'COMPANY', 'Company'
    #     EMPLOYEE = 'EMPLOYEE', 'Employee'

    # base_role = Role.COMPANY

    # role = models.CharField(_('Role'), max_length=50, choices=Role.choices)

    # is_company = models.BooleanField(default=False)
    # is_employee = models.BooleanField(default=False)

    # def save(self, *args, **kwargs):
    #     if not self.pk:
    #         self.role = self.base_role
    #         return super().save(*args, **kwargs)


# class EmployeeManager(BaseUserManager):
#     """Return only users with the Employee role."""
#     def get_queryset(self, *args, **kwargs):
#         results = super().get_queryset(*args, **kwargs)
#         return results.filter(role=User.Role.EMPLOYEE)

# class EmployeeManager(models.Manager):
#     def get_queryset(self, *args, **kwargs):
#         return super().get_queryset(*args, **kwargs).filter(role=User.Role.EMPLOYEE)


# class Employee(User):
#     # Employee.objects.create(username='user', email='a@a.com')
#     base_role = User.Role.EMPLOYEE
#     employee = EmployeeManager()
#     objects = EmployeeManager()

#     class Meta:
#         proxy = True

    # def save(self, *args, **kwargs):
    #     if not self.pk:
    #         self.role = User.Role.EMPLOYEE
    #     return super().save(*args, **kwargs)


# class EmployeeProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     about = models.TextField(null=True, blank=True)


# @receiver(post_save, sender=Employee)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created and instance.role == 'EMPLOYEE':
#         EmployeeProfile.objects.create(user=instance)
