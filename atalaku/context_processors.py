from atalaku import settings


def site_context(request):
    is_dashboard_allowed = False
    if request.user.is_authenticated:
        is_dashboard_allowed = request.user.has_perm('dashboard.can_view_dashboard')
    context = {
        'site_name' : settings.SITE_NAME,
        'meta_keywords': settings.META_KEYWORDS,
        'meta_description': settings.META_DESCRIPTION,
        'is_dashboard_allowed': is_dashboard_allowed,
        'redirect_to' : '/'
    }
    return context
    
    
