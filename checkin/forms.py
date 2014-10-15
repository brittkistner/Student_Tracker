from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.forms import UserCreationForm
from django import forms
from models import UserProfile, Class


class EmailUserCreationForm(UserCreationForm):
    helper = FormHelper()
    helper.form_method="POST"
    helper.form_class = 'form-horizontal'
    helper.add_input(Submit('Register', 'Register', css_class='btn-default'))

    class Meta:
        model = UserProfile
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            UserProfile.objects.get(username=username)
        except UserProfile.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )


class StudentCheckInForm(forms.Form):
    classes = forms.ChoiceField(widget=forms.RadioSelect, choices=[])
    helper = FormHelper()
    helper.form_method = "POST"
    helper.form_class = 'form-horizontal'
    helper.add_input(Submit('Checkin', 'Checkin', css_class='btn-default'))

    # Initialize and populate the classes selections
    # Pass in student objects
    def __init__(self, student, *args, **kwargs):
        super(StudentCheckInForm, self).__init__(*args, **kwargs)
        self.fields['classes'].choices = [
            (classes.pk, classes.name)
            for classes in Class.objects.filter(student=student)
        ]



