from django.urls import path

from . import views

app_name = 'recipe'

urlpatterns = [
    # - Tag Urls - #
    path('tags', views.TagList.as_view(), name='tag_list'),
    path('tag/<int:pk>', views.TagDetail.as_view(), name='tag_detail'),
    path('tag/create', views.TagCreate.as_view(), name='tag_create'),
    path('tag/update/<int:pk>', views.TagUpdate.as_view(), name='tag_update'),
    path('tag/delete/<int:pk>', views.TagDelete.as_view(), name='tag_delete'),
    # - Ingredient Urls - #
    path('ingredients', views.IngredientList.as_view(),
         name='ingredient_list'),
    path('ingredient/<int:pk>', views.IngredientDetail.as_view(),
         name='ingredient_detail'),
    path('ingredient/create', views.IngredientCreate.as_view(),
         name='ingredient_create'),
    path('ingredient/update/<int:pk>', views.IngredientUpdate.as_view(),
         name='ingredient_update'),
    path('ingredient/delete/<int:pk>', views.IngredientDelete.as_view(),
         name='ingredient_delete'),
]
