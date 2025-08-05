from .models import TodoList
from typing import Any

from rest_framework import serializers


class AddTodoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoList
        fields = ['id', 'title', 'text']
        extra_kwargs = {
            'title': {'required': True, 'max_length': 30},
            'text': {'required': False, 'max_length': 200},
        }

class UpdateTodoListSerializer(serializers.ModelSerializer):
    confirm_title = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=30
    )
    confirm_text = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=200
    )

    class Meta:
        model = TodoList
        fields = {'title', 'text'}
