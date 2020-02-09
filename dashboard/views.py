from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.http import Http404
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import F, Q
from rest_framework.authtoken.models import Token
from dashboard import forms
from events.models import Event, Category
from events.forms import EventForm, EventCancelForm, CategoryForm, EventSearchForm
from events.event_services import EventService, EventTicket
from atalaku import settings
from dashboard.permissions import get_view_permissions, PermissionManager
from django.utils.text import gettext_lazy as _
import logging


logger = logging.getLogger(__name__)


def dashboard_home(request):
    event_list = EventService.get_events()
    page_title = 'Events Home'
    template_name = 'dashboard/dashboard.html'
    page = request.GET.get('page', 1)
    paginator = Paginator(event_list, 10)
    logger.debug("Events requested page : %s", page)
    logger.debug("Events List - Number of Pages  : %s", paginator.num_pages)
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
        logger.debug("Events requested page not an Integer : %s", page)
    except EmptyPage:
        events = None
        logger.debug("Events requested page : %s - Empty page resulted -", page)
    context = {
        'events': events,
        'page_title': page_title
    }
    context.update(get_view_permissions(request.user))
    return render(request, template_name, context)

# Create your views here.
def events(request):
    event_list = EventService.get_events()
    page = request.GET.get('page', 1)
    paginator = Paginator(event_list, 1)
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)
    page_title = 'Events'
    template_name = 'dashboard/event_list.html'
    context = {
        'events': events,
        'page_title': page_title
    }
    context.update(get_view_permissions(request.user))
    return render(request, template_name, context)


def event_detail(request, event_uuid=None):
    event = EventService.get_event(event_uuid)
    template_name = 'dashboard/event_detail.html'
    context = {
        'event': event,
        'page_title': 'Event ' + event.name,
        'monitoring': EventService.event_summary(event_uuid)
    }
    context.update(get_view_permissions(request.user))
    return render(request, template_name, context)


@login_required
def event_update(request, event_uuid=None):
    event = get_object_or_404(Event, event_uuid=event_uuid)
    template_name = 'dashboard/event_update.html'
    if request.method == 'POST':
        event_data = EventService.extract_event_data_from_form(request)


        if event_data:
            logger.debug("Event Update  : Event date %s", event_data)
            event = EventService.event_update(event.pk, **event_data)
            messages.success(request, _("The Event has been updated"))
            return redirect('dashboard:event-detail', event_uuid=event_uuid)
        else :
            form = EventForm(request.POST, instance=event)
            logger.debug("Event Update  : Event data is None")
            messages.error(request, _("The Event could not be updated. Please check your submitted form"))
    else :
        form = EventForm(instance=event)
    context = {
        'event': event,
        'page_title': 'Event ' + event.name,
        'form' : form

    }
    context.update(get_view_permissions(request.user))
    return render(request, template_name, context)

@login_required
def event_create(request):
    template_name = 'dashboard/event_create.html'
    if request.method == 'POST':
        event_data = EventService.extract_event_data_from_form(request)
        if event_data:
            event, created = EventService.create_event(**event_data)
            if created:
                messages.success(request, _("The Event has been created"))
                return redirect('dashboard:event-detail', event_uuid=event.event_uuid)
            else :
                messages.error(request, _("The Event could not be created. An Event with the same information already exists"))
        else :
            messages.error(request, _("The Event could not be updated. Please check your submitted form"))

    context = {
        'page_title': _('Event Creation'),
        'form' : EventForm()

    }
    context.update(get_view_permissions(request.user))
    return render(request, template_name, context)

@login_required
def event_cancel(request, event_uuid=None):
    canceled = EventService.cancel_events(**{'event_uuid':event_uuid})
    if canceled:
        messages.success(request, _("The Event has been canceled"))
    else :
        messages.error(request, _("The Event could not be canceled"))
        logger.error("The Event with uuid %s could not be canceled", event_uuid)
    
    return redirect('dashboard:home')


@login_required
def event_delete(request, event_uuid=None):
    EventService.delete_event(event_uuid)
    
    return redirect('dashboard:home')

