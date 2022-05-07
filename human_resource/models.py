from django.db import models


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
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=PENDING)
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.person
