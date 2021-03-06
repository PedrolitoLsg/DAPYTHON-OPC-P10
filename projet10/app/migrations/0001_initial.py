# Generated by Django 4.0 on 2022-01-19 18:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUsers',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=40, unique=True)),
                ('first_name', models.CharField(max_length=40)),
                ('last_name', models.CharField(max_length=40)),
                ('password', models.CharField(max_length=80)),
                ('is_active', models.BooleanField(default=True)),
                ('staff', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Projects',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=350)),
                ('type', models.CharField(choices=[('back-end', 'Be'), ('front-end', 'Fe'), ('IOS', 'Ios'), ('Android', 'Android')], max_length=40)),
                ('author_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.customusers')),
            ],
        ),
        migrations.CreateModel(
            name='Issues',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=180)),
                ('desc', models.CharField(max_length=500)),
                ('tag', models.CharField(choices=[('Bug', 'B'), ('Improvement', 'I'), ('Task', 'T')], max_length=40)),
                ('priority', models.CharField(choices=[('High', 'H'), ('Medium', 'M'), ('Low', 'L')], max_length=40)),
                ('status', models.CharField(choices=[('To-do', 'Td'), ('Work In Progress', 'Wip'), ('Done', 'Done')], max_length=40)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('assignee_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issue_assignee', to='app.customusers')),
                ('author_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issue_author', to='app.customusers')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.projects')),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=350)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('author_user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.customusers')),
                ('issue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.issues')),
            ],
        ),
        migrations.CreateModel(
            name='Contributors',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('permission', models.CharField(max_length=80)),
                ('role', models.CharField(max_length=80)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.projects')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.customusers')),
            ],
            options={
                'unique_together': {('user', 'project')},
            },
        ),
    ]
