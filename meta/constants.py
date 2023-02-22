from django.db import models
from django.utils.translation import gettext_lazy as _


class Genders(models.IntegerChoices):
    MALE = 0, _("Male")
    FEMALE = 1, _("Female")
    TRANS = 2, _("Trans")


class Priorities(models.IntegerChoices):
    HI = 3
    MD = 2
    LO = 1


class States(models.IntegerChoices):
    ANDHRA_PRADESH = 1, _("Andhra Pradesh")
    ARUNACHAL_PRADESH = 2, _("Arunachal Pradesh")
    ASSAM = 3, _("Assam")
    BIHAR = 4, _("Bihar")
    CHHATTISGARH = 5, _("Chhattisgarh")
    GOA = 6, _("Goa")
    GUJARAT = 7, _("Gujarat")
    HARYANA = 8, _("Haryana")
    HIMACHAL_PRADESH = 9, _("Himachal Pradesh")
    JHARKHAND = 10, _("Jharkhand")
    KARNATAKA = 11, _("Karnataka")
    KERALA = 12, _("Kerala")
    MADHYA_PRADESH = 13, _("Madhya Pradesh")
    MAHARASHTRA = 14, _("Maharashtra")
    MANIPUR = 15, _("Manipur")
    MEGHALAYA = 16, _("Meghalaya")
    MIZORAM = 17, _("Mizoram")
    NAGALAND = 18, _("Nagaland")
    ODISHA = 19, _("Odisha")
    PUNJAB = 20, _("Punjab")
    RAJASTHAN = 21, _("Rajasthan")
    SIKKIM = 22, _("Sikkim")
    TAMIL_NADU = 23, _("Tamil Nadu")
    TELANGANA = 24, _("Telangana")
    TRIPURA = 25, _("Tripura")
    UTTAR_PRADESH = 26, _("Uttar Pradesh")
    UTTARAKHAND = 27, _("Uttarakhand")
    WEST_BENGAL = 28, _("West Bengal")
    ANDAMAN_AND_NICOBAR_ISLANDS = 29, _("Andaman and Nicobar Islands")
    CHANDIGARH = 30, _("Chandigarh")
    DADRA_AND_NAGAR_HAVELI_AND_DAMAN_AND_DIU = 31, _(
        "Dadra and Nagar Haveli and Daman and Diu"
    )
    DELHI = 32, _("Delhi")
    JAMMU_AND_KASHMIR = 33, _("Jammu and Kashmir")
    LADAKH = 34, _("Ladakh")
    LAKSHADWEEP = 35, _("Lakshadweep")
    PUDUCHERRY = 36, _("Puducherry")

