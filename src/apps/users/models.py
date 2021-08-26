from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy as _
from users.managers import UserManager

class UserModel(AbstractBaseUser, PermissionsMixin):
    """
    Model to store the user information.
    """
    email = models.EmailField(_("Email"), unique=True, blank=False, null=False)
    first_name = models.CharField(_("First name"), max_length=30, blank=False)
    last_name = models.CharField(_("Last name"), max_length=30, blank=False)
    date_joined = models.DateTimeField(_("Start date"), auto_now_add=True)
    phone = models.CharField(_("telefono"), max_length=25, null=True, blank=True)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    email_confirmed = models.BooleanField(
        default=False, verbose_name="Email confirmado"
    )
    is_staff = models.BooleanField(
        _("estatus del staff"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("activo"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table: str = "users"
        verbose_name: str = _("User")
        verbose_name_plural: str = _("Users")
        ordering = ["email", "first_name", "last_name"]

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self) -> str:
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    get_full_name.short_description = "Nombre completo"

    def get_short_name(self) -> str:
        """
        Returns the short name for the user.
        """
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)
