from updates.models import Update as UpdateModel
from django.views.generic import View
from django.http import HttpResponse

# data will be serialized here so no need to import JsonResponse
from updates.api.mixins import CSRFExemptMixin
import json

from restapi.mixins import HttpResponseMixin
from updates.forms import UpdateModelForm

from updates.api.utils import is_json
# For CRUD

class UpdateModelDetailAPIView(CSRFExemptMixin ,HttpResponseMixin, View):
    '''
    Retrive , Update , Delete
    '''
    is_json = True

    def get_object(self , pk=None): # for getting individual object with particular pk
        # # 1st way:
        # try:
        #     obj = UpdateModel.objects.get(pk=pk)
        # except UpdateModel.DoesNotExist:
        #     obj = None
        # return obj

        # 2nd way : This is more better and it also handles does not exits!

        qs = UpdateModel.objects.filter(pk=pk)
        if qs.count() == 1:
            return qs.first()
        return None

    def get(self , request , pk, *args , **kwargs): # for Retrive
        obj = self.get_object(pk=pk) # using get_object that we defined above

        if obj is None: # condition for , if obj is none
            error_data = json.dumps({"message" : "Update not found!"})
            return self.render_to_response(error_data , status = 404)
        json_data = obj.serialize()

        # return HttpResponse(json_data , content_type="application/json")
        return self.render_to_response(json_data)

    def post(self , request , *args , **kwargs): # for Create
        json_data = json.dumps({"message" : "Not allowed, please use api/updates/ endpoint!"})
        # return HttpResponse({} , content_type="application/json")
        return self.render_to_response(json_data , status = 403)

    def put(self , request , pk , *args , **kwargs): # for Update
        # we put that valid_json part first bcoz we wanted that coming data should be json!
        valid_json = is_json(request.body)
        if not valid_json:
            error_data = json.dumps({"message" : "Invalid data sent , please send using JSON."})
            return self.render_to_response(error_data , status = 400)


        obj = self.get_object(pk=pk) # using get_object that we defined above

        if obj is None: # condition for , if obj is none
            error_data = json.dumps({"message" : "Update not found!"})
            return self.render_to_response(error_data , status = 404)


        # we can also do that or also we can use all method for following data dictionary
        # data = {
        #     "user" : obj.user,
        #     "content" : obj.content
        # }
        data = json.loads(obj.serialize())
        passed_data = json.loads(request.body)  # passed_data coz this data is coming in!
        # coz it contains json data and for using it we r converting it to pytho data

        for key,value in passed_data.items(): # for changing default data to the data which coming in!
            data[key] = value

        print(passed_data) # just for checking

        form = UpdateModelForm(data ,instance = obj)
        if form.is_valid():
            obj = form.save(commit = True)
            obj_data = json.dumps(data) # obj_data = obj.serialize() bcoz data is already serialized
            return self.render_to_response(obj_data,status=201)

        if form.errors:
            data = json.dumps(form.errors)
            # return HttpResponse(data , content_type="application/json" , status = 400)
            return self.render_to_response(data , status = 400)

        # print(dir(request)) # just for information from which we knew that
        # we should use requese.body instead of request.POST

        # print(request.body) # instead of request.POST

        # new_data = json.loads(request.body) # we dont need this coz we r validatiog with form
        # print(new_data['content'])

        json_data = json.dumps({"message" : "Success Json data!"})
        # return HttpResponse(json_data , content_type="application/json")
        return self.render_to_response(json_data)


    def delete(self , request , pk , *args , **kwargs): # for Delete
        obj = self.get_object(pk=pk) # using get_object that we defined above

        if obj is None: # condition for , if obj is none
            error_data = json.dumps({"message" : "Update not found!"})
            return self.render_to_response(error_data , status = 404)

        deleted_ , item_deleted = obj.delete()
        print(item_deleted)

        if deleted_ == 1:
            num = str(pk)
            json_data = json.dumps({"message" : "Successfully deleted! pk = {}".format(num)})
            # return HttpResponse(json_data , content_type="application/json")
            return self.render_to_response(json_data , status = 200)

        error_data = json.dumps({"message" : "Could not delete item. Please try again later.!"})
        return self.render_to_response(error_data , status=400)

