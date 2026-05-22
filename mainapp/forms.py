from django import forms
from .models import Enquiry

class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = '__all__'
        widgets = {
            "name" : forms.TextInput(attrs={"class" : "form-control"}),
            "email" : forms.EmailInput(attrs={"class" : "form-control"}),
            "contactno" : forms.NumberInput(attrs={"class" : "form-control"}),
            "subject" : forms.TextInput(attrs={"class" : "form-control"}),
            "message" : forms.Textarea(attrs={"class" : "form-control","rows" : "4"}),
        }