from django.db import models
from dashboard import constants as Constants


# Create your models here.

class AccessPermissions(models.Model):
   
    class Meta:
        managed = False
        permissions = [
            (Constants.TOKEN_GENERATE_PERM, 'Dashboard Can generate Token'),
            (Constants.DASHBOARD_VIEW_PERM, 'Dashboard Can view Dashboard'),

            (Constants.ACCOUNT_VIEW_PERM, 'Dashboard Can View Account'),
            (Constants.ACCOUNT_CHANGE_PERM, 'Dashboard Can Change Account'),
            (Constants.ACCOUNT_ADD_PERM, 'Dashboard Can Add Account'),
            (Constants.ACCOUNT_DELETE_PERM, 'Dashboard Can Delete Account'),

            (Constants.CATEGORY_VIEW_PERM, 'Dashboard Can View Category'),
            (Constants.CATEGORY_CHANGE_PERM, 'Dashboard Can Change Category'),
            (Constants.CATEGORY_ADD_PERM, 'Dashboard Can Add Category'),
            (Constants.CATEGORY_DELETE_PERM, 'Dashboard Can Delete Category'),

            (Constants.EVENT_VIEW_PERM, 'Dashboard Can View Event'),
            (Constants.EVENT_CHANGE_PERM, 'Dashboard Can Change Event'),
            (Constants.EVENT_ADD_PERM, 'Dashboard Can Add Event'),
            (Constants.EVENT_DELETE_PERM, 'Dashboard Can Delete Event'),

            (Constants.EVENTTICKET_VIEW_PERM, 'Dashboard Can View Event Ticket'),
            (Constants.EVENTTICKET_CHANGE_PERM, 'Dashboard Can Change Event Ticket'),
            (Constants.EVENTTICKET_ADD_PERM, 'Dashboard Can Add Event Ticket'),
            (Constants.EVENTTICKET_DELETE_PERM, 'Dashboard Can Delete Event Ticket'),

            (Constants.GROUP_ADD_PERM, 'Dashboard Can create a Group'),
            (Constants.GROUP_CHANGE_PERM, 'Dashboard Can change a Group'),
            (Constants.GROUP_DELETE_PERM, 'Dashboard Can delete a Group'),
            (Constants.GROUP_VIEW_PERM, 'Dashboard Can view Group'),



            (Constants.USER_VIEW_PERM, 'Dashboard Can View User'),
            (Constants.USER_CHANGE_PERM, 'Dashboard Can Change User'),
            (Constants.USER_ADD_PERM, 'Dashboard Can Add User'),
            (Constants.USER_DELETE_PERM, 'Dashboard Can Delete User'),
        ]