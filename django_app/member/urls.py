from django.conf.urls import url

from . import views

app_name = 'member'
urlpatterns = [
    url(r'^login/$', views.login_view, name='login'),
    url(r'^signup/$', views.signup_fbv, name='signup'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^logout/$', views.logout_fbv, name='logout'),
    url(r'^profile/change/$', views.change_profile_image, name='change_image'),
]
