__author__ = 'mariozx'
from pyramid.authorization import Allow
from pyramid.authentication import Authenticated
class _BaseResource(object):
    def __init__(self, parent, name):
        self.__parent__ = parent
        self.__name__ = name
        self._child_resources = {}

    __children__ = {}

    def __getitem__(self, key):
        try:
            return self._child_resources[key]
        except KeyError:
            _cls = self.__children__[key]
            self._child_resources[key] = _cls(self, key)

        return self._child_resources[key]

class FBNotice(_BaseResource):

    __acl__ = [
        (Allow, Authenticated, 'account_info'),
    ]

class Root(_BaseResource):
    __name__ = None
    __parent__ = None

    __children__ = {
        'facebook': FBNotice
    }

    def __init__(self, request):
        self.request = request
        super(Root, self).__init__(None, None)
