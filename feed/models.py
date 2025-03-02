import uuid
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from feed.managers import CustomUserManager

class User(AbstractBaseUser, PermissionsMixin):
    """ The user Model an extension of the Abstract user for
        values not defined in the built-in Django User model
    """

    class Role(models.TextChoices):
        NORMAL = "normal",
        ADMIN = "admin"
    
   
    user_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True, verbose_name="email address")
    password = models.CharField(max_length=128, null=True)
    role = models.CharField(choices=Role, default=Role.NORMAL, max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Model to represent posts
class Post(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')  # The user who created the post
    content = models.TextField()  # Content of the post
    created_at = models.DateTimeField(auto_now_add=True)  # Time when the post was created
    updated_at = models.DateTimeField(auto_now=True)  # Time when the post was last updated
    likes_count = models.PositiveIntegerField(default=0)  # Cached count for likes
    shares_count = models.PositiveIntegerField(default=0)  # Cached count for shares

    class Meta:
        db_table = 'feed_posts'
        ordering = ['-created_at']  # Posts will be ordered by creation time by default

    def __str__(self):
        return f"Post {self.id} by {self.user.first_name} {self.user.last_name}"

# Model to represent comments on a post
class Comment(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')  # User who commented
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')  # The post being commented on
    content = models.TextField()  # The content of the comment
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the comment was created
    parent_comment = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE) # For replies to comments

    class Meta:
        ordering = ['-created_at']  # Comments ordered by creation time (most recent first)
        db_table = 'feed_comments'

    def __str__(self):
        return f"Comment {self.id} on Post {self.post.id} by {self.user.first_name} {self.user.last_name}"


# Model to track interactions like "Likes" and "Shares"
class Interaction(models.Model):

    INTERACTION_TYPES = (
        ('like', 'Like'),
        ('share', 'Share'),
    )
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interactions')  # User who interacted
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='interactions')  # The post being interacted with
    interaction_type = models.CharField(max_length=10, choices=INTERACTION_TYPES)  # Type of interaction (like or share)
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the interaction occurred

    class Meta:
        db_table = 'feed_interactions'
        unique_together = ('user', 'post', 'interaction_type')  # Ensure one like or share per user/post

    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} {self.interaction_type}d Post {self.post.id}"
