from django import forms
from myapp.models import Company

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'license_image_url', 'boss', 'id_card_front_url', 'id_card_back_url', 'address', 'description']
