# core/forms.py
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

    # Honeypot field — should remain empty
    hp_field = forms.CharField(required=False, widget=forms.HiddenInput)
    
    def clean_hp_field(self):
        data = self.cleaned_data['hp_field']
        if data:
            raise forms.ValidationError("Bot detected!")
        return data