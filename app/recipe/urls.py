from django.urls import path

from .views import TagList, TagDetail, TagCreate, TagUpdate, TagDelete

app_name = 'recipe'

urlpatterns = [
    path('tags', TagList.as_view(), name='tag_list'),
    path('tag/<int:pk>', TagDetail.as_view(), name='tag_detail'),
    path('tag/create', TagCreate.as_view(), name='tag_create'),
    path('tag/update/<int:pk>', TagUpdate.as_view(), name='tag_update'),
    path('tag/delete/<int:pk>', TagDelete.as_view(), name='tag_delete'),
]
