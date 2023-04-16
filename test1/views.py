from datetime import datetime

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
collection2 = db_handle['user_details_table']
collection3 = db_handle['food_details']
collection4 = db_handle['progress_table']
collection5 = db_handle['total_calorie_log']
name_param = ''
program = ''
calories = 0


# Create your views here.
def home(request):
    return render(request, 'signin.html')


def signup(request):
    return render(request, 'signup.html')


def home1(request):
    return render(request, 'home.html', {'message': name_param})


def cals_track(request):
    return render(request, 'cals.html')


def create(request):
    name = request.GET['username']
    email = request.GET['email']
    password = request.GET['password']
    s = set()
    cursor = collection.find({}, {"email": 1})
    for i in cursor:
        s.add(i['email'])
    if email in s:
        return render(request, 'signup.html', {'message': 'Email Id already exist'})
    else:
        dic = {'name': name,
               'email': email,
               'password': password}
        collection.insert_one(dic)
        return render(request, 'signin.html', {'message': 'Successfully Registered ' + str(name)})


def logincheck(request):
    email = request.POST['email']
    password = request.POST['password']
    dic = {}
    cursor = collection.find({}, {"email": 1, "password": 1})
    for i in cursor:
        dic[i['email']] = i['password']
    if email in dic.keys() and password in dic.values():
        global name_param
        name_param = email
        return render(request, 'home.html', {'message': name_param})
    elif email in dic.keys() and password not in dic.values():
        return render(request, 'signin.html', {'message': 'Incorrect Password'})
    else:
        return render(request, 'signin.html', {'message': 'Incorrect Email and Password'})


def add_details(request):
    height = request.GET['height']
    weight = request.GET['weight']
    goal = request.GET['Goal']
    s = set()
    cursor = collection2.find({}, {"mail": 1})

    duration = request.GET['duration']
    weekly_gain = 0

    global program

    if (int(goal) > int(weight)):
        program = "Weight gain"
        weekly_gain = (int(goal) - int(weight)) / (int(duration) * 4)
    else:
        program = "Weight loss"
        weekly_gain = (int(weight) - int(goal)) / (int(duration) * 4)

    dic = {'mail': name_param,
           'duration': duration,
           'height': height,
           'weight': weight,
           'Goal': goal,
           'Weekly_gain': weekly_gain,
           'Program_type': program}
    for i in cursor:
        s.add(i['mail'])
    if name_param in s:
        return render(request, 'home.html', {'message': 'Details already registered'})
    else:
        x = collection2.insert_one(dic)
    if x:
        return render(request, "home.html", {'message': program, 'weekly_gain': weekly_gain})
    else:
        print("error")


def track(request):
    item = request.GET['item']
    quantity = request.GET['quantity']
    meal_tym = request.GET['meal_time']
    if (item == ''):
        return render(request, 'cals.html', {'message': "enter the details"})
    global calories, ans
    calories = 0
    date = datetime.utcnow()  # create a datetime object representing the current UTC time

    query = {'food': item}
    query2 = {'email': name_param}
    x = collection3.find(query)
    for result in x:
        calorie = result.get('cals', "")
        ans = int(calorie) * int(quantity)
        calories += ans

    dic = {'email': name_param,
           'meal_time': meal_tym,
           'food': item,
           'quantity': quantity,
           'calorie': ans,
           'date': date
           }
    collection4.insert_one(dic)
    dic2 = {
        'email': name_param,
        'total_calorie': calories,
        'date': date

    }
    y = collection5.find(query2)
    count = collection5.count_documents(query2)

    if count > 0:
        print("trigerred 1")
        for result in y:
            calo = result.get('total_calorie', "")
            calories += int(calo)

        myquery = {"email": name_param}
        newvalue = {"$set": {'total_calorie': calories}}
        collection5.update_one(myquery, newvalue)
    else:
        collection5.insert_one(dic2)

    print(calories)

    return render(request, 'cals.html', {'message': calories})


def log(request):
    query = {'email': name_param}
    projection = {'meal_time': 1, 'food': 1, 'quantity': 1, 'calorie': 1, 'date': 1}
    results = collection4.find(query, projection)

    my_data = [{'food': result['food'], 'quantity': result['quantity'], 'meal_time': result['meal_time'],
                'date': result['date']} for result in results]

    query2 = {'email': name_param}
    projection2 = {'total_calorie': 1, 'email': 1}
    res = collection5.find(query2, projection2)
    for x in res:
        print(x['total_calorie'])
    print("###")
    print(my_data)
    return render(request, 'cals.html', {'log': my_data})


def profile(request):
    query = {'mail': name_param}
    projection = {'height': 1, 'weight': 1, 'Goal': 1, 'Program_type': 1, 'Weekly_gain': 1, 'mail': 1}
    res = collection2.find(query, projection)

    my_data = [{'height': result['height'], 'weight': result['weight'], 'Goal': result['Goal'],
                'Program_type': result['Program_type'], 'Weekly_gain': result['Weekly_gain'], 'mail':result['mail']} for result in res]
    print(my_data)
    return render(request, 'profile.html', {'details': my_data})
