# Move
from django import forms
from organizers.models import OrganizerModel
from users.models import UserModel


class SignupForm(forms.ModelForm):
    """
    Form for registering a new organizer user.
    """

    nickname = forms.CharField()
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_validation = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserModel
        fields = [
            "first_name",
            "last_name",
            "nickname",
            "password",
            "password_validation",
        ]

    def clean_nickname(self):
        """
        Validate that the nickname is unique
        """
        nickname = self.cleaned_data.get("nickname")
        if OrganizerModel.objects.filter(nickname=nickname).exists():
            raise forms.ValidationError("Nickname already in use")
        return nickname

    def clean_email(self):
        """
        Validate that the email is not already in use.
        """
        email = self.cleaned_data.get("email")
        if UserModel.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already in use")
        return email

    def clean(self):
        """Verify password confirmation match"""
        data = super().clean()

        password = data["password"]
        password_confirmation = data["password_validation"]

        if password != password_confirmation:
            raise forms.ValidationError("Passwords do not match")

        return data

    def save(self):
        self.cleaned_data.pop("password_validation")
        nickname = self.cleaned_data.pop("nickname")
        user = UserModel.objects.create_user(**self.cleaned_data)
        organizer = OrganizerModel(user=user, nickname=nickname)
        organizer.save()
        return organizer
