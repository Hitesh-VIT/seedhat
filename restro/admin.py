from django.contrib import admin
from .models import *

class KeysAdmin(admin.ModelAdmin):
    pass
admin.site.register(Keys,KeysAdmin)


class ProfileAdmin(admin.ModelAdmin):
    pass
admin.site.register(Profile,ProfileAdmin)


class RestaurantsAdmin(admin.ModelAdmin):
    pass
admin.site.register(Restaurants,RestaurantsAdmin)


class VisitsAdmin(admin.ModelAdmin):
    pass
admin.site.register(Visits,VisitsAdmin)


class DiscountsAdmin(admin.ModelAdmin):
    pass
admin.site.register(Discounts,DiscountsAdmin)

class Special_discountAdmin(admin.ModelAdmin):
    pass
admin.site.register(Special_discount,Special_discountAdmin)

