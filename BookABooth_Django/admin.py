from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import *

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
    filter_horizontal = ('service_package',)

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

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'password1', 'password2'),
        }),
    )

    fieldsets = (
        (None, {'fields': ('username', 'password', 'company')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone')}),
        ('Permissions', {'fields': ('privacy_policy_accepted', 'is_active', 'is_staff', 'is_superuser')}),
    )


class SystemAdmin(admin.ModelAdmin):

    list_display = ('id', 'enabled')
    list_filter = ('id', 'enabled')

    def has_add_permission(self, request):
        """
        Prevents adding two instances of System.
        """
        return not System.objects.exists()

class SystemConfigurationAdmin(admin.ModelAdmin):

    list_display = ('cancellation_reimbursement', 'cancellation_reimbursement_until')

    def has_add_permission(self, request):
        """
        Prevents adding two SystemConfigurations.
        """
        return not SystemConfiguration.objects.exists()


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
_register(SystemConfiguration, SystemConfigurationAdmin)
