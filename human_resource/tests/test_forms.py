from django.test import TestCase

from ..forms import Lowercase, Uppercase, CandidateForm


class TestLowercaseAndUppercaseFields(TestCase):
    def test_lowercase_field(self):
        field = Lowercase()
        self.assertEqual(field.to_python("HELLO"), "hello")
        self.assertEqual(field.to_python("WORLD"), "world")
        self.assertEqual(field.to_python("MiXeD"), "mixed")

    def test_uppercase_field(self):
        field = Uppercase()
        self.assertEqual(field.to_python("hello"), "HELLO")
        self.assertEqual(field.to_python("world"), "WORLD")
        self.assertEqual(field.to_python("MiXeD"), "MIXED")


class TestCandidateForm(TestCase):

    def test_phonenumber_widget_attrs(self):
        form = CandidateForm()
        phonenumber_widget = form.fields['phonenumber'].widget
        self.assertEqual(phonenumber_widget.attrs['data-mask'], '9999-9999-999')
        self.assertEqual(phonenumber_widget.attrs['placeholder'], '0706-1234-567')

    def test_unrequired_fields(self):
        form = CandidateForm()
        for field in ['experience', 'employed', 'remote', 'travel', 'company', 'position', 'started_job', 'finished_job', 'about_job']:
            self.assertFalse(form.fields[field].required)
