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
        self.email = create_user.email

    def load(self):
        args = {"first_name": self.first_name, "email": self.email}
        return render_to_response('reg/register_success.html', args, RequestContext(self.request))


class email_activation_view(object):
    def __init__(self, status, request):
        self.status = status
        self.request = request

    def load(self):
        args = {'status': self.status}

        return render_to_response('reg/confirm.html', args, RequestContext(self.request))


class profile_page_view(object):
    def __init__(self, country, status, request):
        self.country = country
        self.status = status
        self.request = request

    def load(self):
        args = {'status': self.status, 'country': self.country}

        return render_to_response('advrprof/profile.html', args, RequestContext(self.request))


class profile_deleted_view(object):
    def __init__(self, request):
        self.request = request

    def load(self):

        return render_to_response('advrprof/delete.html', RequestContext(self.request))

class user_profile_updated_view(object):
    def __init__(self, request, country):
        self.request = request
        self.country = country

    def load(self):
        args = {'country': self.country}

        return render_to_response('advrprof/profile.html', args, RequestContext(self.request))

class logout_view(object):
    def __init__(self, request):
        self.request = request

    def load(self):
        args = {'status':'logout'}
        return render_to_response('homepage/home.html', args,  RequestContext(self.request))