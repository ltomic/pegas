from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from user.models import UserProfile
from tasks.models import Task

def content_file_name(instance, filename):
    ret = '/'.join([
	'content', 
	instance.user.user.username,
	instance.task.url,
	filename])
    return ret

class Language(models.Model):
    name = models.CharField(max_length=20, default='')
    short = models.CharField(max_length=20, default='')
    extension = models.CharField(max_length=3, default='')
    cmd = models.CharField(max_length=200, default='')

    def __unicode__(self):
        return self.name

class Submission(models.Model):
    code = models.FileField(upload_to=content_file_name)
    lang = models.ForeignKey(Language)
    date = models.DateTimeField()
    user = models.ForeignKey(UserProfile)
    task = models.ForeignKey(Task)
    verdict = models.CharField(max_length=30, default='In queue')
    time = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    memory = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def __unicode__(self):
    	return self.user.user.username + ":" + self.task.name

class Submission_test(models.Model):
    sub = models.ForeignKey(Submission)
    index = models.CharField(max_length=5)
    time = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    memory = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    verdict = models.CharField(max_length=30, default=0)
    series = models.IntegerField(default=0)
	
class Submission_judge(models.Model):
    sub = models.OneToOneField(Submission)

    def __unicode__(self):
    	return str(self.sub.date) + ":" + self.sub.task.name
