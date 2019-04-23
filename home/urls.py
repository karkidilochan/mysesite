from django.urls import path
from django.contrib import admin


app_name = 'home'

urlpatterns = [
    path('', admin.site.urls),
    path('admin/', admin.site.urls),

]

admin.site.site_header = "DSA-Form Generator"
admin.site.site_title = "DSA-Form Generator"
admin.site.index_title = "Welcome to Daily Subject Assignment Form Generator"
