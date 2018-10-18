"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls import include, url, handler400, handler403, handler404, handler500
from django.conf.urls.static import static
from django.urls import path
import debug_toolbar
from core.views import *
from core.backends import *

urlpatterns = [
    path('', index, name='index'),
    path('dashboard/', dashboard, name='dashboard'),
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='signin'),
    path('logout/', logout_view, name='logout'),
    path('register/', RegistrarUsuarioView.as_view(), name='register'),
    # Courses
    path('courses/', course_list, name='course_list'),
    path('course/add/', CourseFormView.as_view(), name='course_add'),
    path('lecture/add/', LectureFormView.as_view(), name='lecture_add'),
    path('discount/add/', DiscountFormView.as_view(), name='discount_add'),
    path('courses-teacher/', course_list_teacher, name='course_list_teacher'),
    path('courses-favorite/', favorites_list, name='course_list_favorite'),
    path('lectures/<int:id>', view_lectures, name='view_lectures'),
    path('detail/course/<int:id>', course_details, name="detail_course"),
    path('subscriptions_list', subscriptions_list, name="subscriptions_list"),
    path('aprove_subscription/<int:id>', aprove_subscription, name="aprove_subscription"),
    #
    path('buy-course/<int:id>',buy_course_confirmation, name="buy_course_confirmation"),
    path('buy/<int:id>', buy_course, name="buy_course"),
    #Recover Password
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [ url(r'^__debug__/', include(debug_toolbar.urls)), ]

handler404 = 'core.views.handler404'
handler500 = 'core.views.handler500'
