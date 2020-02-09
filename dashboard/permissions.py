from dashboard import constants as Constants



class PermissionManager :
    """
    This Class provides a central to check for permission.
    """

    @staticmethod
    def user_has_perm(user=None, perm=None):
        flag = False
        if user and perm and hasattr(user, 'has_perm'):
            flag = user.has_perm(Constants.APP_PREFIX + perm)
        return flag


    @staticmethod
    def user_can_generate_token(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.TOKEN_GENERATE_PERM)

    @staticmethod
    def user_can_access_dashboard(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.DASHBOARD_VIEW_PERM)

    ## USER PERMISSION
    @staticmethod
    def user_can_view_user(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.USER_VIEW_PERM)
    
    @staticmethod
    def user_can_change_user(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.USER_CHANGE_PERM)

    @staticmethod
    def user_can_add_user(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.USER_ADD_PERM)
    
    @staticmethod
    def user_can_delete_user(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.USER_DELETE_PERM)

    ## ACCOUNT PERMISSION
    @staticmethod
    def user_can_view_account(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.ACCOUNT_VIEW_PERM)
    
    @staticmethod
    def user_can_change_account(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.ACCOUNT_CHANGE_PERM)

    @staticmethod
    def user_can_add_account(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.ACCOUNT_ADD_PERM)
    
    @staticmethod
    def user_can_delete_account(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.ACCOUNT_DELETE_PERM)
    
    ## GROUP PERMISSION
    @staticmethod
    def user_can_view_group(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.GROUP_VIEW_PERM)
    
    @staticmethod
    def user_can_change_group(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.GROUP_CHANGE_PERM)

    @staticmethod
    def user_can_add_group(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.GROUP_ADD_PERM)
    
    @staticmethod
    def user_can_delete_group(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.GROUP_DELETE_PERM)

    ## EVENT PERMISSION
    @staticmethod
    def user_can_view_event(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.EVENT_VIEW_PERM)
    
    @staticmethod
    def user_can_change_event(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.EVENT_CHANGE_PERM)

    @staticmethod
    def user_can_add_event(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.EVENT_ADD_PERM)

    @staticmethod
    def user_can_delete_event(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.EVENT_DELETE_PERM)

    ## EVENT TICKET PERMISSION

    @staticmethod
    def user_can_change_event_ticket(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.EVENTTICKET_CHANGE_PERM)

    @staticmethod
    def user_can_view_event_ticket(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.EVENTTICKET_VIEW_PERM)

    @staticmethod
    def user_can_add_event_ticket(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.EVENTTICKET_ADD_PERM)

    @staticmethod
    def user_can_delete_event_ticket(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.EVENTTICKET_DELETE_PERM)

    
    ## CATEGORY PERMISSION

    @staticmethod
    def user_can_change_category(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.CATEGORY_CHANGE_PERM)
    
    @staticmethod
    def user_can_add_category(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.CATEGORY_ADD_PERM)
    
    @staticmethod
    def user_can_delete_category(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.CATEGORY_DELETE_PERM)

    @staticmethod
    def user_can_view_category(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.CATEGORY_VIEW_PERM)

    

def get_view_permissions(user=None):
    context = {
        'can_access_dashboard' : PermissionManager.user_can_access_dashboard(user),
        'can_view_event': PermissionManager.user_can_view_event(user),
        'can_view_eventticket': PermissionManager.user_can_view_event_ticket(user),
        'can_view_user': PermissionManager.user_can_view_user(user),
        'can_view_category': PermissionManager.user_can_view_category(user),
        'can_view_group' : PermissionManager.user_can_view_group(user),
        'can_add_group' : PermissionManager.user_can_add_group(user),
        'can_generate_token': PermissionManager.user_can_generate_token(user)
    }
    return context