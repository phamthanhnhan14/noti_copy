__author__ = 'mariozx'

from pyramid.view import view_config, forbidden_view_config

@view_config(route_name='home', renderer='index.mako')
def my_view(request):
    return {}

class MainLayout(object):
    page_title = 'Hooray! My App!'

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.home_url = request.application_url


def includeme(config):
    """
    :type config: pyramid.config.Configurator
    """
    config.add_layout('notification_demo.views.MainLayout',
                  'notification_demo:templates/_layout.mako')

@forbidden_view_config(renderer='forbidden.mak')
def forbidden(request):
    return {}