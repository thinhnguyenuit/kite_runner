from django.contrib import admin

from kite_runner.models import Profile, User

admin.site.register(User)
admin.site.register(Profile)
