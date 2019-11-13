from events.models import Event, Category

def event_context(request):
    context = {
        'events' : None,
        'favorite_events': None,
        'categories' : Category.objects.all()
    }
    if request.user.is_authenticated:
        if hasattr(request.user, 'registered_events'):
            context['events'] = request.user.registered_events.all()
        if hasattr(request.user, 'favorite_events'):
            context['favorite_events'] = request.user.favorite_events.all()
    return context
    
    
