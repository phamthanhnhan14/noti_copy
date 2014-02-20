# coding: utf-8
__author__ = 'mariozx'
from pyramid.view import view_config, forbidden_view_config
from pyramid.httpexceptions import HTTPFound
from ..import resources as _rsr
from notification_demo.lib import notification as N_Api

@view_config(context=_rsr.FBNotice, renderer='facebook.mak', permission="account_info")
def fb_notice_view(request):
    access_token = request.session['vgid_access_token']
    print 'access token: %s' % access_token

    scenario = request.GET.get("scenario")
    rid = request.GET.get("rid")
    if (scenario == "delete") and rid:
        # Huy tai khoan dang ky nhan thong bao qua facebook
        if N_Api.del_fb_receiver(access_token, rid):
            request.session.flash(u'Hủy bỏ nhận thông báo thành công', 'notification')
        return HTTPFound(request.path)

    if scenario == "callback":
        request.session.flash(u'Đăng ký nhận thông báo Facebook thành công', 'notification')
        return HTTPFound(request.path)

    list_fb_receivers = N_Api.get_list_fb_receiver(access_token)
    if not list_fb_receivers:
        list_fb_receivers = []

    if request.method == "POST":
        data = {"content": request.POST.get("message"),
                "users": request.user.id,
                "link": request.url}

        if N_Api.send_fb_message(data):
            _msg = u"""Bạn đã gửi thông báo thành công. Vui lòng truy cập <a href="https://www.facebook.com/" target="_blank">Facebook</a> để kiểm tra thông báo."""
            request.session.flash(_msg, 'notification')

    return {
        'list_fb_receivers': list_fb_receivers
    }
