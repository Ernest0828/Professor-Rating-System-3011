from rest_framework import serializers
from .models import Professor, Module, ModuleInstance, Rating, CachedRating

class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = ['professor_id', 'professor_name', 'average_rating']
        
class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['module_code', 'module_name']
        
class ModuleInstanceSerializer(serializers.ModelSerializer):
    module = ModuleSerializer()
    #professors = ProfessorSerializer(many=True)
    
    class Meta:
        model = ModuleInstance
        fields = ['module_instance_id', 'semester', 'year', 'professors', 'module']
        
class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['rating_id', 'rating', 'module_instance', 'user', 'professor']
        
class CachedRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CachedRating
        fields = ['average_rating', 'professor']                    