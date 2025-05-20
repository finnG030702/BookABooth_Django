from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User, Booking, Booth, System, Company, Location, ServicePackage

# Register your models here.

class BookingAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'received',
        'status',
        'confirmed',
        'price',
        'cancellationfee',
        'company',
        'booth',
    )
    list_filter = (
        'received',
        'company',
        'booth',
        'confirmed',
        'id',
        'status',
        'price',
        'cancellationfee',
    )


class BoothAdmin(admin.ModelAdmin):

    list_display = ('id', 'title', 'ceiling_height', 'available', 'location', 'get_service_package')
    list_filter = ('location', 'id', 'title', 'ceiling_height', 'service_package', 'available')

    def get_service_package(self, obj):
        return ", ".join([sp.name for sp in obj.service_package.all()])
    get_service_package.short_description = 'Service Packages'


class CompanyAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'billing_address',
        'logo',
        'description',
        'waiting_list',
        'exhibitor_list',
    )
    list_filter = (
        'id',
        'name',
        'billing_address',
        'logo',
        'description',
        'waiting_list',
        'exhibitor_list',
    )
    search_fields = ('name',)

class UserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'phone',
        'privacy_policy_accepted',
        'company',
        'is_superuser',
    )
    list_filter = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'phone',
        'privacy_policy_accepted',
        'company',
        'is_superuser',
    )


class SystemAdmin(admin.ModelAdmin):

    list_display = ('id', 'enabled')
    list_filter = ('id', 'enabled')


class LocationAdmin(admin.ModelAdmin):

    list_display = ('id', 'location', 'site_plan')
    list_filter = ('id', 'location', 'site_plan')


class ServicePackageAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'price', 'description')
    list_filter = ('id', 'name', 'price', 'description')
    search_fields = ('name',)


def _register(model, admin_class):
    admin.site.register(model, admin_class)


_register(Booking, BookingAdmin)
_register(Booth, BoothAdmin)
_register(Company, CompanyAdmin)
_register(User, UserAdmin)
_register(System, SystemAdmin)
_register(Location, LocationAdmin)
_register(ServicePackage, ServicePackageAdmin)
