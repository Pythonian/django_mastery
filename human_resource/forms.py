from django import forms
from .models import Message


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
