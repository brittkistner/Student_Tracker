from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.shortcuts import render_to_response
from checkin.forms import EmailUserCreationForm, StudentCheckInForm
from checkin.models import CheckIn, Class


# ##############
# REGISTRATION #
###############

def register(request):
    if request.method == 'POST':
        form = EmailUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # text_content = 'Thank you for signing up for our website, {}'.format(user.username)
            # html_content = '<h2>Thanks {} {} for signing up!</h2> <div>You joined at {}.  I hope you enjoy using our site</div>'.format(user.first_name, user.last_name, user.date_joined)
            # msg = EmailMultiAlternatives("Welcome!", text_content, settings.DEFAULT_FROM_EMAIL, [user.email])
            # msg.attach_alternative(html_content, "text/html")
            # msg.send()
            new_user = authenticate(username=request.POST['username'],
                                    password=request.POST['password1'])
            login(request, new_user)
            return redirect("login")

    else:
        form = EmailUserCreationForm()

    return render(request, "registration/register.html", {
        'form': form,
    })


########
# HOME #
########

@login_required()
def home(request):
    if not request.user.is_student:
        classes = Class.objects.filter(teacher=request.user)
    else:
        classes = Class.objects.filter(student=request.user)
    data = {
        'classes': classes
    }
    return render(request, 'home.html', data)


# check in the students to class
# check in from request Post
@login_required()
def checkin(request):
    if request.user.is_student:
    #Check if student or teacher
        student_check_in_form = StudentCheckInForm(student=request.user)
        #Pass in student user to get classes for the particular student in form
        if request.method == "POST":
            student_check_in_form = StudentCheckInForm(request.POST)
            if student_check_in_form.is_valid():
                checkin = CheckIn.objects.create(
                    student=request.user,
                    class_name=Class.objects.get(
                        pk=int(student_check_in_form.cleaned_data['classes'])
                    )
                )
                if checkin:
                    return redirect('home')

    data = {'student_check_in_form': student_check_in_form}
    return render(request, 'checkin/checkin.html', data)

# class Class(models.Model):
#     name = models.CharField(max_length=50)
#     teacher = models.ForeignKey(UserProfile, related_name="classes_teacher")
#     student = models.ManyToManyField(UserProfile, related_name="classes_student")
#     class_start = models.DateTimeField()
#     class_end = models.DateTimeField()
#
#
# class CheckIn(models.Model):
#     student = models.ForeignKey(UserProfile, related_name="check_ins")
#     class_name = models.ForeignKey(Class, related_name="check_ins")
#     check_in_time = models.DateTimeField(auto_now_add=True)
