"""questionnaire URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from question_foruser import  views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/', views.index),
    url(r'^login/', views.login),
    url(r'^del/(?P<del_id>\d+)', views.del_item),
    url(r'^save/(?P<save_id>\d+)', views.save_item),
    url(r'^edit/(\d+)', views.edit_item),
    url(r'^save/(\d+)', views.save_item),
    url(r'^save2/(\d+)', views.save2_item),
    url(r'^answer_question/(\d+)/(\d+)/$', views.answer_question),
]
