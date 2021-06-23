from colorfield.fields import ColorField
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Q
# Create your models here.
from django.forms import fields
from datetime import date
from django.utils.html import format_html




class Image(models.Model):
    id_image = models.AutoField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='users/', default='/users/default.png')



class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ForeignKey(Image, related_name='img', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.last_name + ' ' + self.user.first_name

class Theme(models.Model):
    id_theme = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    short_description = models.CharField(max_length=2000)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name



class Note(models.Model):
    id_task = models.AutoField(primary_key=True)
    id_theme = models.ForeignKey(Theme, related_name='theme', on_delete=models.CASCADE, blank = True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    short_description = models.CharField(max_length=2000)
    deadline = models.DateField( ("Date"), default=date.today, blank=False)
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Step(models.Model):
    step_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    note_id = models.ForeignKey(Note, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    short_description = models.CharField(max_length=2000)

class Files_step(models.Model):

    file = models.FileField(upload_to='steps', blank=True, null=True)
    step = models.ForeignKey(Step, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Файлы"
        verbose_name_plural = "Файлы"

    def __str__(self):
        return self.file.name

class Image_step(models.Model):
    image = models.ImageField(upload_to='steps', blank=True, null=True)
    step = models.ForeignKey(Step, blank=True, null=True, on_delete=models.CASCADE)
    def __str__(self):
        return self.image.name

class Task(models.Model):
    note_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    step_id = models.ForeignKey(Step, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    short_description = models.CharField(max_length=2000)
    image = models.ImageField()


class Files_task(models.Model):
    file = models.FileField(upload_to='notes', blank=True, null=True)
    note_id = models.ForeignKey(Task, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.file.name

class Image_note(models.Model):
    image = models.ImageField(upload_to='notes', blank=True, null=True)
    note_id = models.ForeignKey(Task, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.image.name

