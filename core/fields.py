from django.db import models


class UpperField(models.CharField):
    def get_prep_value(self, value):
        return str(value).upper()


def get_upperfield():
    return UpperField
