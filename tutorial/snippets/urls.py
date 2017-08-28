from django.conf.urls import url, include
from snippets import views
from rest_framework.routers import SimpleRouter
from rest_framework.schemas import get_schema_view

# Create a router and register our viewsets with it.
router = SimpleRouter()
router.register(r'snippets', views.SnippetViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'feedings', views.FeedingViewSet)
router.register(r'discharge', views.DischargeViewSet)
schema_view = get_schema_view(title='Pastebin API')

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^schema/$', schema_view),
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^newFeeding/', views.FeedingFormView.as_view(), name='newFeeding'),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]