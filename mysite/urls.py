"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from django.conf.urls import include
from . import views
urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'', views.home),
    path(r'hub', views.home, name="start"),
    path(r'help', views.help, name="help"),
    path(r'why', views.why, name="why"),
    # Plano
    path(r'kbj-plano', views.button, name='kbj-plano'),
    path(r'kbj-plano-schedule', views.kbjplano, name="plano_script"),
    path(r'request-off', views.form, name="form"),
    path(r'upload-plano', views.upload_plano, name="upload-plano"),
    path(r'schedule-plano', views.show_plano, name="schedule-plano"),
    # Frisco
    path(r'kbj-frisco', views.kbjfrisco, name='kbj-frisco'),
    path(r'kbj-frisco-schedule', views.kbjfrisco_schedule, name="frisco_script"),
    path(r'upload-frisco', views.upload_frisco, name="upload-frisco"),
    path(r'schedule-frisco', views.show_frisco, name="schedule-frisco"),
    # Pizza
    path(r'pizza', views.pizza, name='pizza'),
    path(r'pizza-schedule', views.pizza_schedule, name="pizza_script"),
    path(r'upload-pizza', views.upload_pizza, name="upload-pizza"),
    path(r'schedule-pizza', views.show_pizza, name="schedule-pizza"),
    # WFG
    path(r'wood-fire-grill', views.wood, name='wood-fire-grill'),
    path(r'wood-fire-grill-schedule', views.wood_schedule,
         name="wood-fire-grill_script"),
    path(r'upload-WFG', views.upload_wood, name="upload-WFG"),
    path(r'schedule-WFG', views.show_wood, name="schedule-WFG"),
    # Pizza
    path(r'italian', views.italian, name='italian'),
    path(r'italian-schedule', views.italian_schedule, name="italian-script"),
    path(r'upload-italian', views.upload_italian, name="upload-italian"),
    path(r'schedule-italian', views.show_italian, name="schedule-italian"),

    path(r'logout', views.log, name="log"),
    path('accounts/', include('django.contrib.auth.urls')),

    path(r'send_plano', views.send_plano, name="send_plano"),
    path(r'send_frisco', views.send_frisco, name="send_frisco"),
    path(r'send_pizza', views.send_pizza, name="send_pizza"),
    path(r'send_italian', views.send_italian, name="send_italian"),
    path(r'send_woodfire', views.send_woodfire, name="send_woodfire"),
    path(r'complete', views.check_for_cap, name="check")
]
