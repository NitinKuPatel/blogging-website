from django.db import models
from django.contrib.auth.models import User, AbstractUser, Group, Permission
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import get_user_model



# Create your models here.
class CustomUser(AbstractUser):
    address = models.TextField(blank=True, null=True)
    contact = models.CharField(max_length=15, blank=True, null=True)
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_groups_set",  # Avoid conflict with auth.User.groups
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions",  # Avoid conflict with auth.User.user_permissions
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

class CustomManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter()


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=256)
    slug = models.SlugField(max_length=264,unique_for_date='publish')
    author = models.ForeignKey(CustomUser, related_name='blog_posts', on_delete=models.CASCADE)

    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,choices = STATUS_CHOICES,default='draft')
    objects = CustomManager()

    class Meta:
        ordering = ('publish',)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blogdetail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])
    

class files(models.Model):

    file_name=models.CharField(max_length=20)
    person = models.ForeignKey(Post, related_name="uploaded_files",on_delete=models.CASCADE)
    file =models.FileField(upload_to='file/',max_length=264, null=True)
    uploaded = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now =True)

    def __str__(self):
        return self.file_name
    def get_absolute_url(self):
        return reverse('file_detail', kwargs={'pk': self.pk})

