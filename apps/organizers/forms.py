# Move
from django import forms
from django.contrib.auth.password_validation import validate_password
from organizers.models import OrganizerModel
from users.models import UserModel


class SignupForm(forms.Form):
    """
    Form for registering a new organizer user.
    """

    nickname = forms.CharField(
        label="Usuario", max_length=20, help_text="Máximo 20 caracteres", required=True
    )
    email = forms.EmailField(label="Correo", required=True)
    first_name = forms.CharField(label="Nombre", required=True)
    last_name = forms.CharField(label="Apellido", required=True)
    # TODO Add password validations
    password = forms.CharField(
        widget=forms.PasswordInput, label="Contraseña", required=True
    )
    password_validation = forms.CharField(
        widget=forms.PasswordInput, label="Confirmar contraseña", required=True
    )
    description = forms.CharField(
        widget=forms.Textarea,
        label="Descripción de usuario.",
        help_text="Campo opcional donde se puede indicar si se trata de una organización o de un particular, lugar de residencia, entre otros datos.",
        required=False,
    )

    class Meta:
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
            raise forms.ValidationError("El nombre de usuario ya está en uso")
        return nickname

    def clean_email(self):
        """
        Validate that the email is not already in use.
        """
        email = self.cleaned_data.get("email")
        if UserModel.objects.filter(email=email).exists():
            raise forms.ValidationError("La dirección de correo ya está en uso")
        return email

    def clean_password_validation(self):
        """
        Validate that the password and password_validation fields match.
        """
        password = self.data.dict().get("password")
        password_validation = self.data.dict().get("password_validation")
        if password != password_validation:
            raise forms.ValidationError("Las contraseñas no coinciden")
        try:
            validate_password(password)
        except forms.ValidationError as error:
            raise forms.ValidationError(error)

        return password_validation

    def clean(self):
        """Verify password confirmation match"""
        data = super().clean()
        if not data:
            return data
        return data

    def save(self):
        self.cleaned_data.pop("password_validation")
        nickname = self.cleaned_data.pop("nickname")
        description = self.cleaned_data.pop("description")
        user = UserModel.objects.create_user(**self.cleaned_data)
        organizer = OrganizerModel(
            user=user, nickname=nickname, description=description
        )
        organizer.save()
        return organizer
