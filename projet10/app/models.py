from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.db.models import CharField, EmailField, ForeignKey, DateTimeField
from django.contrib.auth.models import PermissionsMixin
from .managers import CustomUsersManager


class CustomUsers(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True)
    username = None
    email = EmailField(max_length=40, unique=True)
    first_name = CharField(max_length=40)
    last_name = CharField(max_length=40)
    password = CharField(max_length=80)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    objects = CustomUsersManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    list_filter = ('staff', 'admin')
    list_display = ('user_id', 'first-name', 'last_name')
    ordering = ('user_id')

    @property
    def is_staff(self):
        return self.staff


class Projects(models.Model):
    class Types(models.TextChoices):
        BE = 'back-end'
        FE = 'front-end'
        IOS = 'IOS'
        ANDROID = 'Android'

    id = models.BigAutoField(primary_key=True)
    title = CharField(max_length=100)
    description = CharField(max_length=350)
    type = CharField(max_length=40, choices=Types.choices)
    author_user = ForeignKey(to=CustomUsers, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Contributors(models.Model):
    class Role(models.TextChoices):
        AUTHOR = 'Author'
        CONTRIB = 'Contributor'

    id = models.BigAutoField(primary_key=True)
    user = ForeignKey(to=CustomUsers, on_delete=models.CASCADE)
    project = ForeignKey(to=Projects, on_delete=models.CASCADE)
    permission = CharField(max_length=80)
    role = CharField(max_length=11, choices=Role.choices)

    class Meta:
        unique_together = ['user', 'project']


class Issues(models.Model):
    class Priorities(models.TextChoices):
        H = 'High'
        M = 'Medium'
        L = 'Low'

    class Tags(models.TextChoices):
        B = 'Bug'
        I = 'Improvement'
        T = 'Task'

    class Statuses(models.TextChoices):
        TD = 'To-do'
        WIP = 'Work In Progress'
        DONE = 'Done'

    id = models.BigAutoField(primary_key=True)
    title = CharField(max_length=180)
    desc = CharField(max_length=500)
    tag = CharField(max_length=40, choices=Tags.choices)
    priority = CharField(max_length=40, choices=Priorities.choices)
    project = ForeignKey(to=Projects, on_delete=models.CASCADE)
    status = CharField(max_length=40, choices=Statuses.choices)
    author_user = ForeignKey(to=CustomUsers, on_delete=models.CASCADE, related_name='issue_author')
    assignee_user = ForeignKey(to=CustomUsers, on_delete=models.CASCADE, related_name='issue_assignee')
    created_time = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comments(models.Model):
    id = models.BigAutoField(primary_key=True)
    issue = ForeignKey(to=Issues, on_delete=models.CASCADE)
    description = CharField(max_length=350)
    author_user_id = ForeignKey(to=CustomUsers, on_delete=models.CASCADE)
    created_time = DateTimeField(auto_now_add=True)
