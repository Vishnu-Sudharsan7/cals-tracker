from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from test1.utils import get_db_handle, get_collection_handle

DATABASE_NAME = 'Credentials'
DATABASE_HOST = 'localhost'
DATABASE_PORT = '27017'
db_handle, mongo_client = get_db_handle(DATABASE_NAME, DATABASE_HOST, DATABASE_PORT)
collection = db_handle['user_auth_table']
collection2= db_handle['user_details_table']
name_param=''
program=''
# Create your views here.
def home(request):
    return render(request, 'signin.html')


def signup(request):
    return render(request, 'signup.html')


def home1(request):
    return render(request,'home.html')

def cals_track(request):
    return render(request,'cals.html')


def create(request):
    name = request.GET['username']
    email = request.GET['email']
    password = request.GET['password']
    s=set()
    cursor = collection.find({},{"email": 1})
    for i in cursor:
        s.add(i['email'])
    if email in s:
        return render(request,'signup.html',{'message': 'Email Id already exist'})
    else:
        dic = {'name':name,
               'email':email,
               'password':password}
        collection.insert_one(dic)
        return render(request,'signin.html',{'message': 'Successfully Registered '+str(name)})


def logincheck(request):
    email = request.POST['email']
    password = request.POST['password']
    dic = {}
    cursor = collection.find({},{"email": 1,"password":1})
    for i in cursor:
        dic[i['email']] = i['password']
    if email in dic.keys() and password in dic.values():
        global name_param
        name_param=email
        return render(request,'home.html',{'message':name_param})
    elif email in dic.keys() and password not in dic.values():
        return render(request,'signin.html',{'message': 'Incorrect Password'})
    else:
        return render(request,'signin.html',{'message': 'Incorrect Email and Password'})


def add_details(request):
    height= request.GET['height']
    weight = request.GET['weight']
    goal=request.GET['Goal']
    s = set()
    cursor = collection2.find({}, {"mail": 1})

    duration=request.GET['duration']
    weekly_gain=0

    global program

    if(int(goal)>int(weight)):
        program="Weight gain"
        weekly_gain = (int(goal) - int(weight)) / (int(duration) * 4)
    else:
        program="Weight loss"
        weekly_gain=(int(weight)-int(goal))/(int(duration)*4)

    dic = {'mail': name_param,
               'duration': duration,
               'height': height,
               'weight': weight,
               'Goal': goal,
                'Weekly_gain':weekly_gain,
           'Program_type':program}
    for i in cursor:
        s.add(i['mail'])
    if name_param in s:
        return render(request,'home.html',{'message': 'Details already registered'})
    else:
        x=collection2.insert_one(dic)
    if x:
        return render(request, "home.html", {'message':program,'weekly_gain':weekly_gain})
    else:
        print("error")

