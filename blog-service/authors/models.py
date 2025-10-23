from django.db import models


class Author(models.Model):
    display_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['display_name']
        indexes = [
            models.Index(fields=['email']),
        ]
    
    def __str__(self):
        return self.display_name
