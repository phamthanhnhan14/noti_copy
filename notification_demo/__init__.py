from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid_beaker import session_factory_from_settings, set_cache_regions_from_settings
from .models import (
    DBSession,
    Base,
    initialize_web_database,
    )
from notification_demo.lib.request import NDRequest
import resources as _rsr
import os
ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
STATIC_DIR = os.path.join(ROOT_DIR, 'www', 'static')

def main(global_config, **app_settings):
    """ This function returns a Pyramid WSGI application.
    """
    settings = global_config
    settings.update(app_settings)
    initialize_web_database(settings)
    session_factory = session_factory_from_settings(settings)
    auth_policy = AuthTktAuthenticationPolicy(
        settings['auth_tkt.secret'],
        callback=models.user.get_user_groups,
        hashalg='sha512',
    )
    set_cache_regions_from_settings(settings)
    config = Configurator(settings=settings,
                          request_factory=NDRequest,
                          session_factory=session_factory,
                          root_factory=_rsr.Root,
                          authentication_policy=auth_policy)

    config.include('pyramid_mako')
    config.include('pyramid_layout')

    config.include('notification_demo.lib.client_script')
    config.include("pyramid_vgid_oauth2")
    config.include("notification_demo.views")
    config.include("notification_demo.lib.notification")

    config.add_static_view('static', STATIC_DIR, cache_max_age=3600)
    config.add_route('home', '/')
    config.scan()
    return config.make_wsgi_app()
