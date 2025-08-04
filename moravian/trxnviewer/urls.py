from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'api/memoirs', views.MemoirViewSet, basename='memoir_api')

urlpatterns = [
    path("memoirs", views.index, name="memoirs"),
    path("memoirs/<int:memoir_id>/", views.detail_memoir,
         name="detail_memoir"),
    path("memoirs/<int:memoir_id>/<int:image_id>", views.detail_image,
         name="detail_image"),
    path("memoirs-zip", views.MemoirZipView.as_view(),
         name='memoir_zip')
] + router.urls
