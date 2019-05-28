from django.shortcuts import render
from django.http import JsonResponse,HttpResponse

from updates.models import Update
from django.views.generic import View

from restapi.mixins import JsonResponseMixin

from django.core.serializers import serialize
import json
# Create your views here.


# def detail_view(request):
#     return render()  # return JSON data


def json_example_view(request):
    '''
    URI -- for a REST API
    GET -- Retrive
    '''

    data = {
        "count" : 10 ,
        "name" : "john"
    }
    return JsonResponse(data)


    # In earlier django versions when there was no JsonResponse ,
    # We have to do following which is now replaced by above code in latest django versions
    #
    # import json
    #
    # def update_model_detail_view(request):
    #     data = {
    #         "count" : 10 ,
    #         "name" : "john"
    #     }
    #     json_data = json.dumps(data)
    #     return HttpResponse(json_data, content_type='application/json')



class JsonCBV(View):
    def get(self , request , *args , **kwargs):
        data = {
            "count" : 10 ,
            "name" : "john"
        }
        return JsonResponse(data)


class JsonCBV2(JsonResponseMixin , View):
    def get(self , request , *args , **kwargs):
        data = {
            "count" : 10 ,
            "name" : "john"
        }
        return self.render_to_json_response(data)

# these list and detail are created before UpdateManager class
# and that serialize() method in models.py so it doesn't use .serialize() which we'd created in Update class

# tag : '' --> for use in urls.py coz we've created both views again
class SerializedDetailView(JsonResponseMixin , View):
    def get(self , request , *args , **kwargs):
        obj = Update.objects.get(pk=1)
        data = serialize("json" , [obj] , fields=('user' , 'content'))

        return HttpResponse(data, content_type='application/json')


class SerializedListView(JsonResponseMixin , View):
    def get(self , request , *args , **kwargs):
        qs = Update.objects.all()
        data = serialize("json" , qs , fields=('user' , 'content'))
        # print(data)
        return HttpResponse(data, content_type='application/json')




# These list and detail views are created after that UpdateManager class
# and serialize() method created in models.py so now we can use
#  .serialize() that we've created in Update class


# tag : 'manager' -->for urls.py coz we already have both these views with some difference but working is same!
class SerializedManagerDetailView(JsonResponseMixin , View):
    def get(self , request , *args , **kwargs):
        obj = Update.objects.get(pk=1)


        # data = serialize("json" , [obj] , fields=('user' , 'content'))
        # Above line is from above detail view but now instead of this we can use following

        data  = obj.serialize()
        return HttpResponse(data, content_type='application/json')


class SerializedManagerListView(JsonResponseMixin , View):
    def get(self , request , *args , **kwargs):

        # qs = Update.objects.all()
        # data = serialize("json" , qs , fields=('user' , 'content'))

        # Insted of above 2 commented line we can now use following

        data = Update.objects.all().serialize()
        return HttpResponse(data, content_type='application/json')
