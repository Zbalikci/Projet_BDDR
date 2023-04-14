"""projet_bddr URL Configuration

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
from django.urls import include,path
#from appli_covid19.views import pie_chart
from appli_covid19.views import ArticleChart


urlpatterns = [
    path('appli_covid19/', include('appli_covid19.urls')),
    path('appli_covid19/themes/', include('appli_covid19.urls')),
    #path('appli_covid19/articles/', include('appli_covid19.urls')),
    path('admin/', admin.site.urls),
    path('',ArticleChart.as_view(),name='home'),

]

    