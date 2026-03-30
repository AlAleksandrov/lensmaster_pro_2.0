from django import forms
from common.forms import MixinForm
from inventory.models import Equipment


class EquipmentForm(MixinForm, forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['brand', 'model', 'equipment_type', 'cover_image', 'specifications', 'purchase_date', 'notes', 'is_active']

        widgets = {
            'brand': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter brand name'
                }
            ),
            'model':forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter model name'
                }
            ),
            'equipment_type': forms.Select(
                attrs={
                    'class': 'form-select',
                }
            ),
            'cover_image': forms.FileInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Upload cover image'
                }
            ),
            'specifications': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Technical specs, sensor size, mount type...'
                }
            ),
            'purchase_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),
            'notes': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Internal notes, condition, storage location...'
                }
            ),
            'is_active': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input'
                }
            ),
        }

        labels = {
            'cover_image': 'Equipment Image',
            'purchase_date': 'Purchase Date',
            'is_active': 'Active (available for use)',
        }

        help_texts = {
            'specifications': 'Optional — technical details visible on the equipment page.',
        }
