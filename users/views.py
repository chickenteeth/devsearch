from multiprocessing import context
from re import search
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile, Message
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from .utils import searchProfiles, paginateProfiles
from django.views import View


def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            messages.error(request, 'Username or Password is incorrect')

    return render(request, 'users/login_register.html')


# class LoginUser(View):
#     def get(self, request):
#         page = 'login'
#         if request.user.is_authenticated:
#             return redirect('profiles')

#         return render(request, 'users/login_register.html')

#     def post(self, request):
#         username = request.POST['username'].lower()
#         password = request.POST['password']

#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             return redirect(request.GET['next'] if 'next' in request.GET else 'account')
#         else:
#             messages.error(request, 'Username or Password is incorrect')
#             return render(request, 'users/login_register.html')


def logoutUser(request):
    logout(request)
    messages.info(request, 'User successfully logged out')
    return redirect('login')

# class LogoutUser(View):
#     def get(self, request):
#         logout(request)
#         messages.info(request, 'User successfully logged out')
#         return redirect('login')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Create instance of user to use later
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account created')

            login(request, user)
            return redirect('edit-account')
        else:
            messages.error(
                request, 'An error has occurred during registration')

    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)


# class RegisterUser(View):
#     def get(self, request):
#         page = 'register'
#         form = CustomUserCreationForm()
#         context = {'page': page, 'form': form}
#         return render(request, 'users/login_register.html', context)

#     def post(self, request):
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             # Create instance of user to use later
#             user = form.save(commit=False)
#             user.username = user.username.lower()
#             user.save()

#             messages.success(request, 'User account created')

#             login(request, user)
#             return redirect('edit-account')
#         else:
#             messages.error(
#                 request, 'An error has occurred during registration')
#             return render(request, 'users/login_register.html', context)


def profiles(request):
    profiles, search_query = searchProfiles(request)
    custom_range, profiles = paginateProfiles(request, profiles, 6)
    context = {'profiles': profiles, 'search_query': search_query,
               'custom_range': custom_range}
    return render(request, 'users/profiles.html', context)


# class AllProfiles(View):
#     def get(self, request):
#         profiles, search_query = searchProfiles(request)
#         custom_range, profiles = paginateProfiles(request, profiles, 6)
#         context = {'profiles': profiles, 'search_query': search_query,
#                    'custom_range': custom_range}
#         return render(request, 'users/profiles.html', context)


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")
    context = {'profile': profile, 'topSkills': topSkills,
               'otherSkills': otherSkills}
    return render(request, 'users/user-profile.html', context)


# class UserProfile(View):
#     def get(self, request, pk):
#         profile = Profile.objects.get(id=pk)
#         topSkills = profile.skill_set.exclude(description__exact="")
#         otherSkills = profile.skill_set.filter(description="")
#         context = {'profile': profile, 'topSkills': topSkills,
#                    'otherSkills': otherSkills}
#         return render(request, 'users/user-profile.html', context)


@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    context = {'profile': profile, 'skills': skills, 'projects': projects}
    return render(request, 'users/account.html', context)


# class UserAccount(View):
#     def get(self, request):
#         profile = request.user.profile
#         skills = profile.skill_set.all()
#         projects = profile.project_set.all()
#         context = {'profile': profile, 'skills': skills, 'projects': projects}
#         return render(request, 'users/account.html', context)


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {'form': form}
    return render(request, 'users/profile_form.html', context)


# class EditAccount(View):
#     def get(self, request):
#         profile = request.user.profile
#         form = ProfileForm(instance=profile)
#         context = {'form': form}
#         return render(request, 'users/profile_form.html', context)

#     def post(self, request):
#         profile = request.user.profile
#         form = ProfileForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             form.save()
#             return redirect('account')


@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill Added Successfully')
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


# class CreateSkill(View):
#     def get(self, request):
#         profile = request.user.profile
#         form = SkillForm
#         context = {'form': form}
#         return render(request, 'users/skill_form.html', context)

#     def post(self, request):
#         profile = request.user.profile
#         form = SkillForm(request.POST)
#         if form.is_valid():
#             skill = form.save(commit=False)
#             skill.owner = profile
#             skill.save()
#             messages.success(request, 'Skill Added Successfully')
#             return redirect('account')


@login_required(login_url='login')
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill Updated Successfully')
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


# class UpdateSkill(View):
#     def get(self, request, pk):
#         profile = request.user.profile
#         skill = profile.skill_set.get(id=pk)
#         form = SkillForm(instance=skill)
#         context = {'form': form}
#         return render(request, 'users/skill_form.html', context)

#     def post(self, request, pk):
#         profile = request.user.profile
#         skill = profile.skill_set.get(id=pk)
#         form = SkillForm(request.POST, instance=skill)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Skill Updated Successfully')
#             return redirect('account')


@login_required(login_url='login')
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)

    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill Deleted')
        return redirect('account')

    context = {'object': skill}
    return render(request, 'delete_template.html', context)


# class DeleteSkill(View):
#     def get(self, request, pk):
#         profile = request.user.profile
#         skill = profile.skill_set.get(id=pk)
#         context = {'object': skill}
#         return render(request, 'delete_template.html', context)

#     def post(self, request, pk):
#         profile = request.user.profile
#         skill = profile.skill_set.get(id=pk)
#         skill.delete()
#         messages.success(request, 'Skill Deleted')
#         return redirect('account')


@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messageRequest = profile.messages.all()
    unreadCount = messageRequest.filter(is_read=False).count()
    context = {'messageRequest': messageRequest, 'unreadCount': unreadCount}
    return render(request, 'users/inbox.html', context)


# class Inbox(View):
#     def get(self, request):
#         profile = request.user.profile
#         messageRequest = profile.messages.all()
#         unreadCount = messageRequest.filter(is_read=False).count()
#         context = {'messageRequest': messageRequest,
#                    'unreadCount': unreadCount}
#         return render(request, 'users/inbox.html', context)


@login_required(login_url='login')
def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {'message': message}
    return render(request, 'users/message.html', context)


# class ViewMessage(View):
#     def get(self, request, pk):
#         profile = request.user.profile
#         message = profile.messages.get(id=pk)
#         if message.is_read == False:
#             message.is_read = True
#             message.save()
#         context = {'message': message}
#         return render(request, 'users/message.html', context)


def createMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email

            message.save()
            messages.success(request, 'Your message has been sent')
            return redirect('user-profile', pk=recipient.id)

    context = {'recipient': recipient, 'form': form}
    return render(request, 'users/message_form.html', context)


# class CreateMessage(View):
#     def get(self, request, pk):
#         recipient = Profile.objects.get(id=pk)
#         form = MessageForm()

#         try:
#             sender = request.user.profile
#         except:
#             sender = None

#         context = {'recipient': recipient, 'form': form}
#         return render(request, 'users/message_form.html', context)

#     def post(self, request, pk):

#         try:
#             sender = request.user.profile
#         except:
#             sender = None

#         recipient = Profile.objects.get(id=pk)
#         form = MessageForm(request.POST)
#         if form.is_valid():
#             message = form.save(commit=False)
#             message.sender = sender
#             message.recipient = recipient

#             if sender:
#                 message.name = sender.name
#                 message.email = sender.email

#             message.save()
#             messages.success(request, 'Your message has been sent')
#             return redirect('user-profile', pk=recipient.id)
