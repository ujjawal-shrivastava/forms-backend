from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django import forms

class UserCreationForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('email',)
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances
    add_form = UserCreationForm
    list_display = ("email",'name','added','updated')
    list_display_links=("email",)
    list_filter = ('userid',)
    search_fields = ['name', 'email']
    ordering = ("userid",)

    fieldsets = (
        (None, {'fields': ('userid', 'email','name', 'password','verified','is_superuser', 'is_staff', 'is_active')}),
        )

    readonly_fields = ('userid',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','name', 'password','verified', 'is_superuser', 'is_staff', 'is_active')}
            ),
        )

    filter_horizontal = ()
admin.site.register(get_user_model(), CustomUserAdmin)