import datetime
from time import sleep
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.test import TestCase, LiveServerTestCase
# from cards.forms import EmailUserCreationForm
# from cards.models import Card, Player, WarGame
# from cards.test_utils import run_pyflakes_for_package, run_pep8_for_package
# from cards.utils import create_deck
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import WebDriver
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
            # student=self.student,
            class_start=datetime.datetime.now(),
            class_end=datetime.datetime.now(),
        )
        self.check_in = CheckIn.objects.create(
            student=self.student,
            class_name=self.klass,
        )

    def test_user_profile_model_uicode(self):
        self.assertEqual(self.student.__unicode__(), 'student')

    def test_check_in_model_unicode(self):
        self.assertEqual(self.check_in.__unicode__(), 'class1')


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
# class FormTestCase(TestCase):
#     def test_clean_username_exception(self):
#         # Create a player so that this username we're testing is already taken
#         Player.objects.create_user(username='test-user')
#
#         # set up the form for testing
#         form = EmailUserCreationForm()
#         form.cleaned_data = {'username': 'test-user'}
#
#         # use a context manager to watch for the validation error being raised
#         with self.assertRaises(ValidationError):
#             form.clean_username()
#
#     def test_clean_username(self):
#         # Create a player so that this username we're testing is already taken
#         Player.objects.create_user(username='test-user')
#
#         # set up the form for testing
#         form = EmailUserCreationForm()
#         form.cleaned_data = {'username': 'test-user2'}
#
#         self.assertEqual(form.clean_username(), 'test-user2')


class SeleniumTests(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(SeleniumTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(SeleniumTests, cls).tearDownClass()

    def test_login(self):
        UserProfile.objects.create_user('user', 'superuser@test.com', 'pass')
        UserProfile.is_student = True
        # let's open the admin login page
        self.selenium.get("{}{}".format(self.live_server_url, reverse('home')))

        homepage_body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('Login/Register', homepage_body.text)

        self.selenium.find_element_by_id('modal_trigger').send_keys(Keys.RETURN)
        self.selenium.find_element_by_name('username').send_keys('user')
        password_input = self.selenium.find_element_by_name('password')
        password_input.send_keys('pass')

        password_input.send_keys(Keys.RETURN)
        sleep(1)

        logged_in_body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('Type of User Profile', logged_in_body.text)

    def test_checkin(self):
        pass

    def test_student_add_help(self):
        user = UserProfile.objects.create_user('student', 'superuser@test.com', 'pass')
        teacher = UserProfile.objects.create_user('teacher', 'superuser@test.com', 'teacher')
        UserProfile.is_student = True
        klass = Class.objects.create(
            name='class1',
            teacher=teacher,
            # student=self.student,
            class_start=datetime.datetime.now(),
            class_end=datetime.datetime.now(),
        )
        klass.student.add(user)
        # let's open the admin login page
        self.selenium.get("{}{}".format(self.live_server_url, reverse('home')))

        # sign in to the app
        self.selenium.find_element_by_id('modal_trigger').send_keys(Keys.RETURN)
        self.selenium.find_element_by_name('username').send_keys('student')
        password_input = self.selenium.find_element_by_name('password')
        password_input.send_keys('pass')
        password_input.send_keys(Keys.RETURN)
        sleep(1)

        # click on the class on front page
        self.selenium.find_element_by_link_text('class1').click()
        sleep(5)

        # click on the add to queue
        self.selenium.find_element_by_id('1').click()
        sleep(5)

        assit_list = self.selenium.find_element_by_class_name('assistList')
        self.assertIn('student', assit_list.text)

    def test_teacher_helped(self):
        pass


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
