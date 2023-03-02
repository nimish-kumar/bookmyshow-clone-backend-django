from django.contrib import admin
from .models import Artist, City, Facility, Genre, Language, Tag

# Register your models here.

admin.site.register(Artist)
admin.site.register(City)
admin.site.register(Facility)
admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Tag)
