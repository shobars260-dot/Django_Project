from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


# signals.py (The definitive version)
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


# 1. Signal to Create the Profile 
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# 2. Signal to Save the Profile on User Update (CRITICAL FIX)
@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    if not created: 
        if hasattr(instance, 'profile'):
            
            # --- CRITICAL FIX: Filter Arguments ---
            
            # 1. Start with a copy of all arguments.
            save_kwargs = kwargs.copy()
            
            # 2. Define a list of ALL arguments that belong ONLY to the User model 
            # or are internal signal metadata, and should NOT be passed to Profile.
            # last_login is the one causing the ValueError.
            # signal is the one that caused the previous TypeError.
            # raw is for internal management commands.
            # update_fields often contains the field names passed during a User update.
            KEYS_TO_REMOVE = ['last_login', 'date_joined', 'signal', 'raw', 'update_fields']

            # 3. Remove these unwanted keys from the arguments
            for key in KEYS_TO_REMOVE:
                if key in save_kwargs:
                    del save_kwargs[key]
            
            # 4. Pass ONLY the cleaned arguments to the profile's save method.
            instance.profile.save(**save_kwargs)