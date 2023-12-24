from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    upload_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('Profile', on_delete=models.DO_NOTHING)
    like = models.IntegerField()
    tags = models.ManyToManyField('Tag', related_name='questions')


class Answer(models.Model):
    content = models.TextField()
    valid = models.BooleanField()
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    user = models.ForeignKey('Profile', on_delete=models.DO_NOTHING)
    like = models.IntegerField()


class Tag(models.Model):
    title = models.CharField(max_length=255)


class Profile(models.Model):
    photo = models.ImageField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class QuestionLike(models.Model):
    question = models.ForeignKey('Question', on_delete=models.DO_NOTHING)
    user = models.ForeignKey('Profile', on_delete=models.CASCADE)


class AnswerLike(models.Model):
    answer = models.ForeignKey('Answer', on_delete=models.DO_NOTHING)
    user = models.ForeignKey('Profile', on_delete=models.CASCADE)
