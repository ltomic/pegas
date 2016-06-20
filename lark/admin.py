from django.contrib import admin
from lark.models import UserProfile, Task, TestCase, Submission, Submission_judge

class TestCaseInline(admin.TabularInline):
	model = TestCase
	extra = 0

class TaskAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['name', 'url', 'time_limit', 'memory_limit', 'checker']}),
	]
	inlines = [TestCaseInline]

admin.site.register(UserProfile)
admin.site.register(Task, TaskAdmin)
admin.site.register(Submission)
admin.site.register(Submission_judge)