def event_search(request):
    template_name = "dashboard/search.html"
    page_title = _("Search")
    context = {
        'page_title' : page_title,
        'events' : None
    }
    context.update(get_view_permissions(request.user))
    if request.method == 'POST':
        form = EventSearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = EventService.event_search(query)
            context['events'] = results
            logger.debug("search query for Event finished")
    return render(request, template_name, context)


def event_category_events(request, category_slug=None):
    events, category  = EventService.get_category_events(category_slug)
    template_name = "dashboard/category_events.html"
    page_title = (category is not None and (category.name + " Events")) or _("Events")
    context = {
        'page_title' : page_title,
        'category': category,
        'events' : events
    }
    context.update(get_view_permissions(request.user))
    return render(request, template_name, context)


@login_required
def event_add_participant(request, event_uuid=None):
    event, added, message = EventService.add_event_participant(event_uuid, request.user)
    if added:
        messages.success(request, message)
    else:
        messages.error(request, message)
    return redirect('dashboard:event-detail', event_uuid=event.event_uuid)



@login_required
def event_remove_participant(request, event_uuid=None):
    event, removed, message = EventService.remove_event_participant(event_uuid, request.user)
    if removed:
        messages.success(request, message)
    else:
        messages.error(request, message)
    
    return redirect('dashboard:event-detail', event_uuid=event.event_uuid)


@login_required
def create_event_category(request):
    form = None
    if request.method == 'POST':
        form = CategoryForm(request.POST.copy())
        if form.is_valid():
            name = form.cleaned_data['name']
            category = EventService.create_category(name)
            if category:
                return redirect('dashboard:home')

    if request.method == 'GET':
        form = CategoryForm()
    template_name = 'dashboard/create_category.html'
    context = {
        'page_title' : _('Category Creation'),
        'form' : form,
    }
    context.update(get_view_permissions(request.user))
    return render(request, template_name, context)



@login_required
def event_tickets(request):
    ticket_list = EventTicket.get_events()
    page = request.GET.get('page', 1)
    paginator = Paginator(ticket_list, 1)
    try:
        tickets = paginator.page(page)
    except PageNotAnInteger:
        tickets = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)
    page_title = _('Tickets')
    template_name = 'dashboard/ticket_list.html'
    context = {
        'ticket': tickets,
        'page_title': page_title
    }
    context.update(get_view_permissions(request.user))
    return render(request, template_name, context)

@login_required
def ticket_detail(request, ticket_uuid=None):
    ticket = EventService.get_ticket(ticket_uuid)
    template_name = 'dashboard/ticket_detail.html'
    context = {
        'ticket': ticket,
        'event' : ticket.event,
        'page_title': _('Ticket')

    }
    context.update(get_view_permissions(request.user))
    return render(request, template_name, context)


@login_required
def users(request):
    username = request.user.username
    can_access_dashboard = PermissionManager.user_can_access_dashboard(request.user)
    if not can_access_dashboard:
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied
    can_view_user = PermissionManager.user_can_view_user(request.user)
    if not can_view_user:
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    context = {}
    queryset = User.objects.all()
    template_name = "dashboard/user_list.html"
    page_title = _("Dashboard Users") + " - " + settings.SITE_NAME
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, utils.PAGINATED_BY)
    try:
        list_set = paginator.page(page)
    except PageNotAnInteger:
        list_set = paginator.page(1)
    except EmptyPage:
        list_set = None
    context['page_title'] = page_title
    context['users'] = list_set
    context['can_access_dashboard'] = can_access_dashboard
    context.update(get_view_permissions(request.user))
    context['can_delete'] = PermissionManager.user_can_delete_user(request.user)
    context['can_update'] = PermissionManager.user_can_change_user(request.user)
    return render(request,template_name, context)

@login_required
def user_details(request, pk=None):
    username = request.user.username
    if not PermissionManager.user_can_access_dashboard(request.user):
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied
    if not PermissionManager.user_can_view_user(request.user):
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied
    context = {}
    #queryset = User.objects.select_related('account')
    user = get_object_or_404(User, pk=pk)
    template_name = "dashboard/user_detail.html"
    page_title = "User Details - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['user_instance'] = user
    context.update(get_view_permissions(request.user))
    context['can_delete'] = PermissionManager.user_can_delete_user(request.user)
    context['can_update'] = PermissionManager.user_can_change_user(request.user)
    return render(request,template_name, context)


