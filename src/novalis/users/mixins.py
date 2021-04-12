from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import redirect


class GroupRequiredMixin(object):

    group_required = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        elif request.user.groups.exists():
            user_groups  = []
            for group in request.user.groups.all():
                user_groups.append(group.name)
            if 'manager' not in user_groups:
                return HttpResponse('you are not authorized to perform this action.')
            return super(GroupRequiredMixin, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

