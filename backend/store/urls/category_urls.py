from django.urls import path
from store.views.category_view import *

find_category_by_name_service = FindCategoryByNameService()
find_all_categories_service = FindAllCategoriesService()
create_category_service = CreateCategoryService()

urlpatterns = [
    path("find_by_name/<str:name>/", FindCategoryByNameView.as_view(find_category_by_name_service=find_category_by_name_service),
         name="category_find_by_name/<str:name>/"),
    path("find_all/", FindAllCategoriesView.as_view(find_all_categories_service=find_all_categories_service),
         name="category_find_all"),
    path("create/", CreateCategoryView.as_view(create_category_service=create_category_service),
         name="category_create"),
]