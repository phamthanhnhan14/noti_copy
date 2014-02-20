__author__ = 'mariozx'

from sqlalchemy import (
    Column,
    types, )
from datetime import datetime
from pyramid.security import (
    Everyone,
    Authenticated,
    authenticated_userid, )
from . import Base, DBSession
from pyramid import security

class _UserGroupsDataType(types.TypeDecorator):
    impl = types.Text

    def __init__(self, groups_set, default_groups=None, *args, **kwargs):
        if default_groups is None:
            default_groups = []
        self._groups_set = groups_set
        self._default_groups = default_groups
        super(_UserGroupsDataType, self).__init__(*args, **kwargs)

    def _group_filter(self, gr_name):
        return gr_name in self._groups_set

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return u','.join(filter(self._group_filter, value))

    def process_result_value(self, value, dialect):
        if value is None:
            return self._default_groups
        groups = [g.encode('utf-8') if not isinstance(g, str) else g
                  for g in value.split(',')]
        return filter(self._group_filter, groups)

class User(Base):
    __tablename__ = 'user'

    GROUP_SUPER_SAIYAN = 'g.super_saiyan'
    GROUP_ADMIN = 'g.admin'
    GROUP_MODERATOR = 'g.moderator'

    GROUPS = [
        GROUP_SUPER_SAIYAN,
        GROUP_ADMIN,
        GROUP_MODERATOR
    ]

    GENDER_MALE = 'MALE'
    GENDER_FEMALE = 'FEMALE'
    GENDER_OTHER = 'OTHER'

    id = Column(types.Integer, primary_key=True, autoincrement=False)
    name = Column(types.VARCHAR(length=255), nullable=False)
    email = Column(types.VARCHAR(length=255), unique=True)
    phone = Column(types.VARCHAR(length=255), unique=True)
    avatar = Column(types.Text())
    gender = Column(types.Enum(GENDER_MALE, GENDER_FEMALE, GENDER_OTHER), default=None)
    dob = Column(types.DateTime(), default=None)
    address = Column(types.Text())
    city_id = Column(types.VARCHAR(length=45))
    sources = Column(types.Text())
    created_time = Column(types.DateTime, nullable=False, default=datetime.now)
    last_modified_time = Column(types.DateTime, nullable=False, default=datetime.now)

    _groups = Column('groups', _UserGroupsDataType(GROUPS))

    @property
    def groups(self):
        return self._groups

    @groups.setter
    def groups(self, value):
        self._groups = value

    def __init__(self, **kwargs):
        self.merge_from_dict(kwargs)

    def merge_from_dict(self, dic):
        if 'last_modified_time' in dic:
            last_modified_time = dic['last_modified_time']
            if not isinstance(last_modified_time, datetime):
                last_modified_time = datetime.strptime(last_modified_time, '%Y-%m-%d %H:%M:%S')
            force_merge = not self.last_modified_time \
                or (self.last_modified_time < last_modified_time)
        else:
            force_merge = False

        for c in self.__table__.columns:
            attr_name = c.name
            if not attr_name in dic:
                continue
            old_value = self.__getattribute__(attr_name)
            new_value = dic[attr_name]
            if new_value and (not old_value or force_merge):
                setattr(self, attr_name, new_value)

    def __unicode__(self):
        return u"%s (%d#%s)" % (self.name, self.id, self.email)

    def __str__(self):
        return self.__unicode__().encode('utf-8')

def get_user(user_id):
    user = DBSession.query(User).get(user_id)
    return user

def get_user_privileges(user_id, request=None):
    user = get_user(user_id)
    if user is None:
        return None
    if request is not None:
        request.__user__ = user
    groups = user.groups
    return set([Everyone, Authenticated] + groups)

def get_user_for_request(request):
    user_id = authenticated_userid(request)
    try:
        return request.__user__
    except AttributeError:
        user = get_user(user_id) if user_id is not None else None
        request.__user__ = user
    return request.__user__

def import_user_from_dict(dic):
    """
    @rtype: User
    """
    assert 'id' in dic, "Unknow id from dict %s" % dic
    obj = DBSession.query(User).get(dic['id'])
    if obj is None:
        obj = User()
        obj.merge_from_dict(dic)
        DBSession.add(obj)
    else:
        obj.merge_from_dict(dic)
    obj.id = int(obj.id)

    return obj

def put_vgid_user(acc):
    global DBSession
    u = User(
        id=acc['id'],
        name=acc['name'],
        email=acc['email'],
        avatar=acc['avatar'],
    )
    DBSession.merge(u)
    DBSession.flush()
    return u

def get_user_groups(userid, request):
    """
    :type request: pyramid.request.Request
    """
    user = get_user(userid)
    request.authenticated_user = user

    if user is None:
        return []

    groups = user.groups or ""
    return [security.Everyone, security.Authenticated] + groups.split(',')
