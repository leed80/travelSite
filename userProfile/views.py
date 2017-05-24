from django.shortcuts import render_to_response
from django.template import RequestContext


class registration_page_view(object):
    def __init__(self, request):
        self.request = request

    def load(self):
        return render_to_response('reg/reg.html', RequestContext(self.request))



class user_registered_view(object):
    def __init__(self, request, create_user):
        self.request = request
        self.first_name = create_user.first_name
        self.email = create_user.last_name

    def load(self):
        args = {"first_name": self.first_name, "email": self.email}
        return render_to_response('reg/register_success.html', args, RequestContext(self.request))


