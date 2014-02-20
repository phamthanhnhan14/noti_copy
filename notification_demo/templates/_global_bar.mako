<div class="navbar navbar-inverse" role="navigation">
  <div class="container-fluid">
    <div class="navbar-header">
      <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
        <span class="sr-only">Toggle navigation</span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
      <a class="navbar-brand" href="${layout.home_url}">
          <span class="glyphicon glyphicon-envelope"></span>
          Notification Demo
      </a>
    </div>

    <div class="navbar-collapse collapse">
      <ul class="nav navbar-nav navbar-right">
          <li>${user_board()}</li>
      </ul>
    </div>
    <ul>
        <li>
            <a href="/facebook">Demo Facebook</a>
        </li>
    </ul>
  </div>
</div>

<%def name="user_board()">
    <% import pyramid_vgid_oauth2 as pvo %>
    % if request.authenticated_user:
        <a href="#" class="dropdown-toggle" data-toggle="dropdown">
            <img src="${request.authenticated_user.avatar}" width="32" style="margin:-5px 0px">
            ${request.authenticated_user.name}
            <b class="caret"></b>
        </a>
        <ul class="dropdown-menu">
            <li><a href="#"><strong>${request.authenticated_user.name}</strong></a></li>
            <li><a href="#">${request.authenticated_user.email}</a></li>
            <li class="divider"></li>
            <li><a href="${pvo.signout_url(request)}">Đăng xuất</a></li>
        </ul>
    % else:
        <a href="${pvo.signin_url(request)}">Đăng nhập</a>
    % endif
</%def>
