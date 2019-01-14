from rest_framework import permissions
from .models import Override, Attendance


def is_leader(user, obj):
    if not hasattr(obj, "leader"):
        return False
    leader = obj.leader
    while leader:
        if user == leader.user:
            return True
        else:
            leader = leader.leader
    return False


class IsLeader(permissions.BasePermission):
    """
    Grants read/write permission to resource only if the logged in user is the leader of the resource.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    # note: has_permission is always run before has_object_permission
    def has_object_permission(self, request, view, obj):
        # Transform to linked section
        if isinstance(obj, Override) or isinstance(obj, Attendance):
            obj = obj.section

        return is_leader(request.user, obj)


class IsLeaderOrReadOnly(IsLeader):
    """
    Grants permission to edit resource only if is leader of resource, read-only
    otherwise.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS
            or super().has_permission(request, view)
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in permissions.SAFE_METHODS
            or super().has_object_permission(request, view, obj)
        )


class IsReadIfOwner(permissions.BasePermission):
    """
    Grants permission to read the resource only if the requester is the user associated
    with the object.
    """

    def has_permission(self, request, view):
        return bool(
            (
                request.method in permissions.SAFE_METHODS
                and request.user
                and request.user.is_authenticated
            )
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            (
                request.method in permissions.SAFE_METHODS
                and request.user
                and request.user == obj.user
            )
        )


class IsOwner(permissions.BasePermission):
    """
    Grants permission to read/write the resource only if the requester is the user
    associated with the object.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user == obj.user)
