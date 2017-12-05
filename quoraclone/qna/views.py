from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth as permissionauth
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from qna.forms import (
	RegistrationForm,
	QuestionForm,
	AnswerForm
	)
from django.core.paginator import Paginator
from .models import (
	Question,
	Answer,
	Upvote,
	)

def home(request):
	if request.user.is_authenticated():
		context = {}
		form = QuestionForm(request.POST or None)
		context['form'] = form
		question_list = Question.objects.all()
		page = request.GET.get('page', 1)
		paginator = Paginator(question_list, 9)
		try:
			question_list = paginator.page(page)
		except PageNotAnInteger:
			question_list = paginator.page(1)
		except EmptyPge:
			question_list = paginator.page(paginator.num_pages)
		context['question_list'] = question_list

		if form.is_valid():
			question_instance = form.save(commit=False)
			question_instance.question_by = request.user
			question_instance.save()
			context['form'] = QuestionForm(None)
			context['success_message'] = "Your Question has been posted!"
			return render(request, 'body/homeloggedin.html', context)


		return render(request, 'body/homeloggedin.html', context)

	return render(request, 'body/home.html', {})

def register(request):
	form = RegistrationForm(request.POST or None)
	if form.is_valid():
		user = form.save(commit=False)
		password = form.cleaned_data.get('password2')
		user.set_password(password)
		user.save()
		return redirect("/login")
	return render(request, 'body/register.html', {'form': form })

def question(request, question_id):
	question_instance = Question.objects.get(id= question_id)
	context = {}
	context['question'] = question_instance
	form = AnswerForm(request.POST or None)
	if form.is_valid():
		if request.user.is_authenticated():
			print("if")			
			answer_instance = form.save(commit=False)
			answer_instance.question_name = question_instance
			answer_instance.answer_by = request.user
			answer_instance.save()
			context['success_message'] = "Your answer has been posted!"
			context['form'] = AnswerForm(None)
			return render(request, 'body/question.html', context)
		else:
			print("else")
			return redirect("/login")

	context['form'] = form 
	return render(request, 'body/question.html', context)

@login_required(login_url='/login/')
def upvote(request, answer_id):
	answer_instance = Answer.objects.get(id = answer_id)
	question_instance = answer_instance.question_name
	upvote_instance = Upvote.objects.create(
		upvoted_by=request.user, 
		upvoted_question=question_instance,
		upvoted_answer=answer_instance)
	upvote_instance.save()
	return redirect(request.META['HTTP_REFERER'])
	
@login_required(login_url='/login/')
def remove_upvote(request, answer_id):
	answer_instance = Answer.objects.get(id = answer_id)
	upvote_instance = Upvote.objects.get(upvoted_answer = answer_instance, upvoted_by = request.user)
	upvote_instance.delete()
	return redirect(request.META['HTTP_REFERER'])

def profile(request, username):
	user_instance = User.objects.get(username = username)
	context = {}
	question_list = user_instance.question_by.all()
	print(question_list)
	page = request.GET.get('page', 1)
	paginator = Paginator(question_list, 9)
	try:
		question_list = paginator.page(page)
	except PageNotAnInteger:
		question_list = paginator.page(1)
	except EmptyPge:
		question_list = paginator.page(paginator.num_pages)
	context['question_list'] = question_list
	context['user_details'] = user_instance
	print(question_list)
	return render(request, 'body/profile.html', context)

def user_answers(request, username):
	user_instance = User.objects.get(username = username)
	context = {}
	answers_list = user_instance.answer_by.all()
	page = request.GET.get('page', 1)
	paginator = Paginator(answers_list, 9)
	try:
		answers_list = paginator.page(page)
	except PageNotAnInteger:
		answers_list = paginator.page(1)
	except EmptyPge:
		answers_list = paginator.page(paginator.num_pages)
	context['answers_list'] = answers_list
	context['user_details'] = user_instance
	return render(request, 'body/user_answer.html', context)

def users_upvotes(request, username):
	user_instance = User.objects.get(username = username)
	context = {}
	upvoted_answers_list = user_instance.upvoted_by.all()
	page = request.GET.get('page', 1)
	paginator = Paginator(upvoted_answers_list, 9)
	try:
		upvoted_answers_list = paginator.page(page)
	except PageNotAnInteger:
		upvoted_answers_list = paginator.page(1)
	except EmptyPge:
		upvoted_answers_list = paginator.page(paginator.num_pages)
	context['upvoted_answers_list'] = upvoted_answers_list
	context['user_details'] = user_instance
	return render(request, 'body/user_upvoted_answers.html', context)

def upvoters_list(request, answer_id):
	answer_instance = Answer.objects.get(id = answer_id)
	upvoters_list = answer_instance.upvoted_answer.all()
	context = {}
	context['upvoters_list'] = upvoters_list
	return render(request, 'body/upvoters_list.html', context)

def most_voted_question(request):
	context = {}
	question_list = Question.objects.all()
	max = 0
	most_upvoted_question = None
	for question in question_list:
		if(question.upvoted_question.all().count() > max):
			max = question.upvoted_question.all().count()
			most_upvoted_question = question
	print(most_upvoted_question)
	context['most_upvoted_question'] = most_upvoted_question
	context['title'] = "Most voted question of the hour"
	print(context)
	return render(request, 'body/most_voted_question.html', context)

def most_voted_question_last_hour(request):
	context = {}
	time_diff = datetime.now() - timedelta(hours=1)
	question_list = Question.objects.all()
	max = 0
	most_upvoted_question = None
	for question in question_list:
		if(Upvote.objects.filter(time__lt=time_diff, upvoted_question=question).count() > max):
			max = question.upvoted_question.all().count()
			most_upvoted_question = question
	print(most_upvoted_question)
	context['most_upvoted_question'] = most_upvoted_question
	context['title'] = "Most voted question of the hour"
	print(context)
	return render(request, 'body/most_voted_question.html', context)

def logout(request):
	permissionauth.logout(request)
	return redirect('/')





def condition(request):
	return render(request, 'body/condition.html', {})




	
