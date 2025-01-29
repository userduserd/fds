from django.contrib import admin
from .models import Req, TelegramUser, Course
# Register your models here.


@admin.register(Req)
class ReqAdmin(admin.ModelAdmin):
    list_display = ['id']


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ['id']


@admin.register(Course)
class CourseUserAdmin(admin.ModelAdmin):
    list_display = ['id']