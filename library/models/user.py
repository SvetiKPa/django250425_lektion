from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from django.utils.translation.trans_null import gettext_lazy as _
from django.utils import timezone

from library.enums import Role, Gender


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=45, unique=True)
    email = models.EmailField(_('email address'), max_length=75,
                              unique=True)  # Вот эти _ -- это элиас функции gettext_lazy(). Так проще воспринимать. Функция помогает правильно отображать строковые значения, особенно при работающей интернационализации
    first_name = models.CharField(_("first name"), max_length=50)
    last_name = models.CharField(_("last name"), max_length=50)
    role = models.CharField(
        max_length=35,
        choices=Role.choices(),  # Ставим чойсес как генерируемый список с кортежами из нашего класса Енам
        default=Role.lib_member
    )
    gender = models.CharField(
        choices=Gender.choices()
    )
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=45, null=True, blank=True)
    age = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(6), MaxValueValidator(120)],
        null=True
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    libraries = models.ManyToManyField('Library', related_name='members', blank=True)

    objects = UserManager()  # это специальный Менеджер, через который мы будем делать запросы в будущем.

    USERNAME_FIELD = "username"  # указываем какое поле будет восприниматься как юзернейм при входе в систему
    REQUIRED_FIELDS = ["email", "role",
                       "age"]  # Указываем какие поля должны быть обязательными, помимо юзернейм и пароля (при создании суперпользователя)

    def __str__(self):
        return self.email

    class Meta:
        db_table = "user"
