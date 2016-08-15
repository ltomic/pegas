from rest_framework import serializers
from lark.models import Submission, Submission_test

class SubmissionSerializer(serializers.Serializer):
	id = serializers.IntegerField()
	date = serializers.DateTimeField()
	verdict = serializers.CharField(max_length=20)
	time = serializers.DecimalField(max_digits=6, decimal_places=2)
	memory = serializers.DecimalField(max_digits=6, decimal_places=2)

	def create(self, data):
		return Submission.objects.create(**data)

class Submission_testSerializer(serializers.Serializer):
	index = serializers.IntegerField()
	time = serializers.DecimalField(max_digits=6, decimal_places=2)
	memory = serializers.DecimalField(max_digits=6, decimal_places=2)
	verdict = serializers.CharField(max_length=30)

	def create(self, data):
		return Submission_test.objects.create(**data)
