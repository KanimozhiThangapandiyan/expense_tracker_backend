from django.db import models
import uuid
from datetime import datetime
from django.core.exceptions import ValidationError

MAX_LENGTH = 60
MAX_LENGTH_PHONE = 15
DEFAULT_NULLABLE = {'blank': True, 'null': True}

class Base(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)  
    created = models.DateTimeField(default=datetime.now, editable=False)
    updated = models.DateTimeField(auto_now=True,editable=False)
    is_deleted = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()

    def hard_delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
    class Meta:
        abstract=True

class SingleChoiceField(models.CharField):
    """
    A custom field for selecting one choice from a predefined set of options.
    Inherits from CharField and enforces that only one choice can be selected.
    """
    def __init__(self, choices_config: dict, *args, **kwargs):
        # Store the choices configuration
        self.choices_config = choices_config
        self.options = self.choices_config.get("options", [])

        # Ensure choices are provided
        if not self.options:
            raise ValueError("The 'choices' configuration must contain at least one option.")

        # Define choices for the CharField
        generated_choices = [(option, option) for option in self.options]

        # Set the maximum length to the length of the longest option
        max_length = max(len(option) for option in self.options)

        kwargs.update({
            'choices': generated_choices,
            'max_length': max_length,
        })

        # Initialize the parent CharField with updated kwargs
        super().__init__(*args, **kwargs)

    def validate(self, value, model_instance):
        """Ensure the value is one of the allowed choices."""
        if value not in dict(self.choices).keys():
            raise ValidationError(f"'{value}' is not a valid choice for this field.")

        super().validate(value, model_instance)

    def deconstruct(self):
        """Ensure proper handling of custom params during migrations."""
        name, path, args, kwargs = super().deconstruct()
        kwargs['choices_config'] = self.choices_config
        return name, path, args, kwargs
