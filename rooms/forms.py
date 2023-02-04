from django import forms

from .models import Room
from accounts.models import User


class AddRoomModelForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = (
            "topic",
            "name",
            "description",
        )
