import datetime
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.forms import EmailField
from django.test import TestCase
from checkin.forms import EmailUserCreationForm
from checkin.models import UserProfile, Class, CheckIn
from checkin.test_utils import run_pyflakes_for_package, run_pep8_for_package


class ModelTestCase(TestCase):

    def setUp(self):
        self.student = UserProfile.objects.create(
            username="student",
            password="student",
            is_student=True,
        )
        self.teacher = UserProfile.objects.create(
            username="teacher",
            password="teacher",
            is_student=True,
        )
        self.klass = Class.objects.create(
            name='class1',
            teacher=self.teacher,
            class_start=datetime.datetime.now(),
            class_end=datetime.datetime.now(),
        )
        self.check_in = CheckIn.objects.create(
            student=self.student,
            class_name=self.klass,
        )

    def test_user_profile_model_unicode(self):
        self.assertEqual(self.student.__unicode__(), 'student')

    def test_check_in_model_unicode(self):
        self.assertEqual(self.check_in.__unicode__(), 'class1')

    def test_class_model_unicode(self):
        self.assertEqual(self.klass.__unicode__(), 'class1')


class FormTestCase(TestCase):
    def test_clean_username_exception(self):
        # Create a player so that this username we're testing is already taken
        UserProfile.objects.create_user(username='test-user')

        # set up the form for testing
        form = EmailUserCreationForm()
        form.cleaned_data = {'username': 'test-user'}

        # use a context manager to watch for the validation error being raised
        with self.assertRaises(ValidationError):
            form.clean_username()

    def test_clean_username(self):
        form = EmailUserCreationForm()
        form.cleaned_data = {
            'username': 'test-user'
        }
        self.assertTrue(form.clean_username() == 'test-user')
        # use a context manager to watch for the validation error being raised
        self.assertFieldOutput(EmailField, {'a@a.com': 'a@a.com'}, {'aaa': [u'Enter a valid email address.']})

#
# class ViewTestCase(TestCase):
#     def test_home_page(self):
#         response = self.client.get(reverse('home'))
#         self.assertIn('<p>Suit: spade, Rank: two</p>', response.content)
#         self.assertEqual(response.context['cards'].count(), 52)
#
#     def test_faq_page(self):
#         response = self.client.get(reverse('faq'))
#         self.assertIn('<p>Q: Can I win real money on this website?</p>\n    <p>A: Nope, this is not real, sorry.</p>',
#                       response.content)
#
#     def test_register_page(self):
#         username = 'new-user'
#         data = {
#             'username': username,
#             'email': 'test@test.com',
#             'password1': 'test',
#             'password2': 'test'
#         }
#         response = self.client.post(reverse('register'), data)
#
#         # Check this user was created in the database
#         self.assertTrue(Player.objects.filter(username=username).exists())
#
#         # Check it's a redirect to the profile page
#         self.assertIsInstance(response, HttpResponseRedirect)
#         # does the url location end with profile (cards.com/profile)
#         self.assertTrue(response.get('location').endswith(reverse('profile')))
#
#     def login_page(self):
#         username = 'new-user'
#         data = {
#             'username': username,
#             'password': 'password'
#         }
#         response = self.client.post(reverse('login'), data)
#
#         # Check it's a redirect to the profile page
#         self.assertIsInstance(response, HttpResponseRedirect)
#         # does the url location end with profile (cards.com/profile)
#         self.assertTrue(response.get('location').endswith(reverse('profile')))
#
#     def test_profile_page(self):
#         # Create user and log them in
#         password = 'passsword'
#         user = Player.objects.create_user(username='test-user', email='test@test.com', password=password)
#         self.client.login(username=user.username, password=password)
#
#         # Set up some war game entries
#         self.create_war_game(user)
#         self.create_war_game(user, WarGame.WIN)
#
#         # Make the url call and check the html and games queryset length
#         response = self.client.get(reverse('profile'))
#         self.assertInHTML('<p>Your email address is {}</p>'.format(user.email), response.content)
#         self.assertEqual(len(response.context['games']), 2)

class SyntaxTest(TestCase):
    def test_syntax(self):
        """
        Run pyflakes/pep8 across the code base to check for potential errors.
        """
        packages = ['checkin']
        warnings = []
        # Eventually should use flake8 instead so we can ignore specific lines via a comment
        for package in packages:
            warnings.extend(run_pyflakes_for_package(package, extra_ignore=("_settings",)))
            warnings.extend(run_pep8_for_package(package, extra_ignore=("_settings",)))
        if warnings:
            self.fail("{0} Syntax warnings!\n\n{1}".format(len(warnings), "\n".join(warnings)))
