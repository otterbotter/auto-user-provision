from django import forms
from django.core.exceptions import ValidationError

from auto_user_provision.models import RotatingProvisionKey


class ProvisionKeyInputForm(forms.Form):
    key = forms.CharField()

    def clean_key(self):
        key = self.cleaned_data['key']

        try:
            key_model = RotatingProvisionKey.objects.get(key=key)
        except RotatingProvisionKey.DoesNotExist:
            raise ValidationError('No matching key was found', code='not_found')
        except ValueError:
            raise ValidationError('Invalid key format', code='invalid_format')

        return key
