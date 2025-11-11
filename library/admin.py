from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from library.models import Book, User


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    fieldsets = (  # Специальный параметр, который поможет задавать группы полей. при обновлении и Выделять определённый поля прям в группки
        (None, {'fields': ('username', 'password')}), # безымянная группа, базовые стартовые поля пароля и имени
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'birth_date', 'gender', 'role', 'age')}),  # Группа полей "Персональная информация"
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),  # Группа полей "Разрешения"
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),  # Группа полей "Важные даты"
    )
    add_fieldsets = (  # а это будет отдельная группа тех полей, которые должны быть при СОЗДАНИИ
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'gender', 'is_staff')  # Список полей на отображение
    search_fields = ('username', 'first_name', 'last_name', 'email')  # список полей на поиск
    ordering = ('username',)  # порядок оторбажения данных (сортировка)


admin.site.register(Book)
admin.site.unregister(Group)
admin.site.register(Group)
