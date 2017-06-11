import time, math
from django.utils.timezone import now, utc, localtime
from django.utils.datetime_safe import datetime
from django.db import models
from accounts.models import *


class Event(models.Model):
    e_user = models.ForeignKey(RdxUser, default=1, on_delete=models.CASCADE,
                               verbose_name='Created by')
    e_title = models.CharField(max_length=60, help_text='Max 60 character allowed.')
    e_date = models.DateField(default=None)
    e_time = models.TimeField(default=None)
    e_age_min = models.IntegerField(default=0)
    e_age_max = models.IntegerField(default=100)
    e_location = models.CharField(max_length=100, blank=False, default='Bangalore')
    e_details = models.TextField(null=False, blank=True)
    e_image = ProcessedImageField(upload_to=upload_image,
                                blank=True, null=True,
                                validators=[image_extension],
                                format='JPEG',
                                options={'quality': 70}
                                )
    e_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    e_sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    e_active = models.BooleanField(default=True)
    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-id",)

    def __str__(self):
        return str(self.id)

    def e_icon(self):
        if self.e_image != '':
            return "<img src='{}' width=50px>".format(self.e_image.url)
        else:
            return ''
    e_icon.allow_tags = True


class Joint(models.Model):
    j_user = models.ForeignKey(RdxUser, on_delete=models.CASCADE)
    j_event = models.ForeignKey(Event, on_delete=models.CASCADE)
    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-id",)

    def __str__(self):
        return str(self.id)


class Post(models.Model):
    p_user = models.ForeignKey(RdxUser, default=1, on_delete=models.CASCADE,
                               verbose_name='Posted by')
    p_sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE,
                                       blank=True, default=1)
    p_title = models.CharField(max_length=250, blank=False, null=False)
    p_date = models.DateField(default=None)
    p_time = models.TimeField(default=None)
    p_veg = models.BooleanField(default=True, verbose_name='Veg/Non-Veg')
    p_person = models.IntegerField(default=1)
    p_active = models.BooleanField(default=True)
    p_details = models.TextField(null=False, blank=True)
    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return str(self.id)

    def p_time_ago(self):
        if self.created:
            now_time = int(time.mktime(datetime.now().replace(tzinfo=utc).timetuple()))
            created = int(time.mktime(self.created.timetuple()))
            seconds = (now_time - created) - 19800
            if seconds > 86400:
                day = self.created.day
                suffix = {1: "st", 2: "nd", 3: "rd"}\
                    .get(day if (day < 20) else (day % 10), 'th')
                return format(self.created, "%d{0} %b{1}".format(suffix, ' %Y' \
                    if localtime(now()).year != self.created.year else ''))
            elif (seconds > 3600) and (seconds < 86400):
                hours = seconds / 3600
                return str(math.floor(hours)).zfill(2) + ' hrs ago'
            elif (seconds > 60) and (seconds < 3600):
                minutes = seconds / 60
                return str(math.floor(minutes)).zfill(1) + ' mins ago'
            else:
                return 'Just now'


class Comment(models.Model):
    c_user = models.ForeignKey(RdxUser, on_delete=models.CASCADE)
    c_post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=False)
    c_content = models.TextField()
    c_parent_comment = models.ForeignKey('self', null=True, blank=True,
                                         related_name='reply_set'
                                         )
    c_active = models.BooleanField(default=True)
    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.c_content + '-' + str(self.id)

    def c_time_ago(self):
        if self.created:
            now_time = int(time.mktime(datetime.now().replace(tzinfo=utc).timetuple()))
            created = int(time.mktime(self.created.timetuple()))
            seconds = (now_time - created) - 19800
            if seconds > 86400:
                day = self.created.day
                suffix = {1: "st", 2: "nd", 3: "rd"}\
                    .get(day if (day < 20) else (day % 10), 'th')
                return format(self.created, "%d{0} %b{1}".format(suffix, ' %Y' \
                    if localtime(now()).year != self.created.year else ''))
            elif (seconds > 3600) and (seconds < 86400):
                hours = seconds / 3600
                return str(math.floor(hours)).zfill(2) + ' hrs ago'
            elif (seconds > 60) and (seconds < 3600):
                minutes = seconds / 60
                return str(math.floor(minutes)).zfill(2) + ' mins ago'
            else:
                return 'Just now'