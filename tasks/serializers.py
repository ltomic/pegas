from rest_framework import serializers
from tasks.models import Task

class TaskSerializer(serializers.Serializer):
	name = serializers.CharField(max_length=20)

	def create(self, data):
		return Task.objects.create(**data)
