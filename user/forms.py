from django.forms import ModelForm
from .models import auth

class authform(ModelForm):
    class Meta:
        model = auth
        fields = '__all__'
