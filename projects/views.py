from re import template
from unicodedata import name
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm
from .utils import searchProjects, paginateProjects
from django.views import View


# def projects(request):
#     projects, search_query = searchProjects(request)
#     custom_range, projects = paginateProjects(request, projects, 6)

#     context = {'projects': projects, 'search_query': search_query,
#                'custom_range': custom_range}
#     return render(request, 'projects/projects.html', context)


class Projects(View):
    def get(self, request):
        projects, search_query = searchProjects(request)
        custom_range, projects = paginateProjects(request, projects, 6)

        context = {'projects': projects, 'search_query': search_query,
                   'custom_range': custom_range}
        return render(request, 'projects/projects.html', context)


# def project(request, pk):
#     projectObj = Project.objects.get(id=pk)
#     form = ReviewForm()
#     if request.method == 'POST':
#         form = ReviewForm(request.POST)
#         review = form.save(commit=False)
#         review.project = projectObj
#         review.owner = request.user.profile
#         review.save()

#         projectObj.getVoteCount

#         messages.success(request, 'Review added')
#         return redirect('project', pk=projectObj.id)

#     return render(request, 'projects/single-project.html', {'project': projectObj, 'form': form})


class SingleProject(View):
    def get(self, request, pk):
        projectObj = Project.objects.get(id=pk)
        form = ReviewForm()
        return render(request, 'projects/single-project.html', {'project': projectObj, 'form': form})

    def post(self, request, pk):
        projectObj = Project.objects.get(id=pk)
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectObj
        review.owner = request.user.profile
        review.save()

        projectObj.getVoteCount

        messages.success(request, 'Review added')
        return redirect('project', pk=projectObj.id)


# @login_required(login_url="login")
# def createProject(request):
#     # Get instance of user
#     profile = request.user.profile
#     form = ProjectForm()

#     if request.method == 'POST':
#         newtags = request.POST.get('newtags').replace(',', ' ').split()

#         form = ProjectForm(request.POST, request.FILES)
#         if form.is_valid():
#             # Associate user with project
#             project = form.save(commit=False)
#             project.owner = profile
#             project.save()

#             for tag in newtags:
#                 tag, created = Tag.objects.get_or_create(name=tag)
#                 project.tags.add(tag)

#             return redirect('account')

#     context = {'form': form}
#     return render(request, 'projects/project_form.html', context)


class CreateProject(View):
    def get(self, request):
        profile = request.user.profile
        form = ProjectForm()
        context = {'form': form}
        return render(request, 'projects/project_form.html', context)

    def post(self, request):
        profile = request.user.profile
        newtags = request.POST.get('newtags').replace(',', ' ').split()

        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            # Associate user with project
            project = form.save(commit=False)
            project.owner = profile
            project.save()

            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)

            return redirect('account')


# @login_required(login_url="login")
# def updateProject(request, pk):
#     # Verify user is owner to udpate/delete
#     profile = request.user.profile
#     project = profile.project_set.get(id=pk)
#     form = ProjectForm(instance=project)

#     if request.method == 'POST':
#         newtags = request.POST.get('newtags').replace(',', ' ').split()
#         form = ProjectForm(request.POST, request.FILES, instance=project)
#         if form.is_valid():
#             project = form.save()
#             for tag in newtags:
#                 tag, created = Tag.objects.get_or_create(name=tag)
#                 project.tags.add(tag)

#             return redirect('projects')

#     context = {'form': form, 'project': project}
#     return render(request, 'projects/project_form.html', context)


class UpdateProject(View):
    def get(self, request, pk):
        profile = request.user.profile
        project = profile.project_set.get(id=pk)
        form = ProjectForm(instance=project)
        context = {'form': form, 'project': project}
        return render(request, 'projects/project_form.html', context)

    def post(self, request, pk):
        profile = request.user.profile
        project = profile.project_set.get(id=pk)
        newtags = request.POST.get('newtags').replace(',', ' ').split()
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)

            return redirect('projects')


# @login_required(login_url="login")
# def deleteProject(request, pk):
#     profile = request.user.profile
#     project = profile.project_set.get(id=pk)
#     if request.method == 'POST':
#         project.delete()
#         return redirect('projects')
#     context = {'object': project}
#     return render(request, 'delete_template.html', context)


class DeleteProject(View):
    def get(self, request, pk):
        profile = request.user.profile
        project = profile.project_set.get(id=pk)
        context = {'object': project}
        return render(request, 'delete_template.html', context)

    def post(self, request, pk):
        profile = request.user.profile
        project = profile.project_set.get(id=pk)
        project.delete()
        return redirect('projects')
