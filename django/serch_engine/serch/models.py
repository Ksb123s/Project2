from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Engine_name(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Detaile_name(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class search_data(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField(null=True)
    user = models.CharField(max_length=50, unique=True)
    search_user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True, upload_to="image")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="검색일시")

    modified_at = models.DateTimeField(auto_now=True)
    keyword = models.TextField()
    engine_name = models.ForeignKey(Engine_name, on_delete=models.DO_NOTHING)
    detail_name = models.ForeignKey(Detaile_name, on_delete=models.DO_NOTHING)
    price = models.IntegerField(blank=True, null=True)
    url = models.TextField(unique=True)

    class Meta:
        unique_together = ("user", "title")

    def __str__(self) -> str:
        return "%s - %s - %s" % (self.search_user, self.keyword, self.detail_name)


class Search_Keyword_Record_Data(models.Model):
    keyword = models.TextField()
    engine_name = models.ForeignKey(Engine_name, on_delete=models.DO_NOTHING)
    detail_name = models.ForeignKey(Detaile_name, on_delete=models.DO_NOTHING)
    search_user = models.ForeignKey(User, on_delete=models.CASCADE)
    count = models.IntegerField(blank=True, default=1)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="검색일시")
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("keyword", "engine_name", "detail_name", "search_user")

    def __str__(self) -> str:
        return "%s- %s - %s -%s" % (
            self.keyword,
            self.count,
            self.engine_name.name,
            self.detail_name.name,
        )
