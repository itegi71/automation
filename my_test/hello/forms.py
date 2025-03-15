from django import forms 
from .models import USER

class DonoForm(forms.ModelForm):
    class Meta:
        model=USER
        fields=['name','age','id_number','gender','location', 'phone','center']

    



