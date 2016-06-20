from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class UserProfile(models.Model):
	user = models.OneToOneField(User)

	quote = models.CharField(max_length=140)

	def __unicode__(self):
		return self.user.username

def checker_path(instance, filename):
	ret = '/'.join([
			'test', 
			instance.name,
			'checker'
			])
	return ret
			
class Task(models.Model):
	name = models.CharField(max_length=30, unique=True)
	url = models.CharField(max_length=30, unique=True)
	time_limit = models.DecimalField(max_digits=6, decimal_places=3, default=0)
	memory_limit = models.IntegerField(default=64)
	link = models.URLField(max_length=200, default='')
	tip = models.IntegerField(default=0)
	checker = models.FileField(upload_to=checker_path)
	checker_lang = models.CharField(max_length=10, default='')

	def __unicode__(self):
		return self.name

class TestCase(models.Model):
	task = models.ForeignKey(Task)
	index = models.CharField(max_length=5)
	ulaz = models.FileField()
	izlaz = models.FileField()
	is_dummy = models.BooleanField(default=0)

	def __unicode__(self):
		return self.task.name + ":" + str(self.index)

def content_file_name(instance, filename):
	ret = '/'.join([
			'content', 
			instance.user.user.username,
			instance.task.url,
			filename])
	return ret

class Submission(models.Model):
	code = models.FileField(upload_to=content_file_name)
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


