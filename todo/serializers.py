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
