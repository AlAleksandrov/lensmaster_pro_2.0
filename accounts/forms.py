from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from accounts.models import Profile

User = get_user_model()

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('A user with this email already exists.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('A user with this username already exists.')
        return username

class ProfileEditForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)
    email = forms.EmailField(required=False)

    class Meta:
        model = Profile
        fields = ('profile_picture', 'phone', 'bio', 'city')
        widgets = {
            'phone': forms.TextInput(
                attrs={
                    'class': 'form-control bg-dark text-white border-secondary',
                    'placeholder': '08XXXXXXXX',
                }
            ),
            'bio': forms.Textarea(
                attrs={
                    'class': 'form-control bg-dark text-white border-secondary',
                    'rows': 4,
                    'placeholder': 'Tell us about yourself...',
                }
            ),
            'city': forms.TextInput(
                attrs={
                    'class': 'form-control bg-dark text-white border-secondary',
                    'placeholder': 'Your city...',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        user.email = self.cleaned_data.get('email', '')
        if commit:
            user.save()
            profile.save()
        return profile