@login_required
def generate_token(request):
    username = request.user.username
    can_view_dashboard = PermissionManager.user_can_access_dashboard(request.user)
    if not can_view_dashboard :
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied
    can_generate_token = PermissionManager.user_can_generate_token(request.user)
    if not can_generate_token:
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    template_name = "dashboard/token_generate.html"
    context = {
        'page_title' :_('User Token Generation') + ' - ' + settings.SITE_NAME,
        'can_generate_token' : can_generate_token,
    }
    if request.method == 'POST':
            form = forms.TokenForm(utils.get_postdata(request))
            if form.is_valid():
                user_id = form.cleaned_data['user']
                username = form.cleaned_data['username']
                user = User.objects.get(pk=user_id)
                t = Token.objects.get_or_create(user=user)
                context['generated_token'] = t
                messages.add_message(request, messages.SUCCESS, _('Token successfully generated for user {}'.format(username)) )
                return redirect('dashboard:home')
            else :
                messages.add_message(request, messages.ERROR, _('The submitted form is not valid') )
    else :
            context['form'] = forms.TokenForm()
            context.update(get_view_permissions(request.user))
        

    return render(request, template_name, context)



@login_required
def groups(request):
    username = request.user.username
    can_access_dashboard = PermissionManager.user_can_access_dashboard(request.user)
    if not can_access_dashboard:
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    can_view_group = PermissionManager.user_can_view_group(request.user)
    if not can_view_group:
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    context = {}
    
    #current_account = Account.objects.get(user=request.user)
    group_list = Group.objects.all()
    template_name = "dashboard/group_list.html"
    page_title = "Groups" + " - " + settings.SITE_NAME
    page = request.GET.get('page', 1)
    paginator = Paginator(group_list, utils.PAGINATED_BY)
    try:
        group_set = paginator.page(page)
    except PageNotAnInteger:
        group_set = paginator.page(1)
    except EmptyPage:
        group_set = None
    context['page_title'] = page_title
    context['groups'] = group_set
    context['can_delete_group'] = PermissionManager.user_can_delete_group(request.user)
    context['can_update_group'] = PermissionManager.user_can_change_group(request.user)
    context['can_add_group'] = PermissionManager.user_can_add_group(request.user)
    context.update(get_view_permissions(request.user))
    return render(request,template_name, context)

@login_required
def group_detail(request, pk=None):
    username = request.user.username
    can_access_dashboard = PermissionManager.user_can_access_dashboard(request.user)
    if not can_access_dashboard:
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    can_view_group = PermissionManager.user_can_view_group(request.user)
    if not can_view_group:
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    context = {}
    group = get_object_or_404(Group, pk=pk)
    template_name = "dashboard/group_detail.html"
    page_title = "Group Detail" + " - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['group'] = group
    context['can_delete_group'] = PermissionManager.user_can_delete_group(request.user)
    context['can_update_group'] = PermissionManager.user_can_change_group(request.user)
    context.update(get_view_permissions(request.user))
    return render(request,template_name, context)


@login_required
def group_update(request, pk=None):
    # TODO CHECK if the requesting User has the permission to update a group
    username = request.user.username
    can_access_dashboard = PermissionManager.user_can_access_dashboard(request.user)
    if not can_access_dashboard:
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    can_change_group = PermissionManager.user_can_change_group(request.user)
    if not can_change_group:
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    context = None
    page_title = 'Group Update'
    template_name = 'dashboard/group_update.html'
    group = get_object_or_404(Group, pk=pk)
    form = forms.GroupFormCreation(instance=group)
    group_users = group.user_set.all()
    available_users = User.objects.exclude(pk__in=group_users.values_list('pk'))
    permissions = group.permissions.all()
    available_permissions = Permission.objects.exclude(pk__in=permissions.values_list('pk'))
    if request.method == 'POST':
        form = forms.GroupFormCreation(request.POST, instance=group)
        users = request.POST.getlist('users')
        if form.is_valid() :
            logger.debug("Group form for update is valid")
            if form.has_changed():
                logger.debug("Group has changed")
            group = form.save()
            if users:
                logger.debug("adding %s users [%s] into the group", len(users), users)
                group.user_set.set(users)
            logger.debug("Saved users into the group %s",users)
            return redirect('dashboard:groups')
        else :
            logger.error("Error on editing the group. The form is invalid")
    
    context = {
            'page_title' : page_title,
            'form': form,
            'group': group,
            'users' : group_users,
            'available_users' : available_users,
            'permissions': permissions,
            'available_permissions' : available_permissions,
            'can_change_group' : can_change_group
    }
    context.update(get_view_permissions(request.user))
    return render(request, template_name, context)


