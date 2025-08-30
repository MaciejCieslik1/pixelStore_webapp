from store.models import Category


class CategoryTestHelper:
    @staticmethod
    def create_categories() -> tuple[Category, Category]:
        category1 = Category(name="example_name1", description="example_description1")
        category2 = Category(name="example_name2", description="example_description2")
        category1.save()
        category2.save()
        return category1, category2
