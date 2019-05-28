import json

from django.core.serializers import serialize
from django.db import models
from django.conf import settings
# Create your models here.

def upload_update_image(instance , filename):
    return "updates/{user}/{filename}".format(user = instance.user,filename=filename)

class UpdateQuerySet(models.QuerySet):
    # def serialize(self):  # for list view
    #     return serialize("json", self , fields=('user','content','image'))

    # def serialize(self):  # for list view
    #     qs = self
    #     final_array = []
    #     for obj in qs:
    #         final_array.append(json.loads(obj.serialize()))
    #     return json.dumps(final_array)

    # def serialize(self):  # for list view
    #     qs = self
    #     final_array = []
    #     for obj in qs:
    #         final_array.append(json.loads(obj.serialize()))
    #     return json.dumps(final_array)


    # another way to serialize data with .values method
    def serialize(self):  # This is more efficient method
        list_values = list(self.values("user","content","image","pk"))
        return json.dumps(list_values)

class UpdateManager(models.Manager):
    def get_queryset(self):
        return UpdateQuerySet(self.model , using=self._db)



class Update(models.Model):
    user  =  models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE)
    content  = models.TextField(blank=True,null=True)
    image  = models.ImageField(upload_to=upload_update_image,blank=True,null=True)
    updated = models.DateTimeField(auto_now = True)
    timestamp = models.DateTimeField(auto_now_add = True)

    objects = UpdateManager()

    def __str__(self):
        return self.content or ''

    # def serialize(self): # for particular instance and we r including image field also
    #     return serialize("json" , [self] , fields=('user','content','image')) # for detail view


    # for getting more useful data
    # def serialize(self):
    #     json_data = serialize("json",[self],fields=('user','content','image'))
    #     stuct = json.loads(json_data)
    #     data = json.dumps(stuct[0]['fields']) # for detail view coz we have only one object so we have given index 0
    #     return data


    # The more effiecient serialize method for detailview is following

    def serialize(self):
        try:
            image = self.image.url
        except:
            image = ""
        data = {
            "pk" : self.pk,
            "content" : self.content,
            "user" : self.user.pk ,
            "image" : image
        }
        return json.dumps(data)
