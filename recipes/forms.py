from django import forms
from django.contrib.auth.models import User

CHART_CHOICES = (
    ('#1', 'Bar chart'),
    ('#2', 'Pie chart'),
    ('#3', 'Line chart'),
)

class RecipesSearchForm(forms.Form):
    name = forms.CharField(
        max_length=120, 
        required=False, 
        widget=forms.TextInput(attrs={'placeholder': 'Enter recipe name'})
    )
    ingredients = forms.CharField(
        max_length=500, 
        required=False, 
        widget=forms.TextInput(attrs={'placeholder': 'Enter an ingredient'})
    )
    chart_type = forms.ChoiceField(choices=CHART_CHOICES)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': ''}),
    )
    password_confirm = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'placeholder': ''}),
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']  # Include password_confirm

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Hash the password
        if commit:
            user.save()
        return user