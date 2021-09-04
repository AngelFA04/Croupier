from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from organizers.forms import SignupForm

# from django.views.generic import TemplateView


def signup(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = SignupForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # Save form date into database
            form.save()
            # breakpoint()
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(username=email, password=password)
            login(request, user)

            # redirect to a new URL:
            return HttpResponseRedirect("/organizers/welcome")
    # if a GET (or any other method) we'll create a blank form
    else:
        form = SignupForm()
    return render(request, "organizers/signup.html", {"form": form})


# TODO Add validation to only registered users can access this page
@login_required(login_url="/users/login")
def welcome(request):
    """
    View to show the welcome message to only the registered users and
    to give her options to continue with the registration process or
    to start creating a raffle
    """
    # TODO Pass in the context if the user is already logged in
    context = {}
    return render(request, "organizers/welcome.html", context=context)