@login_required
def group_create(request):
    username = request.user.username
    can_access_dashboard = PermissionManager.user_can_access_dashboard(request.user)
    if not can_access_dashboard:
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    can_add_group = PermissionManager.user_can_add_group(request.user)
    if not can_add_group:
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    context = None
    page_title = 'Group Creation'
    template_name = 'dashboard/group_create.html'
    available_permissions = Permission.objects.all()
    available_users = User.objects.all()
    form = forms.GroupFormCreation()
    if request.method == 'POST':
        form = forms.GroupFormCreation(request.POST)
        users = request.POST.getlist('users')
        if form.is_valid():
            logger.debug("Group Create : Form is Valid")
            group_name = form.cleaned_data.get('name', None)
            logger.debug('Creating a Group with the name {}'.format(group_name))
            if not Group.objects.filter(name=group_name).exists():
                group = form.save()
                messages.success(request, "The Group has been succesfully created")
                if users:
                    group.user_set.set(users)
                    logger.debug("Added users into the group %s",users)
                else :
                    logger.debug("Group %s created without users", group_name)

                return redirect('dashboard:groups')
            else:
                msg = "A Group with the given name {} already exists".format(group_name)
                messages.error(request, msg)
                logger.error(msg)
            
        else :
            messages.error(request, "The Group could not be created. Please correct the form")
            logger.error("Error on creating new Group Errors : %s", form.errors)
    
    context = {
            'page_title' : page_title,
            'form': form,
            'available_users' : available_users,
            'available_permissions': available_permissions,
            'can_add_group' : can_add_group
    }
    context.update(get_view_permissions(request.user))
    return render(request, template_name, context)


@login_required
def group_delete(request, pk=None):
    # TODO Check if the user requesting the deletion has the Group Delete permission
    username = request.user.username
    can_access_dashboard = PermissionManager.user_can_access_dashboard(request.user)
    if not can_access_dashboard:
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    can_delete_group = PermissionManager.user_can_delete_group(request.user)
    if not can_delete_group:
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied
    try:
        group = Group.objects.get(pk=pk)
        name = group.name
        messages.add_message(request, messages.SUCCESS, 'Group {} has been deleted'.format(name))
        group.delete()
        logger.debug("Group {} deleted by User {}", name, request.user.username)
        
    except Group.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'Group could not be found. Group not deleted')
        logger.error("Group Delete : Group not found. Action requested by User {}",request.user.username)
        
    return redirect('dashboard:groups')


#######################################################
########            Permissions 

@login_required
def permissions(request):
    username = request.user.username
    can_access_dashboard = PermissionManager.user_can_access_dashboard(request.user)
    if not can_access_dashboard:
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied


    context = {}
    permission_list = Permission.objects.all()
    template_name = "dashboard/permission_list.html"
    page_title = "Permissions" + " - " + settings.SITE_NAME
    page = request.GET.get('page', 1)
    paginator = Paginator(permission_list, utils.PAGINATED_BY)
    try:
        permission_set = paginator.page(page)
    except PageNotAnInteger:
        permission_set = paginator.page(1)
    except EmptyPage:
        permission_set = None
    context['page_title'] = page_title
    context['permissions'] = permission_set
    context.update(get_view_permissions(request.user))
    return render(request,template_name, context)

