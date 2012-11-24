from django.db import models
from django.contrib.auth.models import User


        
class UserProfile(models.Model):
        user = models.OneToOneField(User)
        activation_key = models.CharField(max_length=40)
        key_expires = models.DateTimeField()
        
        # necessario per il salvataggio dell'utente
        def create_user_profile(sender, instance, created, **kwargs):
                if created:
                UserProfile.objects.create(user=instance)

        post_save.connect(create_user_profile, sender=User)
