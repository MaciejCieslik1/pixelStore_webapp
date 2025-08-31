from store.exceptions import CategoryNotFoundError, CategoryNameAlreadyOccupiedError
from store.helper_classes.authentication_helper import TokenUtils
from store.models import User, Category


class FindCategoryByNameService:
    def find_by_name(self, token: str, user: User, name: str) -> dict:
        TokenUtils.verify_access_token(token, user)
        try:
            category = Category.objects.get(name=name)
            return {"name": category.name, "description": category.description}
        except Category.DoesNotExist:
            raise CategoryNotFoundError("Category with this name not found.")

class FindAllCategoriesService:
    def find_all(self, token: str, user: User) -> list:
        TokenUtils.verify_access_token(token, user)
        try:
            categories = Category.objects.all()
            return [{"name": category.name, "description": category.description} for category in categories]
        except Category.DoesNotExist:
            raise CategoryNotFoundError("Category with this name not found.")


class CreateCategoryService:
    def create(self, token: str, user: User, new_category_data: dict) -> str:
        TokenUtils.verify_access_token(token, user)

        if Category.objects.filter(name=new_category_data["name"]).exists():
            raise CategoryNameAlreadyOccupiedError("Category with this name already exists.")

        category = Category(name=new_category_data["name"], description=new_category_data["description"])
        category.save()
        return f"Category {new_category_data['name']} created successfully."
