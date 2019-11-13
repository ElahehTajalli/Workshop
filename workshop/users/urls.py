from django.conf.urls import url

from . import views

urlpatterns = [
    url('signup', views.signup ),
    url('login', views.login_view ),
    url('verify/(?P<verify_id>[0-9a-f-]+)', views.verify),
    url('list', views.user_list )
]