from datetime import timezone
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Category Model
class Category(models.Model):
    category_name = models.CharField(max_length=30)  # Name of the category

    user = models.ForeignKey(
        User,                           # Links category to a specific user
        on_delete=models.CASCADE,       # Deletes category if the user is deleted
        related_name='categories',      # Allows reverse lookup: user.categories.all()
        null=True,                      # Optional field
        blank=True                      # Optional in forms
    )

    def __str__(self) -> str:
        return self.category_name       # String representation of the category

    class Meta:
        verbose_name = 'Category'        # Singular name in Django Admin
        verbose_name_plural = 'Categories'  # Plural name in Django Admin


# Contact Model
class Contact(models.Model):
    first_name = models.CharField(max_length=30)      # First name of contact
    last_name = models.CharField(max_length=30)       # Last name of contact
    phone = models.CharField(max_length=20)           # Phone number
    email = models.EmailField(blank=True, max_length=254)  # Optional email
    created_date = models.DateTimeField(default=timezone.now)  # Auto timestamp on creation
    description = models.TextField(blank=True)        # Optional description
    show = models.BooleanField(default=True)          # Whether the contact is visible
    picture = models.ImageField(                      # Optional image upload
        blank=True,
        upload_to='pictures/%Y/%m/'                   # Organized by year/month
    )
    category = models.ForeignKey(                     # Optional category link
        Category,
        on_delete=models.SET_NULL,                    # Keep contact if category deleted
        null=True,
        blank=True
    )

    user = models.ForeignKey(                         # Link contact to a user
        User,
        on_delete=models.CASCADE,                     # Delete contact if user is deleted
        related_name='contacts',                      # Allows reverse lookup: user.contacts.all()
        null=True,
        blank=True
    )

    def __str__(self) -> str:
        # String representation combining first and last name
        return f'{self.first_name} {self.last_name}'

