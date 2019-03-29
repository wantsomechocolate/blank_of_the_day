from django.contrib import admin

# Register your models here.

#from admin.models import Group
#admin.site.register(Group)



from useless_mutant.models import Post, Hashtag

admin.site.register(Post)
admin.site.register(Hashtag)