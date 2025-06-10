from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.utils import timezone
from decimal import Decimal

class Booking(models.Model): # TODO: Kommentare für Models überarbeiten
    """
    Booking, which will be created by users.

    received (datetime): When the booking was received.
    status (str): Status of the booking (blocked, prebooked, confirmed, canceled). Prebooked is used as default.
    confirmed (datetime): When the booking was confirmed via e-mail.
    price (decimal): Price of the booking, depends on ServicePackage and Location.
    cancellationfee (decimal): Price for the cancellation, percentage of price.
    company (Company): Which Company sent this booking.
    booth (Booth): Which booth is booked with this booking.
    """

    class Status(models.TextChoices):
        BLOCKED = 'blocked', 'Blocked'
        PREBOOKED = 'prebooked', 'Prebooked'
        CONFIRMED = 'confirmed', 'Confirmed'
        CANCELED = 'canceled', 'Canceled'

    received = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PREBOOKED)
    confirmed = models.DateTimeField(blank=True, null=True)
    price = models.DecimalField(max_digits=21, decimal_places=2, blank=True, null=True)
    cancellationfee = models.DecimalField(max_digits=21, decimal_places=2, blank=True, null=True)
    company = models.ForeignKey('Company', on_delete=models.DO_NOTHING, related_name="companies")
    booth = models.ForeignKey('Booth', on_delete=models.SET_NULL, null=True, blank=True, related_name="booths")

    def cancel(self, canceled_by_admin=False):

        self.status = 'canceled'

        # Configure Reimbursement for cancellation. Including fallback, if SystemConfiguration is empty.
        config = SystemConfiguration.objects.first()
        if config:
            reimbursement_percent = config.cancellation_reimbursement
            reimbursement_until = config.cancellation_reimbursement_until

            if timezone.now().date() <= reimbursement_until:
                percentage = Decimal(100 - reimbursement_percent) / 100
                self.cancellationfee = self.price * percentage
            else:
                self.cancellationfee = self.price
        else:
            self.cancellationfee = self.price

        # TODO: Wird Cancellationfee auch gesetzt, wenn Admin Buchung storniert?
        self.save()

        booth = self.booth
        booth.available = True
        booth.save()

        company = self.company
        company.exhibitor_list = False
        company.save()

        if canceled_by_admin:
            users = self.company.employees.all()
            user = users.first() if users.exists() else None
            send_mail(
                subject="Django BookABooth - Ihre Buchung wurde storniert",
                message=(
                    f"Moin {user.username}, \n\n"
                    f"Ihre Buchung für den Stand {booth.title} wurde von einem Administrator storniert.\n"
                    f"Falls Sie Rückfragen haben, wenden Sie sich gerne an unser Team."
                ),
                from_email="noreply@bookabooth.de",
                recipient_list=[user.email],
                fail_silently=True,
            )


class Booth(models.Model):
    """
    Booth, which can be booked by users.

    title (str): Name of the booth (A1, A2, B1 etc.).
    ceiling_height (decimal): How tall the ceiling is at the booth's location.
    available (boolean): If the booth is already booked (default=True).
    location (Location): The physical location where the booth will be.
    service_package (ServicePackage): Defines if the booth is standard or premium.
    """
    title = models.CharField(unique=True, max_length=200)
    ceiling_height = models.DecimalField(max_digits=21, decimal_places=2, blank=True, null=True)
    available = models.BooleanField(default=True)
    location = models.ForeignKey('Location', on_delete=models.SET_NULL, blank=True, null=True, related_name='booths')
    service_package = models.ManyToManyField('ServicePackage', blank=True, related_name='servicePackages')

    def __str__(self):
        return self.title


class Company(models.Model):
    """
    The company, which books the booth. User is an employee of the company.

    name (str): Name of the comapny.
    billing_adress (str): Adress of the company, used for billing after the exhibition.
    logo (image): Logo of the company, which will be displayed in the app.
    description (str): A description of the company, will be displayed on the exhibitor list.
    waiting_list (boolean): Boolean, if the company is on the waiting list or not.
    exhibitor_list (boolean): Boolean, if the company is on the exhibitor list or not.
    """
    name = models.CharField(max_length=200, blank=True, null=True, unique=True)
    billing_address = models.CharField(max_length=255, blank=True, null=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    description = models.CharField(max_length=1024, blank=True, null=True)
    comment = models.CharField(max_length=1024, blank=True, null=True)
    waiting_list = models.BooleanField(default=False)
    exhibitor_list = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class System(models.Model):
    """
    Represents the system as a whole. Is used to disable bookings.

    enabled (boolean): When enabled, the booking is permitted for users.
    """
    enabled = models.BooleanField(default=False)

    def __str__(self):
        x = str(self.id)
        return x
    
class SystemConfiguration(models.Model):
    """
    To configure the reimbursement. Cancel-Modal will pull the values out of this model.

    cancellation_reimbursement: The percentage of the booking price that is reimbursed when a booking is cancelled.
    cancellation_reimbursement_until: The date until which the cancellation reimbursement is valid, after this date there is no reimbursement.
    """
    cancellation_reimbursement = models.PositiveIntegerField(default=100)
    cancellation_reimbursement_until = models.DateField()

    def __str__(self):
        return "System Configuration"
    
class User(AbstractUser):
    """
    User, which extends the already established Django-User. UUID and is_verified are managed ELSEWHERE

    phone (decimal): Phone number of the user.
    privacy_policy_accepted (boolean): Will be set True when the user agrees to the privacy policy.
    company (Company): The company the user works for. 
    """
    phone = models.TextField(max_length=20, blank=True, null=True)
    privacy_policy_accepted = models.BooleanField(default=False, blank=False, null=False)
    company = models.ForeignKey('Company', on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')

    def __str__(self):
        return self.username


class Location(models.Model):
    """
    Where the booth is located. Has a name and a picture, which will be displayed in the app.

    location (str): Name of the Location (Aula, Zelt 1, ...)
    site_plan (image): Site plan of the given location.
    """
    location = models.CharField(unique=True, max_length=200)
    site_plan = models.ImageField(upload_to='site_plan/', blank=True, null=True)

    def __str__(self):
        return self.location


class ServicePackage(models.Model):
    """
    Service Package, which will be added to booth.

    name (str): Name of the package (Standard, Premium, etc.).
    price (decimal): Price of the service package.
    description (str): What this package contains.
    """
    name = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=21, decimal_places=2, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class TermsUpdateLog(models.Model):
    """
    Tracks when the terms of service are updated.

    updated_at (datetime): When the terms were last updated.
    """
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Aktualisiert am {self.updated_at.strftime('%d.%m.%Y %H:%M:%S')}"
