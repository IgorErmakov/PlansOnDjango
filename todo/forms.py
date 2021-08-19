from django.forms import ModelForm
from .models import TodoItem

class TodoForm(ModelForm):

    class Meta:
        model = TodoItem
        fields = [
            'name',
            'memo',
            'is_important',
        ]
