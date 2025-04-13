from django.shortcuts import render
from functools import wraps

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        
        referer = request.META.get('HTTP_REFERER', '/')
        return render(request, 'errors/permission_denied.html', {
            'referer': referer,
        }, status=403)

    return _wrapped_view
