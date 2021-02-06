from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import DjangoModelPermissions


class BearerTokenAuthentication(TokenAuthentication):
    keyword = "Bearer"


class CustomDjangoModelPermissions(DjangoModelPermissions):
    def __init__(self):
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']
