from django.contrib import admin
from .models import *


class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'e_title', 'e_user', 'e_icon', 'e_category',
                    'e_sub_category', 'e_active')
    list_per_page = 50

    class Meta:
        model = Event


class JointAdmin(admin.ModelAdmin):
    list_display = ('id', 'j_user', 'j_event')
    list_per_page = 50

    class Meta:
        model = Joint


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'p_user', 'p_title', 'p_veg', 'p_active')
    list_per_page = 50

    class Meta:
        model = Post


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'c_user', 'c_post', 'c_content', 'c_active')
    list_per_page = 50

    class Meta:
        model = Comment


admin.site.register(Event, EventAdmin)
admin.site.register(Joint, JointAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
