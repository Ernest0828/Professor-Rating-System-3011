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

def precise_round(value):
    if value is None:
        return 0
    decimal = value - int(value)
    if decimal <= 0.5:
        return math.ceil(value)
    else:
        return math.floor(value)

# Create your views here.

#PART 1: register 
@api_view(['POST'])
def register_view (request):   
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

#PART 2:login 
@api_view(['POST'])
def login_view (request):
    try:
        username = request.POST['username']
        password = request.POST['password']
    except:
        return HttpResponse("Invalid data", status=400)
    
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponse("Login successful", status = 200)
    else:
        return HttpResponse("Invalid login", status = 400)
    
#PART 3: logout 
#@api_view(['POST'])
@csrf_exempt
def logout_view (request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponse("Logged out", status = 200)
    else:
        return HttpResponse("Not logged in", status = 400)

#PART 4: list 
@api_view(['GET'])
def list_view (request):
    module_instance = ModuleInstance.objects.all()
    serializer = ModuleInstanceSerializer(module_instance, many=True)    
    return Response(serializer.data)

#PART 5: view 
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
    
    if not professor:
        return Response({"error": "Invalid professor ID"}, status=400)
    if not module:
        return Response({"error": "Invalid module code"}, status=400)
    
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
        
        professor = Professor.objects.filter(professor_id=professor_id).first()
        module = Module.objects.filter(module_code=module_code).first()
        module_instance = ModuleInstance.objects.filter(module=module, year=year, semester=semester).first()
        
        if not professor:
            return JsonResponse({"error": "Invalid professor ID"}, status=400)
        elif not module:
            return JsonResponse({"error": "Invalid module code"}, status=400)
        elif not module_instance:
            return JsonResponse({"error": "Invalid module instance"}, status=400)
        
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
    
