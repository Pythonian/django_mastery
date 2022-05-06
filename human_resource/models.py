from django.db import models


class RegisteredEmail(models.Model):
    """ Class to track and prevent duplicated email. """
    email = models.CharField(max_length=40)

    def __str__(self):
        return self.email
