from django import forms
from django.contrib.auth.models import Group, Permission
from accounts.models import Account
from events.models import Event, Category, EventTicket



class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ("user","date_of_birth","telefon",
                  "newsletter","account_type",
                  "email_validated", )
        


class TokenForm(forms.Form):
    user = forms.IntegerField()


class GroupFormCreation(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'permissions']