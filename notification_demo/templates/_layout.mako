<!doctype html>
<html lang="vi">
    <head>
        <meta content="text/html; charset=utf-8" http-equiv="Content-Type">
        <meta content="vi" name="language">
        <meta content="Đấu giá" name="description">
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <%
            ClientScript.js_file(static_url("js/jquery.min.js"), name="jquery")
            ClientScript.js_file(static_url("js/jquery-ui.min.js"), name="jquery-ui")
            ClientScript.css_file(static_url("bootstrap/css/bootstrap-glyphicons.css"))
            ClientScript.css_file(static_url("bootstrap/css/bootstrap.css"), name="bootstrap")
            ClientScript.js_file(static_url("bootstrap/js/bootstrap.min.js"), name="bootstrap")
        %>
        <%def name="page_title()">Chú ý thay đổi nội dung ở đây</%def>
        <title>${self.page_title()}</title>
    </head>
    <body>
        <%include file="_global_bar.mako" />
        ${next.body()}
        <div class="container-fluid">
            <div class="row">
                <hr>
                <p class="text-left" style="margin-left: 30px; font-family: monospace; text-align: center" ><small>
                    Công ty Cổ phần Vật Giá Việt Nam. Số GCNDT: 011032001615, cấp ngày 21/06/2012, nơi cấp: UBND thành phố Hà Nội.
                    <br>
                    Trụ sở chính: Lê Đại Hành, Hai Bà Trưng, Hà Nội - Chi nhánh Hồ Chí Minh: Đường Lữ Gia, Phường 15, Quận 11, Hồ Chí Minh
                    <br>
                    &copy; 2014 by VGID team.
                </small></p>
            </div>
        </div>
    </body>
</html>