from rest_framework import serializers
from .models import Professor, Module, ModuleInstance, Rating, CachedRating

class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = ['professor_id', 'professor_name']
        
class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['module_code', 'module_name']
        
class ModuleInstanceSerializer(serializers.ModelSerializer):
    # module = ModuleSerializer()
    professors = serializers.SerializerMethodField()
    module_name = serializers.CharField(source='module.module_name')
    module_code = serializers.CharField(source='module.module_code')
    
    class Meta:
        model = ModuleInstance
        fields = ['module_code', 'semester', 'year', 'module_name', 'professors']
        
    def get_professors(self, obj):
        return [{"professor_id":professor.professor_id, "professor_name":professor.professor_name} for professor in obj.professors.all()]   
        
class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['rating_id', 'rating', 'module_instance', 'user', 'professor']
        
class CachedRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CachedRating
        fields = ['average_rating', 'professor']                    