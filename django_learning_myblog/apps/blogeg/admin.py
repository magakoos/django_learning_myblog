from django.contrib import admin
from apps.blogeg.models import BlogAutors, BlogPosts, Comment
# Register your models here.


class BlogPostsAdmin(admin.ModelAdmin):
    fields = ('autor', ('label', 'is_arhive'), 'content', 'publication_date', )

    # list_display = ('label','is_publised', 'publication_date', 'is_arhive')
    # list_readonly_fields = ('is_publised')
    list_display = ('label', 'publication_date', 'is_arhive')
    list_editable = ['is_arhive']
    list_filter = ('is_arhive', 'publication_date')


class BlogAutorAdmin(admin.ModelAdmin):
    fields = ['name']


admin.site.register(BlogPosts, BlogPostsAdmin)
admin.site.register(BlogAutors, BlogAutorAdmin)
admin.site.register(Comment)
