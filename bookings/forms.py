from django import forms
from django.utils import timezone
from bookings.models import BookingRequest, ServicePackage


class BookingRequestForm(forms.ModelForm):
    class Meta:
        model = BookingRequest
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone',
            'city',
            'heard_from',
            'event_date',
            'package',
            'message'
        ]
        widgets = {
            'event_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),
            'message': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder': 'Please tell us more about your event (at least 10 characters)...'
                }
            ),
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'Your first name'
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Your last name'
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'example@mail.com'
                }
            ),
            'phone': forms.TextInput(
                attrs={
                    'placeholder': '08XXXXXXXX'
                }
            ),
            'city': forms.TextInput(
                attrs={
                    'placeholder': 'Your city'
                }
            ),
            'package': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        required_by_validation = {'phone', 'city', 'message', 'package'}
        for name in required_by_validation:
            if name in self.fields:
                self.fields[name].required = True

    def clean_event_date(self):
        date = self.cleaned_data.get('event_date')
        if date and date < timezone.now().date():
            raise forms.ValidationError('You cannot select a date in the past.')
        return date

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if not message.strip():
            raise forms.ValidationError('Message cannot be empty.')
        if len(message) < 10:
            raise forms.ValidationError('Please provide a bit more details (at least 10 characters).')
        return message

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.strip():
            raise forms.ValidationError('Phone number cannot be empty.')
        if len(phone) < 10:
            raise forms.ValidationError('Phone number must be at least 10 digits.')
        return phone

    def clean_city(self):
        city = self.cleaned_data.get('city')
        if not city.strip():
            raise forms.ValidationError('City cannot be empty.')
        return city

    def clean_package(self):
        package = self.cleaned_data.get('package')
        if not package:
            raise forms.ValidationError('Please select a package.')
        return package


class ServicePackageForm(forms.ModelForm):
    class Meta:
        model = ServicePackage
        fields = ['name', 'category', 'price', 'duration_hours', 'max_photos_included', 'description', 'is_active']

        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control bg-light text-white border-secondary',
                    'placeholder': 'Package name'
                }
            ),
            'category': forms.Select(
                attrs={
                    'class': 'form-select bg-light text-white border-secondary',
                    'placeholder': 'Select category'
                }
            ),
            'price': forms.NumberInput(
                attrs={
                    'class': 'form-control bg-light text-white border-secondary',
                    'placeholder': 'Price'
                }
            ),
            'duration_hours': forms.NumberInput(
                attrs={
                    'class': 'form-control bg-light text-white border-secondary',
                    'placeholder': 'Duration in hours'
                }
            ),
            'max_photos_included': forms.NumberInput(
                attrs={
                    'class': 'form-control bg-dark text-white border-secondary',
                    'placeholder': 'Max photos included'
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control bg-light text-white border-secondary',
                    'rows': 3,
                    'placeholder': 'Package description'
                }
            ),
            'is_active': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input'
                }
            ),
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is None:
            raise forms.ValidationError("Price is required.")
        if price <= 0:
            raise forms.ValidationError("Price must be greater than 0.")
        return price

    def clean_duration_hours(self):
        duration_hours = self.cleaned_data.get('duration_hours')
        if duration_hours is None:
            raise forms.ValidationError("Duration is required.")
        if duration_hours <= 0:
            raise forms.ValidationError("Duration must be greater than 0.")
        return duration_hours

    def clean_max_photos_included(self):
        max_photos_included = self.cleaned_data.get('max_photos_included')
        if max_photos_included is None:
            raise forms.ValidationError("Max photos included is required.")
        if max_photos_included <= 0:
            raise forms.ValidationError("Max photos included must be greater than 0.")
        return max_photos_included

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if not description.strip():
            raise forms.ValidationError("Description cannot be empty.")
        return description

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name.strip():
            raise forms.ValidationError("Name cannot be empty.")
        return name

    def clean_category(self):
        category = self.cleaned_data.get('category')
        if not category:
            raise forms.ValidationError("Category is required.")
        return category