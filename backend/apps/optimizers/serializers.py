from rest_framework import serializers
from .models import PowerRanking, ScheduleAnalysis

class PowerRankingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PowerRanking
        fields = '__all__'

class ScheduleAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleAnalysis
        fields = '__all__'
