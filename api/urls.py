from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import ImageView
from .views import ImageAnalysis


urlpatterns = {
  	url(r'^upload/$', ImageView.as_view(), name='image-upload'),  	
  	url(r'^analysis/$', ImageAnalysis.as_view(), name='image-analysis'),
}

urlpatterns = format_suffix_patterns(urlpatterns)