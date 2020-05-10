from django.urls import include
from django.conf.urls import url
from rest_framework import routers
from rest_framework.documentation import include_docs_urls

from csv2api.apis.users.views import UserViewSet
from csv2api.apis.data.views import (
    FileUploadView, FileDataAPIView,
    DatasetModelViewSet
)

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'datasets', DatasetModelViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls), name='api_index'),
    url(r'^file/upload/', FileUploadView.as_view(), name='file-upload'),
    url(r'^file/(?P<id>[0-9a-fA-F-]+)/', FileDataAPIView.as_view(), name="file-detail"),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^docs/', include_docs_urls(title='csv2api', public=True)),
]