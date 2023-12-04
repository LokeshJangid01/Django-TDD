from django import forms
from .models import Task

class NewTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'dscription',)

class UpdateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'dscription',)