from django import forms


class MixinForm():

    def clean_cover_image(self):
        cover_image = self.cleaned_data.get('cover_image')

        if not cover_image or not hasattr(cover_image, 'content_type'):
            return cover_image


        valid_types = ['image/jpeg', 'image/png', 'image/webp']
        if cover_image.content_type not in valid_types:
            raise forms.ValidationError('Only JPEG, PNG, and WebP images are allowed.')

        max_size = 5 * 1024 * 1024  # 5MB
        if cover_image.size > max_size:
            raise forms.ValidationError(f'Cover image file size must be under 5MB.')

        return cover_image