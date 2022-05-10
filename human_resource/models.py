from django.db import models
from django.utils.html import format_html


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
