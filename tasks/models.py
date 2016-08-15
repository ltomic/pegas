from django.db import models

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