class UpdateModelListAPIView(CSRFExemptMixin ,HttpResponseMixin, View):
    '''
    List view --> Retrieve -- Detail View
    create view
    '''
    is_json = True
    queryset = None

    # This method is for easier work and user readability
    # def render_to_response(data , status=200): # default status is 200
    #     return HttpResponse(data , content_type='application/json' status = status)


    # above method is commented bcoz we created HttpResponseMixin which contains this method
    # to avoid repeatation


    def get_queryset(self , pk=None):
        qs = UpdateModel.objects.all()
        self.queryset = qs
        return qs

    def get_object(self , pk=None): # for getting individual object with particular pk
        if pk is None: # This is bcoz we r also passing None in pk
            return pk

        qs = self.get_queryset().filter(pk=pk)     # qs = UpdateModel.objects.filter(pk=pk)
        if qs.count() == 1:
            return qs.first()
        return None

    def get(self , request , *args , **kwargs):
        data = json.loads(request.body)
        passed_pk = data.get('pk' , None)
        if passed_pk is not None:
            obj = self.get_object(pk = passed_pk)
            if obj is None:
                error_data = json.dumps({"message" : "Object not found!"})
                return self.render_to_response(error_data , status = 404)
            json_data = obj.serialize()
            return self.render_to_response(json_data)
        else:
            qs = self.get_queryset()  # qs = self.UpdateModel.objects.all()
            # bcoz now we have get_queryset method

            json_data = qs.serialize()
            # return HttpResponse(json_data , content_type="application/json")

            return self.render_to_response(json_data) # we havent passed any status bcoz
            # default status for get method is 200 which we already given in that function
            # returning json

    def post(self , request , *args , **kwargs):
        # print(request.POST)
        valid_json = is_json(request.body)
        if not valid_json:
            error_data = json.dumps({"message" : "Invalid data sent , please send using JSON."})
            return self.render_to_response(error_data , status = 400)
        data = json.loads(request.body)

        # we want to use the POST data so we are using the forms
        # form = UpdateModelForm(request.POST)

        form = UpdateModelForm(data)
        if form.is_valid():
            obj = form.save(commit = True)
            obj_data = obj.serialize()
            return self.render_to_response(obj_data,status=201)

        if form.errors:
            data = json.dumps(form.errors)
            # return HttpResponse(data , content_type="application/json" , status = 400)
            return self.render_to_response(data , status = 400)

        data = {"message" : "Not Allowed"}
        return self.render_to_response(data , status = 400)

    # def delete(self , request , *args , **kwargs): # just for show msg to the user
    #     data = json.dumps({"message" : "You can't delete entire list!"})
    #     # status_code = 403
    #     # return HttpResponse(data , content_type="application/json" , status = status_code)
    #
    #     return self.render_to_response(data , status = 403)


    def put(self , request ,*args , **kwargs): # for Update
        # we put that valid_json part first bcoz we wanted that coming data should be json!
        valid_json = is_json(request.body)
        if not valid_json:
            error_data = json.dumps({"message" : "Invalid data sent , please send using JSON."})
            return self.render_to_response(error_data , status = 400)

        passed_data = json.loads(request.body)  # passed_data coz this data is coming in!
        passed_pk = passed_data.get('pk' , None)
        # so we r getting our pk as above from request.body so we have
        # removed 'pk' as argument from this put() method

        if not passed_pk:
            error_data = json.dumps({"pk" : "Requried field to update item!"})
            return self.render_to_response(error_data , status = 400)


        obj = self.get_object(pk=passed_pk)
        if obj is None: # condition for , if obj is none
            error_data = json.dumps({"message" : "Object not found!"})
            return self.render_to_response(error_data , status = 404)


        data = json.loads(obj.serialize())
        # coz it contains json data and for using it we r converting it to pytho data

        for key,value in passed_data.items(): # for changing default data to the data which coming in!
            data[key] = value


        form = UpdateModelForm(data ,instance = obj)
        if form.is_valid():
            obj = form.save(commit = True)
            obj_data = json.dumps(data) # obj_data = obj.serialize() bcoz data is already serialized
            return self.render_to_response(obj_data,status=201)

        if form.errors:
            data = json.dumps(form.errors)
            return self.render_to_response(data , status = 400)

        json_data = json.dumps({"message" : "Success Json data!"})
        return self.render_to_response(json_data)


    def delete(self , request ,*args , **kwargs): # for Delete
        valid_json = is_json(request.body)
        if not valid_json:
            error_data = json.dumps({"message" : "Invalid data sent , please send using JSON."})
            return self.render_to_response(error_data , status = 400)

        passed_data = json.loads(request.body)  # passed_data coz this data is coming in!
        passed_pk = passed_data.get('pk' , None)
        # so we r getting our pk as above from request.body so we have
        # removed 'pk' as argument from this put() method

        if not passed_pk:
            error_data = json.dumps({"pk" : "Requried field to delete item!"})
            return self.render_to_response(error_data , status = 400)


        obj = self.get_object(pk=passed_pk)
        if obj is None: # condition for , if obj is none
            error_data = json.dumps({"message" : "Object not found!"})
            return self.render_to_response(error_data , status = 404)


        deleted_ , item_deleted = obj.delete()
        print(item_deleted)

        if deleted_ == 1:
            num = str(passed_pk)
            json_data = json.dumps({"message" : "Successfully deleted! pk = {}".format(num)})
            # return HttpResponse(json_data , content_type="application/json")
            return self.render_to_response(json_data , status = 200)

        error_data = json.dumps({"message" : "Could not delete item. Please try again later.!"})
        return self.render_to_response(error_data , status=400)
