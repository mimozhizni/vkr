# Generated by Django 2.2.5 on 2021-06-05 17:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0010_auto_20210605_1711'),
    ]

    operations = [
        migrations.CreateModel(
            name='Step',
            fields=[
                ('step_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('short_description', models.CharField(max_length=2000)),
                ('note_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task.Note')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('note_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('short_description', models.CharField(max_length=2000)),
                ('image', models.ImageField(upload_to='')),
                ('step_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task.Step')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Image_step',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='steps')),
                ('step', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='task.Step')),
            ],
        ),
        migrations.CreateModel(
            name='Image_note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='notes')),
                ('note_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='task.Task')),
            ],
        ),
        migrations.CreateModel(
            name='Files_task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to='notes')),
                ('note_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='task.Task')),
            ],
        ),
        migrations.CreateModel(
            name='Files_step',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to='steps')),
                ('step', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='task.Step')),
            ],
            options={
                'verbose_name': '??????????',
                'verbose_name_plural': '??????????',
            },
        ),
    ]
