from django.contrib import admin

# Register your models here.

#from admin.models import Group
#admin.site.register(Group)



from useless_mutant.models import Post, Hashtag

class PostAdmin(admin.ModelAdmin):
	model = Post
	list_display = ['created_at', 'hashtag', 'short_search_query', 'link', 'image']
	list_editable = ['image']
	search_fields = ['hashtag__name']
	#list_display_links = None

class HashtagAdmin(admin.ModelAdmin):
	model = Hashtag
	list_display = ['name', 'created_at', 'last_post_added_time', 'enabled']
	list_editable = ['enabled']
	search_fields = ['name', 'created_at', 'last_post_added_time', 'enabled']
	#list_display_links = None

admin.site.register(Post, PostAdmin)
admin.site.register(Hashtag, HashtagAdmin)


