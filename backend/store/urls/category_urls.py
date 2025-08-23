from django.urls import path

from store.service.category_service import *
from store.views.category_view import *

find_category_by_name_service = FindCategoryByNameService()
find_all_categories_service = FindAllCategoriesService()
create_category_service = CreateCategoryService()

urlpatterns = [
    path("find_category_by_name/", FindCategoryByNameView.as_view(find_category_by_name_service=find_category_by_name_service),
         name="category_find_category_by_name/<str:name>/"),
    path("find_all_categories/", FindAllCategoriesView.as_view(find_all_categories_service=find_all_categories_service),
         name="category_find_all_categories"),
    path("create_category/", CreateCategoryView.as_view(create_category_service=create_category_service),
         name="category_create_category"),
]