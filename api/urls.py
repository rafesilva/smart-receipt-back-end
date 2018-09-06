from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import FileView
from .views import FileAnalysis


urlpatterns = {
  	url(r'^upload/$', FileView.as_view(), name='file-upload'),  	
  	url(r'^analysis/$', FileAnalysis.as_view(), name='file-analysis'),
}

urlpatterns = format_suffix_patterns(urlpatterns)