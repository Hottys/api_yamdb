from django.contrib import admin
from reviews.models import Category, Comment, Review, Title


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)


class TitleAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "year", "description")
    search_fields = ("name", "year")
    list_filter = ("category",)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("title", "text", "score")
    search_fields = ("title",)
    list_filter = ("score",)


class CommentAdmin(admin.ModelAdmin):
    list_display = ("review", "text")
    search_fields = ("review",)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
