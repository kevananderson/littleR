from django.db import models

from context import littleR
from littleR.standard import Standard


class Standard_Model(models.Model):
    """Model for accessing the standard.

    Do you appreciate the physics joke?
    """

    # static data
    _standard = None

    @staticmethod
    def model():
        if Standard_Model._standard is None:
            Standard_Model._standard = Standard("Root").read()
        return Standard_Model._standard
