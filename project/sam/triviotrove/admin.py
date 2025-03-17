from django.contrib import admin
from triviotrove.models import Word

admin.site.register(Word)



admin.site.site_header = "TrivioTrove Admin"
admin.site.site_title = "TrivioTrove"
admin.site.index_title = "Welcome to TrivioTrove Admin Panel"

