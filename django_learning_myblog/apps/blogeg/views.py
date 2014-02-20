# coding=utf-8


from itertools import groupby

from django.shortcuts import get_object_or_404,  resolve_url
from django.template import RequestContext, loader
from django.template.response import TemplateResponse
from django.http import HttpResponse, HttpResponseRedirect

from apps.blogeg.models import BlogPosts, Comment
from apps.blogeg.forms import CommentForm
# Create your views here.


START_USER_PERMISSIONS = ['comment']

def user_gain_perms(user, models_list):
    """
    User gets all permissions (create, change, delete) from list of models

    user = User
    models_list = list of models
    """
    permissions =[]
    for model in models_list:
        model_perm = Permission.objects.filter(codename__icontains=model)
        permissions += model_perm
    user.user_permissions = permissions

def index(request):
    blog_post_list = BlogPosts.objects.order_by('-publication_date'
                                                ).filter(is_arhive=False)

    template = loader.get_template('blogeg/index.html')
    context = RequestContext(request, {'blog_post_list': blog_post_list})
    return HttpResponse(template.render(context))


def post(request, pk):
    data = {}

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post_id = BlogPosts.objects.get(id=pk)
            comment.save()
            return HttpResponseRedirect('/' + pk + '/')
        else:
            data['form'] = CommentForm(request.POST)

    if not data.has_key('form'):
        data['form'] = CommentForm

    data['post'] = get_object_or_404(BlogPosts, id=pk)
    data['comments'] = Comment.objects.filter(is_hide=False,
                                              post_id=pk
                                              ).order_by('-publication_date')

    template = loader.get_template('blogeg/post.html')
    context = RequestContext(request, data)
    return HttpResponse(template.render(context))


def arhive(request):
    years = {}

    arhive_list = BlogPosts.objects.filter(is_arhive=True).values()
    arhive_list = sorted(arhive_list, key=lambda x: x['publication_date'])

    key_years = lambda x: x['publication_date'].year
    key_month = lambda x: x['publication_date'].month

    grouped_years = groupby(arhive_list, key=key_years)

    for year, months in grouped_years:
        years[year] = {}
        dict_of_year = years[year]

        grouped_months = groupby(months, key=key_month)

        for month, post in grouped_months:
            dict_of_year[month] = list(post)

    template = loader.get_template('blogeg/arhive.html')
    context = RequestContext(request, {'arhive': years})

    return HttpResponse(template.render(context))
