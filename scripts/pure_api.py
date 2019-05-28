import requests  #It is 3rd party library which allowss http requests
import json

BASE_URL = "http://127.0.0.1:8000/"

ENDPOINT = "api/updates/"   #api/updates will currently give us that list view of objects


def get_list(pk = None): # --> lists all this out # default id = 7
    if pk is not None:
        data = json.dumps({"pk":pk})
    else:
        data = json.dumps({})
    
    r = requests.get(BASE_URL + ENDPOINT , data = data)
    # print(r.status_code)
    if r.status_code != 200:
        print('Probably not a good sign')
    data = r.json()
    # print(type(json.dumps(data)))
    # for ob in data:
    #     if ob['pk'] == 1:  # --> for user interaction
    #         r2 = requests.get(BASE_URL + ENDPOINT + str(ob['pk']))
    #         print(r2.json()['content'])
    return data


def create_update():
    new_data = {
        "user" : 1,
        "content" : "update after set endpoint"
    }
    # new_data = json.dumps(new_data)

    # following r is for list view in api.views.py so have not concated any pk with BASE_URL & ENDPOINT
    # r = requests.post(BASE_URL + END POINT, data = new_data)  # will get 400

    # r = requests.delete(BASE_URL + ENDPOINT , data = json.dumps(new_data))  # will get 403

    #following r is for detailview with particular pk(default we have pk=1)
    r = requests.post(BASE_URL + ENDPOINT, data = json.dumps(new_data))

    # r = requests.post(BASE_URL + ENDPOINT, data = new_data) -->for verifying that data convert to json message

    print(r.headers)
    print(r.status_code)

    # if(r.status_code in range(200 ,299)):
    #     print(r.json())

    if(r.status_code == requests.codes.ok):
        # print(r.json())
        return r.json()
    return r.text

print(get_list())

# print(create_update())


def do_obj_update(): # update with put method the content of particular pk
    # 1st way :
    new_data ={
        "pk" : 11 ,
         "content" :  "awesome 2!!!!!"
    }
    r = requests.put(BASE_URL + ENDPOINT, data = json.dumps(new_data)) # we have removed that "pk/" coz we r now testing list view's put method

    # r = requests.put(BASE_URL + ENDPOINT + "1/" , data = new_data)
    # message Not applying json.dumps to get that tells us to convert the data into json

    # 2nd way :
    # new_data = {
    #     "pk" : 1 ,
    #     "content" : "new updated pk = 1"
    # }
    # r = requests.put(BASE_URL + ENDPOINT, data = new_data)
    # # Here in above line we dont have "1/" coz
    # we have alreday specified pk : 1 in new_data object!

    # print(r.headers)
    print(r.status_code)
    if r.status_code == requests.codes.ok:
        return r.json()
    return r.text

# print(do_obj_update())


def do_obj_delete():
    new_data = {
        "pk" : 11 ,
        "content" : "new cool new update"}

    r = requests.delete(BASE_URL + ENDPOINT , data = json.dumps(new_data)) # we dont have "id/" coz testing delete of list view!

    print(r.status_code)
    if r.status_code == requests.codes.ok:
        return r.json()
    return r.text

# print(do_obj_delete())
