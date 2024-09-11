from django.urls import path
from .views import register, home, RecipeListView, RecipeDetailView

app_name = 'recipes'

urlpatterns = [
    path('register/', register, name='register'),
    path('', home, name='home'),
     # To connect list/ with the BookListView (a class-based view), you need to call as_view() (a method of class ListView)
    path("list/", RecipeListView.as_view(), name="list"),
    path("list/<int:pk>/", RecipeDetailView.as_view(), name="detail")
]
