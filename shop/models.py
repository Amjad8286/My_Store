from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class ProductSelling(models.Model):
    prod_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    price = models.CharField(max_length=50)
    dec = models.CharField(max_length=1000)
    image = models.ImageField(upload_to="images/")
    liked = models.ManyToManyField(User, default=None, blank=True)

    def __str__(self):
        return self.name

    @property
    def num_likes(self):
        return self.liked.all().count()


LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)

class like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(ProductSelling, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, default='Like',  max_length=20)

    def __str__(self):
        return str(self.post)


class SearchSugesstion(models.Model):
    prod_name = models.ForeignKey(ProductSelling, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.prod_name)


class ReviewsRating(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)

    star = models.IntegerField()    
    product = models.ForeignKey(ProductSelling, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True) 
    review = models.CharField(max_length=1000)  
    datetime = models.DateTimeField(default=now)

    def __str__(self):
        return str(self.name)

    # def avg_rate(self):
    #     rating = ReviewsRating.objects.filter(name=self).aggregate(Avg("star"))
    #     return rating