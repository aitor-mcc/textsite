from django.db.models.signals import post_save 
from django.dispatch import receiver 
from functions import * 
from .models import CustomUser, key 
  
# create key 
@receiver(post_save, sender=CustomUser)  
def create_profile(sender, instance, created, **kwargs): 
    if created: 
        keys = generate_keys() 
        key_model = key(uuid = instance,  
                public_exponent = keys[0][0],  
                modulo = keys[0][1], 
                private_exponent = keys[1][0]) 
        key_model.save() 
 
#save key 
@receiver(post_save, sender=CustomUser)  
def save_profile(sender, instance, **kwargs): 
        instance.key.save() 
