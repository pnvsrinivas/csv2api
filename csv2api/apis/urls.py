from django.urls import include
from django.conf.urls import url
from rest_framework import routers
from rest_framework.documentation import include_docs_urls

from csv2api.apis.users.views import UserViewSet
from csv2api.apis.data.views import DatasetUploadView, DatasetAPIView

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls), name='api_index'),
    url(r'^upload/', DatasetUploadView.as_view()),
    url(r'^data/(?P<id>[0-9a-fA-F-]+)/', DatasetAPIView.as_view(), name="data"),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^docs/', include_docs_urls(title='csv2api', public=True)),
]