import random
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile, Word
from .forms import ProfileForm, LoginForm, RegisterForm

# Store words that have been used in a session
USED_WORDS = set()

# Word list (Move to DB for better scalability)
WORDS = [
    "python", "academic", "developer", "background", "javascript", "beautiful", "django", "calculate", "database",
    "chocolate", "algorithm", "function", "english", "variable", "event", "loop", "fashion", "troubleshoot",
    "flower", "backend", "game", "frontend", "gold", "framework", "happy", "iteration", "holiday", "recursion", 
    "india", "html", "java", "ability"
]

def scramble_word(word):
    """Scrambles the given word"""
    return "".join(random.sample(word, len(word)))

def get_new_word(request):
    global USED_WORDS

    # Reset when all words are used
    if len(USED_WORDS) == len(WORDS):
        USED_WORDS.clear()

    # Select an unused word
    available_words = [word for word in WORDS if word not in USED_WORDS]
    
    if not available_words:
        return JsonResponse({"error": "No words available!"}, status=400)

    word = random.choice(available_words)
    USED_WORDS.add(word)  # Mark word as used
    scrambled = scramble_word(word)

    return JsonResponse({"scrambled": scrambled, "original": word})

# Home Page
def start(request):
    return render(request, "game/index.html")

# User Registration
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            return redirect("login")
        else:
            messages.error(request, "Registration failed. Please check the errors below.")
    else:
        form = RegisterForm()
    
    return render(request, "register.html", {"form": form})

# Profile Page
@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "profile.html", {"form": form, "profile": profile})

# Game session sharing
def play_share(request, uuid):
    word_instance = get_object_or_404(Word, uuid=uuid)
    scrambled = scramble_word(word_instance.word)
    return render(request, "game/play.html", {"scrambled": scrambled})

# Login View
def login_view(request):
    if request.user.is_authenticated:
        return redirect("start")

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect("start")
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})

# Logout View
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return render(request, "logout.html")

# Register View
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data["email"]
            user.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect("start")
        else:
            messages.error(request, "Registration failed. Please check the errors below.")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})
