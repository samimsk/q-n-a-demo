from django.conf.urls import url,include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from qna.views import (
	home,
	register,
	logout,
	question,
	upvote,
	remove_upvote,
	profile,
	user_answers,
	users_upvotes,
	upvoters_list,
	most_voted_question,
	most_voted_question_last_hour,


	condition,
	)


urlpatterns = [
    url(r'^$', home, name="home"),
    url(r'^login/$', auth_views.login, {'template_name': 'body/login.html'}, name="login"),
    url(r'^logout/$', logout, name="logout"),
    url(r'^register/$', register, name="register"),
    url(r'^profile/(?P<username>\w+)$', profile, name="profile"),
    url(r'^profile/(?P<username>\w+)/answers/$', user_answers, name="user_answers"),
    url(r'^profile/(?P<username>\w+)/upvotes/$', users_upvotes, name="users_upvotes"),
    url(r'^upvote/(?P<answer_id>\w+)/$', upvote, name="upvote"),
    url(r'^remove-upvote/(?P<answer_id>\w+)/$', remove_upvote, name="remove_upvote"),
    url(r'^qid=(?P<question_id>\w+)/$', question, name="question"),
    url(r'^most-voted-question/$', most_voted_question, name="most_voted_question"),
    url(r'^most-voted-question-of-the-hr/$', most_voted_question_last_hour, name="most_voted_question_last_hour"),
    url(r'^upvoters-list/ans_id=(?P<answer_id>\w+)$', upvoters_list, name="upvoters_list"),

    url(r'^condition/$', condition, name="condition"),

]