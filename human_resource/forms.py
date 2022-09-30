import datetime
from datetime import date
from django import forms
from django.core.validators import RegexValidator

from .models import Message, Candidate


class Lowercase(forms.CharField):
    """Convert values in a field to lowercase."""
    def to_python(self, value):
        return value.lower()


class Uppercase(forms.CharField):
    """Convert values in a field to uppercase."""
    def to_python(self, value):
        return value.upper()


class MessageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Message
        exclude = ['status']


class ReplyMessage(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

    subject = forms.CharField(max_length=60)
    cc = forms.EmailField(required=False)
    body = forms.CharField(label='', widget=forms.Textarea(
        attrs={'rows': '7', 'placeholder': 'Enter your message...'}))
    attachments = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'multiple': True}))


class CandidateForm(forms.ModelForm):

    firstname = forms.CharField(
        label='First Name', min_length=3, max_length=50,
        validators=[RegexValidator(r'^[a-zA-Z\s]*$', message='Only letters is allowed.')],
        error_messages={'required': 'Your firstname is required.'},
        widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    lastname = forms.CharField(
        label='Last Name', min_length=3, max_length=50,
        validators=[RegexValidator(r'^[a-zA-Z\s]*$', message='Only letters is allowed.')],
        widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    job = Uppercase(
        label='Job Code', min_length=5, max_length=5,
        widget=forms.TextInput(attrs={'placeholder': 'Ex: FE-22', 'data-mask': 'AA-00'}))
    email = Lowercase(
        label='Email address', min_length=8, max_length=50,
        validators=[RegexValidator(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$', message='Enter a valid email address.')],
        widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    # age = forms.CharField(
    #     label='Age', min_length=2, max_length=2,
    #     validators=[RegexValidator(r'^[0-9]*$', message='Only numbers are allowed.')],
    #     widget=forms.TextInput(attrs={'placeholder': 'Age'}))
    gender = forms.CharField(widget=forms.RadioSelect(choices=Candidate.GENDER_CHOICES))
    experience = forms.BooleanField(label='I have experience')
    message = forms.CharField(
        label='About you', min_length=50, max_length=1000,
        widget=forms.Textarea(attrs={'placeholder': 'Tell us about yourself.', 'rows': 5}))
    file = forms.FileField(label='Resume', widget=forms.ClearableFileInput(attrs={'accept': 'application/pdf, application/msword'}))
    image = forms.FileField(label='Photo', widget=forms.ClearableFileInput(attrs={'accept': 'image/png, image/jpeg'}))
    institution = forms.CharField(min_length=3, max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Name of the institution'}))
    course = forms.CharField(max_length=50, min_length=3, widget=forms.TextInput(attrs={'placeholder': 'Your college course'}))
    company = forms.CharField(label='Last company', max_length=50, min_length=3, widget=forms.TextInput(attrs={'placeholder': 'Name of the company'}))
    position = forms.CharField(max_length=50, min_length=3, widget=forms.TextInput(attrs={'placeholder': 'Position held'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Disable all input fields for a Candidate instance to prevent edits.
        # This can also be done in the views.py
        # instance = getattr(self, 'instance', None)
        # array_fields = ['firstname', 'lastname', 'email', 'job', 'salary',
        #                'experience', 'birth_date', 'phonenumber', 'message', 'file', 'personality',
        #                'smoker', 'libraries', 'databases', 'frameworks', 'mobile',
        #                'gender', 'others', 'languages',
        #                'institution', 'course', 'started_course', 'finished_course', 'course_description', 'course_status', 'company', 'position', 'started_job', 'finished_job', 'about_job', 'employed', 'remote', 'travel']
        # for field in array_fields:
        #     if instance and instance.pk:
        #         self.fields[field].disabled = True
        #         self.fields['file'].widget.attrs.update({'style': 'display:none'})
        #         self.fields['image'].widget.attrs.update({'style': 'display:none'})

        # Set a custom error message for a field
        self.fields['lastname'].error_messages.update({'required': 'Your lastname is required.'})
        
        # Update the attr of a field
        self.fields['phonenumber'].widget.attrs.update({'data-mask': '9999-9999-999', 'placeholder': '0706-1234-567'})

        # Pass in a default value for a select field before the choices
        self.fields['personality'].choices = [('', 'Select a personality'),] + list(self.fields['personality'].choices)[0:]

        unrequired_fields = ['experience', 'employed', 'remote', 'travel']
        for field in unrequired_fields:
            self.fields[field].required = False
            # self.fields[field].widget.attrs['autocomplete'] = 'off'

        custome_error_fields = ['job', 'email']
        for field in custome_error_fields:
            self.fields[field].error_messages.update({'required': 'This information is required.'})
        

    class Meta:
        model = Candidate
        fields = ['firstname', 'lastname', 'job', 'email', 'birth_date',
                  'phonenumber', 'message', 'personality', 'salary',
                  'gender', 'smoker', 'experience', 'file', 'others',
                  'frameworks', 'languages', 'databases', 'mobile', 'libraries',
                  'institution', 'course', 'started_course', 'finished_course',
                  'course_description', 'course_status', 'image', 'company',
                  'position', 'started_job', 'finished_job', 'about_job',
                  'employed', 'remote', 'travel']

        labels = {
            'salary': 'Salary scale',
            'smoker': 'Do you smoke?',
            'started_course': 'Started',
            'finished_course': 'Finished',
            'started_job': 'Started',
            'finished_job': 'Finished',
        }

        SALARY = (
            ('', 'Salary expectations (per month)'),
            ('Between ($3000 and $4000)', 'Between ($3000 and $4000)'),
            ('Between ($4000 and $6000)', 'Between ($4000 and $6000)'),
            ('Between ($6000 and $10000)', 'Between ($6000 and $10000)'),
        )

        widgets = {
            'course_description': forms.Textarea(attrs={'rows': 4}),
            'about_job': forms.Textarea(attrs={'rows': 4}),
            'salary': forms.Select(
                choices=SALARY, attrs={'class': 'form-control'}),
            'course_status': forms.Select(attrs={'class': 'form-control'}),
            'smoker': forms.RadioSelect(
                choices=Candidate.SMOKER_CHOICES,
                attrs={'class': 'btn-check'}),
            'birth_date': forms.DateInput(
                attrs={
                    'type': 'date', 
                    'onkeydown': 'return false',
                    'min': '1957-01-01',
                    'max': '2004-12-31'}),
            'started_course': forms.DateInput(
                attrs={
                    'type': 'date', 
                    'onkeydown': 'return false',
                    'min': '2000-01-01',
                    'max': '2022-12-31'}),
            'finished_course': forms.DateInput(
                attrs={
                    'type': 'date', 
                    'onkeydown': 'return false',
                    'min': '2000-01-01',
                    'max': '2022-12-31'}),
            'started_job': forms.DateInput(
                attrs={
                    'type': 'date', 
                    'onkeydown': 'return false',
                    'min': '2000-01-01',
                    'max': '2022-12-31'}),
            'finished_job': forms.DateInput(
                attrs={
                    'type': 'date', 
                    'onkeydown': 'return false',
                    'min': '2000-01-01',
                    'max': '2022-12-31'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Candidate.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(f'This email {email} has been registered.')
        return email

    def clean_job(self):
        job = self.cleaned_data.get('job')
        if job == 'FE-22' or job == 'BE-22' or job == 'FS-22':
            return job
        else:
            raise forms.ValidationError('Job code is invalid.')

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        now = date.today()
        age = (now.year - birth_date.year) - ((now.month, now.day) < (birth_date.month, birth_date.day))
        if age < 18 or age > 65:
            raise forms.ValidationError('Age must be between 18 and 65.')
        return birth_date

    def clean_phonenumber(self):
        phonenumber = self.cleaned_data.get('phonenumber')
        if len(phonenumber) != 13:
            raise forms.ValidationError('Your phonenumber is incomplete.')
        return phonenumber

    def clean_file(self):
        file = self.cleaned_data.get('file', False)
        EXT = ['pdf', 'doc', 'docx'] # Allowed extensions
        ext = str(file).split('.')[-1]
        ext_type = ext.lower()
        if ext_type not in EXT:
            raise forms.ValidationError('Only PDF and DOC files allowed.')
        if file.size > 2 * 1048476:
            raise forms.ValidationError('Maximum file size allowed is 2MB.')
        return file

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image.size > 2 * 1048476:
            raise forms.ValidationError('Maximum image size allowed is 2MB.')
        return image

    def clean_started_course(self):
        """Prevent future date"""
        started_course = self.cleaned_data['started_course']
        if started_course > datetime.date.today():
            raise forms.ValidationError('Future date is invalid.')
        return started_course

    def clean_finished_course(self):
        """Prevent future date"""
        finished_course = self.cleaned_data['finished_course']
        if finished_course is not None:
            if finished_course > datetime.date.today():
                raise forms.ValidationError('Future date is invalid.')
        return finished_course

    def clean_started_job(self):
        """Prevent future date"""
        started_job = self.cleaned_data['started_job']
        if started_job > datetime.date.today():
            raise forms.ValidationError('Future date is invalid.')
        return started_job

    def clean_finished_job(self):
        """Prevent future date"""
        finished_job = self.cleaned_data['finished_job']
        if finished_job > datetime.date.today():
            raise forms.ValidationError('Future date is invalid.')
        return finished_job
