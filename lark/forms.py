from django import forms
from django.contrib.auth.models import User

from lark.models import Language

class CodeForm(forms.Form):
	code = forms.FileField(
			label='Select a file'
			)
        lang = forms.ChoiceField(choices=[(i, i) for i in Language.objects.all()])
