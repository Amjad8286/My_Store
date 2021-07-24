from django.contrib import admin
from .models import ProductSelling, like, SearchSugesstion, ReviewsRating
# Register your models here.
admin.site.register(ProductSelling)
admin.site.register(like)
admin.site.register(SearchSugesstion)
admin.site.register(ReviewsRating)