@login_required
def permission_detail(request, pk=None):
    username = request.user.username
    can_access_dashboard = PermissionManager.user_can_access_dashboard(request.user)
    if not can_access_dashboard:
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    context = {}
    permission = get_object_or_404(Permission, pk=pk)
    template_name = "dashboard/permission_detail.html"
    page_title = "Permission Detail" + " - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['permission'] = permission
    context.update(get_view_permissions(request.user))
    return render(request,template_name, context)


@login_required
def permission_update(request, pk=None):
    # TODO CHECK if the requesting User has the permission to update a permission
    username = request.user.username
    can_access_dashboard = PermissionManager.user_can_access_dashboard(request.user)
    if not can_access_dashboard:
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    context = None
    page_title = 'Permission Update'
    template_name = 'dashboard/permission_update.html'
    permission = get_object_or_404(Permission, pk=pk)
    form = forms.GroupFormCreation(instance=permission)
    permission_users = permission.user_set.all()
    available_users = User.objects.exclude(pk__in=permission_users.values_list('pk'))

    if request.method == 'POST':
        form = forms.GroupFormCreation(request.POST, instance=permission)
        users = request.POST.getlist('users')
        if form.is_valid() :
            logger.debug("Permission form for update is valid")
            if form.has_changed():
                logger.debug("Permission has changed")
            permission = form.save()
            if users:
                logger.debug("adding %s users [%s] into the permission", len(users), users)
                permission.user_set.set(users)
            logger.debug("Added permissions to users %s",users)
            return redirect('dashboard:permissions')
        else :
            logger.error("Error on editing the perssion. The form is invalid")
    
    context = {
            'page_title' : page_title,
            'form': form,
            'users' : permission_users,
            'available_users' : available_users,
            'permission': permission
    }
    context.update(get_view_permissions(request.user))
    return render(request, template_name, context)


@login_required
def permission_create(request):
    username = request.user.username
    can_access_dashboard = PermissionManager.user_can_access_dashboard(request.user)
    if not can_access_dashboard:
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    context = None
    page_title = 'Permission Creation'
    template_name = 'dashboard/permission_create.html'
    available_groups = Group.objects.all()
    available_users = User.objects.all()
    form = forms.GroupFormCreation()
    if request.method == 'POST':
        form = forms.GroupFormCreation(request.POST)
        users = request.POST.getlist('users')
        if form.is_valid():
            logger.debug("Permission Create : Form is Valid")
            perm_name = form.cleaned_data.get('name', None)
            perm_codename = form.cleaned_data.get('codename', None)
            logger.debug('Creating a Permission with the name {}'.format(perm_name))
            if not Permission.objects.filter(Q(name=perm_name) | Q(codename=perm_codename)).exists():
                perm = form.save()
                messages.add_message(request, messages.SUCCESS, "The Permission has been succesfully created")
                if users:
                    perm.user_set.set(users)
                    logger.debug("Permission %s given to users  %s",perm_name, users)
                else :
                    logger.debug("Permission %s created without users", perm_name)

                return redirect('dashboard:permissions')
            else:
                msg = "A Permission with the given name {} already exists".format(perm_name)
                messages.add_message(request, messages.ERROR, msg)
                logger.error(msg)
            
        else :
            messages.add_message(request, messages.ERROR, "The Permission could not be created. Please correct the form")
            logger.error("Error on creating new Permission : %s", form.errors)
    
    context = {
            'page_title' : page_title,
            'form': form,
            'available_users' : available_users,
            'available_groups': available_groups
    }
    context.update(get_view_permissions(request.user))
    return render(request, template_name, context)


@login_required
def permission_delete(request, pk=None):
    # TODO Check if the user requesting the deletion has the Group Delete permission
    username = request.user.username
    can_access_dashboard = PermissionManager.user_can_access_dashboard(request.user)
    if not can_access_dashboard:
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    try:
        perm = Permission.objects.get(pk=pk)
        name = perm.name
        messages.add_message(request, messages.SUCCESS, 'Permission {} has been deleted'.format(name))
        perm.delete()
        logger.debug("Permission {} deleted by User {}", name, request.user.username)
        
    except Permission.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'Permission could not be found. Permission not deleted')
        logger.error("Permission Delete : Permission not found. Action requested by User {}",request.user.username)
        raise Http404('Permission does not exist')
        
    return redirect('dashboard:permissions')