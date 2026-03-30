from django import forms
from common.forms import MixinForm
from .models import Production, Category


class ProductionForm(MixinForm, forms.ModelForm):
    class Meta:
        model = Production
        fields = ['title', 'category', 'location', 'cover_image', 'date_created', 'short_description', 'description', 'is_featured', 'equipment']

        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control bg-light text-white border-secondary',
                    'placeholder': 'Enter project title'
                }
            ),
            'category': forms.Select(
                attrs={
                    'class': 'form-select bg-light text-white border-secondary'
                }
            ),
            'location': forms.TextInput(
                attrs={
                    'class': 'form-control bg-light text-white border-secondary',
                    'placeholder': 'e.g Sofia, Bulgaria'
                }
            ),
            'date_created': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control bg-light text-white border-secondary'
                }
            ),
            'short_description': forms.TextInput(
                attrs={
                    'class': 'form-control bg-light text-white border-secondary',
                    'placeholder': 'Brief summary...'
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control bg-light text-white border-secondary',
                    'rows': 5,
                    'placeholder': 'Detailed project description...'
                }
            ),
            'cover_image': forms.FileInput(
                attrs={
                    'class': 'form-control bg-dark text-white border-secondary'
                }
            ),
            'is_featured': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input'
                }
            ),
            'equipment': forms.CheckboxSelectMultiple(
                attrs={
                    'class': 'equipment-checkbox-list',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['title'].disabled = True
            self.fields['category'].disabled =True


class CategoryForm(MixinForm, forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'cover_image']

        labels = {
            'name': 'Category Name',
            'description': 'Description',
            'cover_image': 'Cover Image',
        }

        help_texts = {
            'name': 'Enter a unique category name',
            'description': 'Provide a brief description of the category',
            'cover_image': 'Upload a cover image for the category',
        }

        error_messages = {
            'required': 'Category name is required.',
            'unique': 'A category with this name already exists.',
            'max_length': 'Category name cannot exceed 100 characters.',
        }

        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control bg-light text-white border-secondary',
                    'placeholder': 'Enter category name'
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control bg-light text-white border-secondary',
                    'rows': 4,
                    'placeholder': 'Enter category description'
                }
            ),
            'cover_image': forms.FileInput(
                attrs={
                    'class': 'form-control bg-light text-white border-secondary',
                    'placeholder': 'Upload category cover image'
                }
            ),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if not name:
            raise forms.ValidationError('Category name cannot be blank or whitespace only.')

        qs = Category.objects.filter(name__iexact=name)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('A category with this name already exists (case-insensitive).')

        return name

