from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Projects, CustomUsers, Issues, Comments, Contributors

owner_methods = ("PUT", "DELETE")
contrib_methods = ("POST", "GET")


class HasContributorPermission(BasePermission):

    def has_permission(self, request, view):
        project = Projects.objects.get(id=view.kwargs['project_id'])
        if project in Projects.objects.filter(contributors__user=request.user):
            project = Projects.objects.get(id=view.kwargs['project_id'])
            if request.method in SAFE_METHODS:
                return True
            return request.user == project.author_user
        return False


class HasProjectPermission(BasePermission):
    def has_permission(self, request, view):
        if Contributors.objects.filter(user=request.user).filter(project=view.kwargs['project_id']).exists():
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.method in owner_methods:
            return obj.author_user == request.user
        else:
            return False


class HasIssuePermission(BasePermission):
    def has_permission(self, request, view):
        if Contributors.objects.filter(user=request.user).filter(project=view.kwargs['project_id']).exists():
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.method in owner_methods:
            if obj.author_user == request.user:
                return True
        else:
            return request.user == obj.author_user


class HasCommentPermission(BasePermission):
    def has_permission(self, request, view):
        if Contributors.objects.filter(user=request.user).filter(project=view.kwargs['project_id']).exists():
            return True

    def has_object_permission(self, request, view, obj):
        if request.method in owner_methods:
            if obj.author_user_id == request.user:
                return True
        else:
            return request.user == obj.author_user_id
