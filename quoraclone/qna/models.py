from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
	title = models.TextField()
	detail = models.TextField(blank=True, null=True)
	question_by = models.ForeignKey(User, default=1, related_name='question_by', blank=True, null=True)
	time = models.DateTimeField(auto_now = True)

	def __str__(self):
		return self.title

	class Meta:
		ordering = ["-time"]


class Answer(models.Model):
	answer_by = models.ForeignKey(User, default=1, related_name='answer_by', blank=True, null=True)
	question_name = models.ForeignKey(Question, on_delete = models.CASCADE, related_name='question_name', blank=True, null=True)
	detail = models.TextField()
	time = models.DateTimeField(auto_now = True)
	def __str__(self):
		return self.detail



	class Meta:
		ordering = ["-time"]

class Upvote(models.Model):
	upvoted_by = models.ForeignKey(User, default=1, related_name='upvoted_by', blank=True, null=True )
	upvoted_question = models.ForeignKey(Question, on_delete = models.CASCADE, related_name='upvoted_question')
	upvoted_answer = models.ForeignKey(Answer, on_delete = models.CASCADE, related_name='upvoted_answer')
	time = models.DateTimeField(auto_now = True)

	def __str__(self):
		return self.upvoted_by.username









