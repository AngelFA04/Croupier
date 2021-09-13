from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render


class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    """ Logout view. """

    template_name = "home.html"


class LoginView(auth_views.LoginView):
    """ Login view. """

    template_name = "users/login.html"
    redirect_field_name = "organizers/welcome.html"

    def post(self, request, *args, **kwargs):
        """
        Logs in the user if the credentials are correct.
        """
        data = request.POST.copy()
        data.update({"username": data.get("email")})
        form = AuthenticationForm(data=data)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


def privacy_view(request):
    """ View to show aprivacy advice.
    """
    return render(request, "users/privacy.html")