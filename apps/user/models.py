from collections.abc import Iterable
from django.utils import timezone

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager as BaseUserManager, Permission
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from .utils import user_get_permissions, user_has_module_perms, user_has_perm
from .validators import PhoneNumberValidator

# Create your models here.

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone, password, **extra_fields):
        """
        Create and save a user with the given phone, and password.
        """
        if not phone:
            raise ValueError("The given phone must be set")
        phone = self.normalize_phone(phone)

        user = self.model(phone=phone, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone, password, **extra_fields)

    @classmethod
    def normalize_phone(cls, phone):
        """
        Normalize the phone.
        """
        phone = phone or ""
        phone.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        if phone.startswith("+") and len(phone) == 13 and phone[1:].isdigit():
            return phone
        else:
            raise ValueError("The phone number is not valid")




class PermissionsMixin(models.Model):
    """
    Add the fields and methods necessary to support the Group and Permission
    models using the ModelBackend.
    """

    is_superuser = models.BooleanField(
        _("superuser status"),
        default=False,
        help_text=_(
            "Designates that this user has all permissions without "
            "explicitly assigning them."
        ),
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("user permissions"),
        blank=True,
        help_text=_("Specific permissions for this user."),
        related_name="user_set",
        related_query_name="user",
    )

    class Meta:
        abstract = True

    def get_user_permissions(self, obj=None):
        """
        Return a list of permission strings that this user has directly.
        Query all available auth backends. If an object is passed in,
        return only permissions matching this object.
        """
        return user_get_permissions(self, obj, "user")

    def get_all_permissions(self, obj=None):
        return user_get_permissions(self, obj, "all")

    def has_perm(self, perm, obj=None):
        """
        Return True if the user has the specified permission. Query all
        available auth backends, but return immediately if any backend returns
        True. Thus, a user who has permission from a single auth backend is
        assumed to have permission in general. If an object is provided, check
        permissions for that object.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        # Otherwise we need to check the backends.
        return user_has_perm(self, perm, obj)

    def has_perms(self, perm_list, obj=None):
        """
        Return True if the user has each of the specified permissions. If
        object is passed, check if the user has all required perms for it.
        """
        if not isinstance(perm_list, Iterable) or isinstance(perm_list, str):
            raise ValueError("perm_list must be an iterable of permissions.")
        return all(self.has_perm(perm, obj) for perm in perm_list)

    def has_module_perms(self, app_label):
        """
        Return True if the user has any permissions in the given app label.
        Use similar logic as has_perm(), above.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        return user_has_module_perms(self, app_label)


class User(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Phone and password are required. Other fields are optional.
    """

    phone_validator = PhoneNumberValidator()

    phone = models.CharField(
        _("phone"),
        max_length=13,
        unique=True,
        help_text=_(
            "Required. 13 characters. Digits and /+/ only."
        ),
        validators=[phone_validator],
        error_messages={
            "unique": _("A user with that phone already exists."),
        },
    )
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def clean(self):
        super().clean()
        self.phone = self.__class__.objects.normalize_phone(self.phone)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def user_sms(self, message, **kwargs):
        """Send an SMS to this user."""
        pass


class SMS():
    pass