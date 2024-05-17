from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, LoginForm, CreateClaim
from .models import LoginUser, Claim

def home(request):
	if request.user.is_authenticated:
		administrator_group = Group.objects.get(name='Administrators')
		is_mod = administrator_group.user_set.filter(id=request.user.id).exists()
		if is_mod:
			return render(request, 'home.html', {'staff': is_mod})
		else:
			return render(request, 'home.html', {'user': request.user})
	else:
		return redirect('login')
	
def login_user(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.success(request, "You Have Successfully Logged In! Welcome!")
				return redirect('home')
			else:
				messages.error(request, 'There was an error with your login information. Try Again or Register!')
				return render(request, 'login.html', {'login':form})
	else:
		form = LoginForm()
		return render(request, 'login.html', {'login':form})

def logout_user(request):
	logout(request)
	messages.success(request, "You Have Been Logged Out...")
	return redirect('home')

def register_user(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			# Authenticate and login
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, "You Have Successfully Registered! Welcome!")
			return redirect('home')
	else:
		form = SignUpForm()
		return render(request, 'register.html', {'form':form})

	return render(request, 'register.html', {'form':form})

def claims(request):
	if request.user.is_authenticated:
		query = request.GET.get('search', '')
		searched = False
		if query:
			claims = Claim.objects.filter(claim_name__icontains=query).order_by('-id')
			searched = True
		else:
			claims = Claim.objects.order_by('-id')
		return render(request, 'claims.html', {'claims':claims, 'query':query, 'searched':searched})
	else:
		messages.success(request, "You must be logged in to use this page!")
		return redirect('home')

def claim(request, pk):
	if request.user.is_authenticated:
		claim = Claim.objects.get(id=pk)
		return render(request, 'claim.html', {'claim':claim})
	
def make_claim(request):
	form = CreateClaim(request.POST or None)
	if request.user.is_authenticated:
		if request.method == "POST":
			if form.is_valid():
				claim = form.save(commit=False)
				claim.username = request.user
				form.save()
				messages.success(request, "Claim staked!")
				return redirect('claims')
		return render(request, 'create_claim.html', {'form':form})
	else:
		messages.success(request, "You must be logged in to use this page!")
		return redirect('home')
	
def forums(request):
	if request.user.is_authenticated:
		return render(request, 'forums.html')
	


def profile(request):
	if request.user.is_authenticated:
		user = request.user
		return render(request, 'profile.html', {'user':user})
	else:
		messages.success(request, "You must be logged in to use this page!")
		return redirect('home')