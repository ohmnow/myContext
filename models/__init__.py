from tortoise import fields
from tortoise.models import Model

class Persona(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)
    preferences = fields.JSONField()

    def __str__(self):
        return self.name
