##<%inherit file="index.mako"></%inherit>
<%inherit file="${context['main_template'].uri}"/>
<%def name="page_title()">Facebook Demo</%def>
<div class="wrap-user-deal row" style="padding-left: 50px">
    <h1 style="color: #DD4B39">Nhận thông báo từ Vật Giá thông qua Facebook</h1>
    <% messages = request.session.pop_flash("notification") %>
    % if messages:
        % for message in messages:
            <div class="alert alert-success">${message|n}</div>
        % endfor
    % endif
    % if list_fb_receivers:
        <legend>Các Facebook bạn đã đăng ký nhận thông báo</legend>
    % else:
        <legend>Click Thêm tài khoản để nhận thông báo từ hệ thống thông qua facebook</legend>
    % endif
    % for receiver in list_fb_receivers:
        <ul>
        <li>
            <a class="col-lg-3" href="https://facebook.com/${receiver.get("fb_id")}"><em>${receiver.get("fb_name", receiver.get("fb_id", None))}</em></a>
            <a class="btn btn-small btn-danger" href="${request.url}?scenario=delete&rid=${receiver.get("id")}">Hủy bỏ</a>
        </li>
        </ul>
    % endfor

    <% from notification_demo.lib.notification import link_accept_app_fb %>
    <a class="btn btn-small btn-primary" href="${link_accept_app_fb(request.path_url+"?scenario=callback")}">Thêm tài khoản Facebook</a>
    <legend>Gửi thông báo Test</legend>
    <form method="post">
    <div class="control-group">
        <label for="SendFBTest_message" class="control-label required">Nội dung thông báo <span class="required">*</span></label>
        <div class="controls">
            <textarea id="SendFBTest_message" name="message" class="span8" rows="5" cols="80" style="font-size: 16px; font-family: monospace !important; color: #808080">Thông báo test dành cho ${request.authenticated_user.name}</textarea>

        </div>
            </div>
        <div class="controls bt-group-edit">
            <button class="btn btn-small btn-primary" type="submit" name="btnSendTest" value="btnSendTest">Gửi thông báo</button>
        </div>
    </form>
</div>
