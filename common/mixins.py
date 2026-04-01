from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect


class PhotographerRequiredMixin(AccessMixin):
    """Mixin to ensure the user is authenticated and has photographer permissions."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        is_photographer = request.user.groups.filter(name='Photographers').exists()
        if not (is_photographer or request.user.is_superuser):
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('home')

        return super().dispatch(request, *args, **kwargs)