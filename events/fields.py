from django.db import models

class FlexibleImageField(models.CharField):
    """
    Campo che può contenere sia un URL che un percorso file
    """
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 500)
        super().__init__(*args, **kwargs)