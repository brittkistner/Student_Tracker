import json
from django.contrib.auth import authenticate, login
from django.core import serializers
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from checkin.forms import EmailUserCreationForm, StudentCheckInForm
from checkin.models import CheckIn, Class

# ##############
# REGISTRATION #
###############
from checkin.models import UserProfile, HelpMe


def register(request):
    if request.method == 'POST':
        form = EmailUserCreationForm(request.POST)
        if form.is_valid():
            # user = form.save() <<=== need this line for email but Pep8 complains about user not referenced....
            form.save()
            # text_content = 'Thank you for signing up for our website, {}'.format(user.username)
            # html_content = '<h2>Thanks {} {} for signing up!</h2>
            # <div>You joined at {}.  I hope you enjoy using our site</div>'
            # .format(user.first_name, user.last_name, user.date_joined)
            # msg = EmailMultiAlternatives("Welcome!", text_content, settings.DEFAULT_FROM_EMAIL, [user.email])
            # msg.attach_alternative(html_content, "text/html")
            # msg.send()
            new_user = authenticate(username=request.POST['username'],
                                    password=request.POST['password1'])
            login(request, new_user)
            return redirect("home")

    else:
        form = EmailUserCreationForm()

    return render(request, "registration/register.html", {
        'form': form,
    })


########
# HOME #
########

# @login_required()
def home(request):
    if not request.user.is_student:
        classes = Class.objects.filter(teacher=request.user)
    else:
        classes = Class.objects.filter(student=request.user)
    data = {
        'classes': classes
    }
    return render(request, 'home.html', data)


def helpme(request):
    assist_list = HelpMe.objects.all()
    data = {
        'user': request.user,
        'assist_list': assist_list,
    }
    return render_to_response('helpMe.html', data)


def new_helpme(request):
    assist_list = HelpMe.objects.all()
    data = {
        'user': request.user,
        'assist_list': assist_list,
    }
    return render_to_response('new_helpMe.html', data)
#########
# CLASS #
#########


def add_help(request, student_id):
    student_in_need = UserProfile.objects.get(pk=student_id)
    HelpMe.objects.create(student=student_in_need)
    return redirect("class")


@csrf_exempt
def ajax_add_help(request, student_id):
    data = json.loads(request.body)
    if data:
        student_in_need = UserProfile.objects.get(pk=student_id)
    HelpMe.objects.create(student=student_in_need)
    return redirect("class")


@csrf_exempt
def ajax_checkin(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if data and request.user.is_student:
            checkin = CheckIn.objects.create(
                    student=request.user,
                    class_name=Class.objects.get(
                        pk=int(data['class_id'])
                    )
                )
            if checkin:
                response = serializers.serialize('json', [checkin])
                return HttpResponse(response, content_type='application/json')


def helped(request, help_id):
    help_me = HelpMe.objects.get(pk=help_id)
    help_me.delete()
    return redirect("class")


# we can work on this later, but this is just a url any user can go to that would
# change the user's is_student boolean to False (making them a teacher)
def to_teacher(request):
    teacher = request.user
    teacher.is_student = False
    teacher.save()
    return redirect("home")


def to_student(request):
    student = request.user
    student.is_student = True
    student.save()
    return redirect("home")


# check in the students to class
# check in from request Post
@login_required()
def checkin(request):
    student_check_in_form = None
    if request.user.is_student:
        # Check if student or teacher
        student_check_in_form = StudentCheckInForm(student=request.user)
        # Pass in student user to get classes for the particular student in form
        if request.method == "POST":
            student_check_in_form = StudentCheckInForm(request.POST)
            if student_check_in_form.is_valid():
                student_check_in_form(request.user)
                # checkin=student_check_in_form.save(request.user)
                checkin = CheckIn.objects.create(
                    student=request.user,
                    class_name=Class.objects.get(
                        pk=int(student_check_in_form.cleaned_data['classes'])
                    )
                )
                if checkin:
                    return redirect('view-class')

    data = {'student_check_in_form': student_check_in_form}
    return render(request, 'checkin/checkin.html', data)


def view_class(request, class_id):
    klass = Class.objects.get(pk=class_id)
    checkins = CheckIn.objects.filter(class_name=klass)
    most_checkins = None
    if checkins:
        find_most_checkins = checkins.values('student').annotate(num_checkins=Count('student'))[0]
        most_checkins = UserProfile.objects.get(pk=find_most_checkins['student'])
    assist_list = HelpMe.objects.all()
    return render(request, 'class.html', {'klass': klass,
                                          'checkins': checkins,
                                          'mayor': most_checkins,
                                          'assist_list': assist_list,
                                        })


def klass(request):
    assist_list = HelpMe.objects.all()
    data = {
        'user': request.user,
        'assist_list': assist_list
    }
    return render(request, 'class.html', data)

# NEW AJAX CALLS


def add_student(request, student_id):
    student_in_need = UserProfile.objects.get(pk=student_id)
    HelpMe.objects.create(student=student_in_need)
    assist_list = HelpMe.objects.all()
    data = {
        'assist_list': assist_list,
        'user': request.user
    }
    return render(request, 'new_helpMe.html', data)


def remove_help(request, help_id):
    help_object = HelpMe.objects.get(pk=help_id)
    help_object.delete()
    assist_list = HelpMe.objects.all()
    data = {
        'assist_list': assist_list,
        'user': request.user
    }
    return render(request, 'new_helpMe.html', data)
