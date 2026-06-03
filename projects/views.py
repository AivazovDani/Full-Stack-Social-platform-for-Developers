from django.shortcuts import redirect, render
from .models import Project
from .form import ProjectForm, ReviewForm
from django.contrib.auth.decorators import login_required
from .utils import searchProjects, pagination
from django.contrib import messages




# Create your views here.


def projects(request):
    search_query, projects = searchProjects(request)
    p = pagination(request, projects)
    
    context = {'projects': p, 'search_query': search_query, 'p': p}

    return render(request, 'projects/projects.html', context=context)

def singleProject(request, pk):
    project = Project.objects.get(id=pk)
    
    project.getVotes()
    form = ReviewForm()
    already_reviewed = ''

    if request.user.is_authenticated:
        profile = request.user.profile
        already_reviewed = project.reviews.filter(owner=profile).exists()


        if request.method == 'POST':
            form = ReviewForm(request.POST)

            if form.is_valid():
                review = form.save(commit=False)
                review.project = project
                review.owner = profile
        
                review.save()
            

                return redirect('account-page')

    return render(request, 'projects/single-project.html', {'project': project, 'form':form, 'already_reviewed': already_reviewed})

@login_required(login_url='login')
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)

        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            form.save()
            messages.success(request, 'Project created successfully')

            return redirect('projects')
        
    return render(request, 'projects/add_project.html', {'form': form})

@login_required(login_url='login')
def editProject(request, pk):
    profile = request.user.profile
    project = profile.projects.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)

        if form.is_valid():
            project = form.save()
            return redirect('projects')
        
    return render(request, 'projects/edit_project.html', {'form': form, 'project': project})

@login_required(login_url='login')
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.projects.get(id=pk)


    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Account edited successfully')
        return redirect('account-page')


    return render(request, 'projects/delete_project.html', {'project': project})