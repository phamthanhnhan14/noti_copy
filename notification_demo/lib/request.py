__author__ = 'mariozx'
from pyramid.request import Request

class NDRequest(Request):
    @property
    def vgid_access_token(self):
        return self.session.get('vgid_access_token', None)

    @vgid_access_token.setter
    def vgid_access_token(self, value):
        self.session['vgid_access_token'] = value

    @vgid_access_token.deleter
    def vgid_access_token(self):
        try:
            del(self.session['vgid_access_token'])
        except KeyError:
            pass

    @property
    def authenticated_user(self):
        try:
            return self._authenticated_user
        except AttributeError:
            self.authenticated_userid
            try:
                return self._authenticated_user
            except AttributeError:
                self._authenticated_user = None
            return self._authenticated_user
        return None

    @authenticated_user.setter
    def authenticated_user(self, value):
        self._authenticated_user = value

    @property
    def user(self):
        return self.authenticated_user
