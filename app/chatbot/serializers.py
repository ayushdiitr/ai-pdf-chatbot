# serializers.py

from rest_framework import serializers

class ChatRequestSerializer(serializers.Serializer):
    query = serializers.CharField(max_length=1000, required=True)

class ChatResponseSerializer(serializers.Serializer):
    answer = serializers.CharField(max_length=2000)
    source1 = serializers.CharField(max_length=1000, required=False)
    source2 = serializers.CharField(max_length=1000, required=False)
    source3 = serializers.CharField(max_length=1000, required=False)
