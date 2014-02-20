#coding: utf-8
__author__ = 'mariozx'

import requests as http_requests
from requests.auth import HTTPBasicAuth
import json
import logging
import urllib

DOMAIN = "http://notification.x.vnpid.com"
RECEIVER_PATH = DOMAIN + "/receiver/fbpns"
SEND_MESSAGE_PATH = DOMAIN + "/message/fbpns"

auth = None
# Tài khoản để gọi API sang hệ thống Notification
# settings = get_current_registry().settings
# print settings
# _usr = settings.get("notification.api.http_user", "")
# _pwd = settings.get("notification.api.http_pwd", "")
#
# auth = HTTPBasicAuth(_usr, _pwd)
#
def catch_resful_exception(fn):
    """ decorator để bắt các lỗi bất thường khi gọi API sang hệ thống notification
    """
    def wrapped(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except http_requests.RequestException as e:
            logging.warning(str(e))
            return None

    return wrapped

def link_accept_app_fb(redirect_link):
    """ Link này để người dùng click đồng ý nhận notification từ app facebook.
    :type redirect_link: str
    """
    return "https://id.vatgia.com/notification/facebook/?" + \
           urllib.urlencode({"scenario": "register", "_cont": redirect_link})

@catch_resful_exception
def get_list_fb_receiver(access_token):
    _url = RECEIVER_PATH + "?access_token=%s" % access_token
    r = http_requests.get(_url, auth=auth)
    if r.status_code == 200:
        try:
            return json.loads(r.text)
        except BaseException:
            return []
    else:
        logging.warning("Warning when connect to notification service: %s" % r.text)

@catch_resful_exception
def del_fb_receiver(access_token, receiver_id=None):
    _url = RECEIVER_PATH + "?access_token=%s" % access_token
    if receiver_id:
        _url += "&receiver_id=%s" % receiver_id
    r = http_requests.delete(url=_url, auth=auth)
    if r.status_code != 200:
        logging.warning(r.text)
    else:
        return True

@catch_resful_exception
def send_fb_message(data):
    """ gửi thông báo đến facebook người dùng
    :type data: dict
    @data:
        "users": Danh sách id (theo id trên hệ thống id.vatgia.com) những tài khoản
                nhận thông báo. các id được ngăn cách bởi dấu phảy
        "content": Nội dung thông báo muốn gửi
        "link": link trả về khi người dùng click vào thông báo trên facebook

    Return:
        None: Nếu có lỗi
        True: Nếu gửi thành công (gửi thành công sang hệ thống notification)
    """
    r = http_requests.post(SEND_MESSAGE_PATH, auth=auth, data=data)
    if r.status_code == 200:
        return True
    else:
        logging.warning(r.text)

class NotificationAPI(object):
    pass

def includeme(config):
    """
    :type config: pyramid.config.Configurator
    """
    global auth
    settings = config.registry.settings
    _usr = settings.get("notification.api.http_user", "")
    _pwd = settings.get("notification.api.http_pwd", "")
    auth = HTTPBasicAuth(_usr, _pwd)