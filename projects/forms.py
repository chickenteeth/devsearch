from dataclasses import field
from django.forms import ModelForm
from django import forms
from .models import Project

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'featured_image', 'description', 'demo_link', 'source_link', 'tags']
        # Use Widgets to change form fields in Django
        widgets = {
            'tags': forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        # Update attributes on specific fields
        # self.fields['title'].widget.attrs.update({'class': 'input', 'placeholder': 'Add Title'})

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})