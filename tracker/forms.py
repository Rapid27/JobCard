from django import forms
from .models import JobCard

class JobCardForm(forms.ModelForm):
    class Meta:
        model = JobCard
        fields = ['location', 'work_required', 'reported_by', 'department_of_reporter', 'category']
