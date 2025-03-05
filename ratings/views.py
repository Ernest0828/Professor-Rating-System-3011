from django.shortcuts import render
from .models import Module
from .models import Professor
from .models import Rating
from .models import ModuleInstance
from .models import CachedRating
from .serializer import ModuleSerializer
from .serializer import ProfessorSerializer
from .serializer import RatingSerializer
from .serializer import ModuleInstanceSerializer
from .serializer import CachedRatingSerializer
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import math
from collections import defaultdict

def precise_round(value):
    if value is None:
        return 0
    decimal = value - int(value)
    if decimal <= 0.5:
        return math.ceil(value)
    else:
        return math.floor(value)

# Create your views here.
@api_view(['GET'])
def view (request):
    modules = Module.objects.all() #get all modules
    serializer = ModuleSerializer(modules, many=True) #serialize the modules
    return Response(serializer.data) #return the serialized data

@api_view(['GET'])
def view_professor (request):
    professor = Professor.objects.all() #get all modules
    serializer = ProfessorSerializer(professor, many=True) #serialize the modules
    return Response(serializer.data) #return the serialized data

@api_view(['GET'])
def view_rating (request):
    rating = Rating.objects.all() #get all modules
    serializer = RatingSerializer(rating, many=True) #serialize the modules
    return Response(serializer.data)

@api_view(['GET'])
def view_module_instance (request):
    module_instance = ModuleInstance.objects.all()
    serializer = ModuleInstanceSerializer(module_instance, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def view_cached_rating (request):
    rating = CachedRating.objects.all() #get all modules
    serializer = CachedRatingSerializer(rating, many=True) #serialize the modules
    return Response(serializer.data)

#PART 1: register /
@api_view(['POST'])
def register_view (request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
        except:
            return Response("Invalid data", status=400)
        
        if User.objects.filter(username=username).exists():
            return Response("Username already exists", status=400)
        if User.objects.filter(email=email).exists():
            return Response("Email already exists", status=400)
        
        user = User.objects.create_user(username, email, password)
        user.save()
        return Response("User created", status=201)

#PART 2:login /
@api_view(['POST'])
def login_view (request):
    try:
        username = request.POST['username']
        password = request.POST['password']
    except:
        return Response("Invalid data", status=400)
    
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response("Login successful", status = 200)
    else:
        return Response("Invalid login", status = 400)
    
#PART 3: logout /
# @api_view(['POST'])
@csrf_exempt
def logout_view (request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponse("Logged out", content_type="text/plain")
    else:
        return HttpResponse("Not logged in", content_type="text/plain")

#PART 4: list 
@api_view(['GET'])
def list_view (request):
    module_instances = ModuleInstance.objects.all()
    """create a dictionary to store the data of same professors teaching same module instance
    grouped_instance = defaultdict(list)
    for instance in module_instances:
        key = (instance.module.module_code, instance.year, instance.semester)
        grouped_instance[key].append(instance)"""
    
    data = []
    
    for module_instance in module_instances:
        module_name = module_instance.module.module_name
        module_code = module_instance.module.module_code
        professors = ','.join([f"{professors.professor_id}, {professors.professor_name}" 
                               for professors in module_instance.professors.all()]) #join all professors from professors table
        
        data.append({
            'module_code': module_code,
            'module_name': module_name,
            'year': module_instance.year,
            'semester': module_instance.semester,
            'professors': professors
        })
        
    return Response({"module_instances": data})

#PART 5: view (draft)
@api_view(['GET'])
def rating_view (request):
    cached_ratings = CachedRating.objects.all()
    data = []

    for cached_rating in cached_ratings:
        data.append({
            "professor_id": cached_rating.professor.professor_id,
            "name": cached_rating.professor.professor_name,
            "average_rating": cached_rating.average_rating
        })

    return Response({"professors": data})

#PART 6: average 
@api_view(['GET'])
def average_view (request):
    professor_id = request.query_params['professor_id']
    module_code = request.query_params['module_code']
    
    professor = Professor.objects.filter(professor_id=professor_id).first() #find corresponding professor
    module = Module.objects.filter(module_code=module_code).first() #find corresponding module
    
    if not professor or not module:
        return Response({"error": "Invalid professor ID or module code"}, status=400)
    
    module_instances = ModuleInstance.objects.filter(module=module) #retrieve all module instances associated with that module
    average_value = Rating.objects.filter(professor=professor, module_instance__in=module_instances).aggregate(Avg('rating'))['rating__avg'] #rating__avg is the key to get the average value
    average_value = precise_round(average_value) if average_value is not None else 0
    stars = '*' * average_value
    
    return Response({
        "professor_id": professor.professor_id,
        "module_code": module.module_code,
        "average_rating": stars
    })
    
#PART 7: rate
#@login_required
@csrf_exempt
def rate_view (request):
    user = request.user
    #ensure that user is logged in before rating
    if not user.is_authenticated:
        return JsonResponse({"error":"Please login"}, status=401)
    
    if request.method == 'POST':
        professor_id = request.POST.get('professor_id')
        module_code = request.POST.get('module_code')
        year = request.POST.get('year')
        semester = request.POST.get('semester')
        rating = request.POST.get('rating')
        
        if not 1 <= int(rating) <= 5:
            return JsonResponse({"error": "Rating must be between 1 to 5"}, status=400)
        
        professor = Professor.objects.filter(professor_id=professor_id).first()
        module = Module.objects.filter(module_code=module_code).first()
        module_instance = ModuleInstance.objects.filter(module=module, year=year, semester=semester).first()
        
        if not professor or not module or not module_instance:
            return JsonResponse({"error": "Invalid professor ID, module code, year or semester"}, status=400)
        
        existed_rating = Rating.objects.filter(
            user=user.username,
            module_instance=module_instance,
            professor=professor            
        ).exists()
        
        if existed_rating:
            return JsonResponse({"error":"You have already rated this professor for this module instance"}, status=400)
        
        #add rating to the Rating table
        Rating.objects.create(
            rating=rating,
            module_instance=module_instance,
            professor=professor,
            user=user.username
        )
    
    return JsonResponse({"message":"Rating added"}, status=201)
    
