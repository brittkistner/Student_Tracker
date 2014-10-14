from django.contrib.auth.models import AbstractUser
from django.db import models


class Teacher(AbstractUser):
    def __unicode__(self):
        return self.first_name


class Student(AbstractUser):
    def __unicode__(self):
        return self.first_name


class Class(models.Model):
    name = models.CharField(max_length=50)
    teacher = models.ForeignKey(Teacher, related_name="classes")
    student = models.ManyToManyField(Student, related_name="classes")
    class_start = models.DateTimeField()
    class_end = models.DateTimeField()


class CheckIn(models.Model):
    student = models.ForeignKey(Student, related_name="check_ins")
    class_name = models.ForeignKey(Class, related_name="check_ins")
    check_in_time = models.DateTimeField(auto_now_add=True)


class HelpMe(models.Model):
    student = models.ForeignKey(Student, related_name="help_mes")
    created_time = models.DateTimeField(auto_now_add=True)


