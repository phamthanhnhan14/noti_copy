<%inherit file="_layout.mako"/>
<% import pyramid_vgid_oauth2 as pvo2%>
% if not request.authenticated_user:
<div class="alert alert-info"> Bạn cần <strong>đăng nhập</strong> để truy cập trang này. Vui lòng click vào đây để <a id="fancybox-signin" href="${pvo2.signin_url(request)}"><strong>đăng nhập</strong>.</a></div>

<em>Trình duyệt sẽ tự động chuyển bạn đến trang đăng nhập sau <span id="countdown">5</span> giây nữa.</em>

<script type="text/javascript">
    function decrease_countdown()
    {
        var sec = parseInt($('#countdown').text())
        sec--
        if (sec <= 0) {
            location.href = "${pvo2.signin_url(request)}";
##            sec = 0
            window.clearInterval(hCountdown)

        }
        $('#countdown').text(sec)
    }

    hCountdown = window.setInterval(decrease_countdown, 1000)
</script>
% else:
    <div class="alert alert-danger"><strong>Cảnh báo!</strong> 403 Forbidden</div>
% endif