from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView
from .models import Recipe
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RecipesSearchForm, UserRegistrationForm
import pandas as pd
from .utils import get_chart
from django.contrib.auth import login

def home(request):
    return render(request, 'recipes/recipes_home.html')

class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = "recipes/recipe_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = RecipesSearchForm()
        return context

    def post(self, request, *args, **kwargs):
        form = RecipesSearchForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            ingredients = form.cleaned_data.get('ingredients', '').split(',')
            chart_type = form.cleaned_data['chart_type']

            # Filter recipes by ingredients
            qs = Recipe.objects.all()
            if name:
                qs = qs.filter(name__icontains=name)
            if ingredients:
                for ingredient in ingredients:
                    qs = qs.filter(ingredients__icontains=ingredient.strip())

            if qs.exists():
                # Convert the queryset to a pandas DataFrame and render it as HTML
                df = pd.DataFrame(qs.values()).drop('id', axis=1) # Remove id column
                chart=get_chart(chart_type, df, labels=df['ingredients'].values)
                df = df.to_html()
            else:
                # No matching recipes found
                df = None
                chart = None

            context = {
                'form': form,
                'df': df,
                'chart': chart,
                'message': 'No recipes found matching your search criteria.' if not qs.exists() else ''
            }
            return render(request, self.template_name, context)

        # If form is invalid, re-render the page with the form errors
        return self.get(request, *args, **kwargs)

class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = Recipe
    template_name = "recipes/recipe_details.html"


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Create the user instance but don't save it yet
            user.set_password(form.cleaned_data['password'])  # Set the password correctly
            user.save()  # Save the user instance
            login(request, user)  # Log the user in after registration
            return redirect('recipes:list')  # Redirect to the recipe list
    else:
        form = UserRegistrationForm()
    return render(request, 'auth/register.html', {'form': form})