from django import forms 
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Question, Answer

class RegistrationForm(forms.Form):
    username = forms.CharField(label = 'Enter Username', min_length = 4, max_length=140)
    email = forms.EmailField(label = 'Enter email')
    password1 = forms.CharField(label = 'Enter password', widget = forms.PasswordInput )
    password2 = forms.CharField(label = 'Confirm password', widget = forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username']
        user_instance = User.objects.filter(username = username)
        if user_instance.exists():
            raise ValidationError("Username already exist")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        user_instance = User.objects.filter(email = email)
        if user_instance.exists():
            raise ValidationError("Email already registered!")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 != password2:
            raise ValidationError("Password did not match!")
        return password2

    def save(self, commit = True):
        user_instance = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password2']
            )

        return user_instance


class QuestionForm(forms.Form):
    title = forms.CharField(widget = forms.Textarea(
        attrs = {'rows': '2', 
                'class': 'form-control bordr',
                'placeholder': 'Type in your question',}),
        error_messages={'required': 'You cannot ask an empty question!!'})


    def save(self, commit = True):
        print(self.cleaned_data)
        title = self.cleaned_data['title']
        question_instance = Question.objects.create(title=title)
        question_instance.save()
        return question_instance

class AnswerForm(forms.Form):
    detail = forms.CharField(widget = forms.Textarea(
        attrs = {'rows': '2', 
                'class': 'form-control bordr',
                'placeholder': 'Type in your answer!',}),
        error_messages={'required': 'You cannot post an empty answer!'})

    def save(self, commit = True):
        detail = self.cleaned_data['detail']
        answer_instance = Answer.objects.create(detail=detail)
        answer_instance.save()
        return answer_instance






