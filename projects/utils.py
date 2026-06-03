from django.db.models import Q
from.models import Project, Tag
from django.core.paginator import Paginator


def searchProjects(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    tags = Tag.objects.filter(name__icontains=search_query)

    projects = Project.objects.distinct().filter(Q(title__icontains=search_query) |
        Q(decription__icontains=search_query) |
        Q(tags__in=tags))
    
    
    return search_query, projects


def pagination(request, queryset):

    page = request.GET.get('page')
    
    p = Paginator(queryset, 1)

    return p.get_page(page)

