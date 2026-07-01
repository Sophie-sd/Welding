from django import forms

from .models import QuoteRequest, Service


class QuoteForm(forms.ModelForm):
    website = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = QuoteRequest
        fields = ('name', 'phone', 'email', 'service', 'message', 'privacy_accepted')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'autocomplete': 'name',
                'maxlength': '80',
                'placeholder': 'John Smith',
                'data-mask': 'name',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-input',
                'autocomplete': 'tel',
                'inputmode': 'tel',
                'placeholder': '+44 7700 900000',
                'data-mask': 'phone',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'autocomplete': 'email',
                'placeholder': 'name@company.co.uk',
                'data-mask': 'email',
            }),
            'service': forms.Select(attrs={'class': 'form-select'}),
            'message': forms.Textarea(attrs={'class': 'form-textarea'}),
            'privacy_accepted': forms.CheckboxInput(),
        }

    def __init__(self, *args, id_prefix='quote', compact=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['phone'].required = True
        self.fields['email'].required = False
        self.fields['service'].required = False
        self.fields['service'].queryset = Service.objects.filter(is_published=True)
        self.fields['service'].empty_label = 'Select a service'
        self.fields['privacy_accepted'].required = True

        rows = 2 if compact else 5
        self.fields['message'].widget.attrs['rows'] = rows

        field_map = {
            'name': f'{id_prefix}-name',
            'phone': f'{id_prefix}-phone',
            'email': f'{id_prefix}-email',
            'service': f'{id_prefix}-service',
            'message': f'{id_prefix}-message',
        }
        for field_name, element_id in field_map.items():
            self.fields[field_name].widget.attrs['id'] = element_id

    def clean_website(self):
        value = self.cleaned_data.get('website', '')
        if value:
            raise forms.ValidationError('Spam detected.')
        return value

    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        if len(name) < 2:
            raise forms.ValidationError('Please enter your full name.')
        return name

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        digits = ''.join(ch for ch in phone if ch.isdigit())
        if len(digits) < 12:
            raise forms.ValidationError('Please enter a valid UK phone number.')
        return phone.strip()
