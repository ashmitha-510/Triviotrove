from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile

# ✅ Profile Form (Allow Profile Image Upload)
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["profile_image"]

# ✅ Login Form (Bootstrap Styled)
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={
            "class": "form-control", 
            "placeholder": "Enter your username",
            "autocomplete": "username"
        })
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            "class": "form-control", 
            "placeholder": "Enter your password",
            "autocomplete": "current-password"
        })
    )

# ✅ Register Form (Ensures Email is Unique)
class RegisterForm(UserCreationForm):  # 🔹 Renamed to match views.py
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter username"})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter email"})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter password"})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirm password"})
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_email(self):
        """✅ Ensure email is unique"""
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use. Please use a different one.")
        return email

    def save(self, commit=True):
        """✅ Save email correctly to User model"""
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
