from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from checkin.forms import EmailUserCreationForm

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

def home(request):
    data = {
        'user': request.user,
    }
    return render(request, 'home.html', data)


#########
# CLASS #
#########

# def klass(request):
#     return render(request, 'class.html')
#
# def klass2(request):
#     return render(request, 'class2.html')