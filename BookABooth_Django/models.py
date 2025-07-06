from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.forms import ValidationError
from django.utils import timezone
from decimal import Decimal


class Booking(models.Model):
    """
    Represents a booth booking submitted by a company.

    Fields:
        received (datetime): Timestamp when the booking was received.
        status (str): Current status of the booking. Default is 'blocked'.
        confirmed (datetime): Timestamp when the booking was confirmed via email.
        price (decimal): Final price of the booking, calculated from service package and location.
        cancellationfee (decimal): Fee in case of cancellation, as a percentage of the price.
        company (Company): Company that submitted the booking.
        booth (Booth): The specific booth assigned to this booking.
    """

    class Status(models.TextChoices):
        BLOCKED = 'blocked', 'Blocked'
        CONFIRMED = 'confirmed', 'Confirmed'
        CANCELED = 'canceled', 'Canceled'

    received = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.BLOCKED)
    confirmed = models.DateTimeField(blank=True, null=True)
    price = models.DecimalField(max_digits=21, decimal_places=2, blank=True, null=True)
    cancellationfee = models.DecimalField(max_digits=21, decimal_places=2, blank=True, null=True)
    company = models.ForeignKey('Company', on_delete=models.PROTECT, related_name="company_bookings")
    booth = models.ForeignKey('Booth', on_delete=models.SET_NULL, null=True, blank=True, related_name="booth_bookings")

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
    Represents a booth that can be booked by a company.

    Fields:
        title (str): Unique name of the booth (e.g., A1, B2).
        ceiling_height (decimal): Height of the ceiling at the booth's location.
        available (bool): Indicates whether the booth is currently available.
                        This field is automatically updated via booking logic.
        location (Location): Physical location where the booth is placed.
        service_package (ManyToMany): Package(s) assigned to this booth (e.g., Standard, Premium).
    """
    title = models.CharField(unique=True, max_length=200)
    ceiling_height = models.DecimalField(max_digits=21, decimal_places=2, blank=True, null=True)
    available = models.BooleanField(default=True)
    location = models.ForeignKey('Location', on_delete=models.CASCADE, blank=True, null=True, related_name='booths')
    service_package = models.ManyToManyField('ServicePackage', blank=True, related_name='booths')

    def __str__(self):
        return self.title


class Company(models.Model):
    """
    Represents an exhibiting company participating in the event.

    Fields:
        name (str): Name of the company (must be unique).
        billing_address (str): Address used for invoicing after the exhibition.
        logo (Image): Company logo, shown in the exhibitor list and the profile.
        description (str): Short description displayed in the public exhibitor list.
        comment (str): Optional internal comment (e.g. for invoicing notes).
        waiting_list (bool): Indicates if the company is on the waiting list.
        exhibitor_list (bool): Indicates if the company should appear in the exhibitor list.
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
    Global system state used to control whether bookings are currently permitted.

    Fields:
        enabled (bool): If True, new bookings can be created. If False, booking is disabled.
    
    Note:
        Only one instance of this model should exist at any given time.
        It serves as a system-wide toggle for enabling/disabling booth bookings.
    """
    enabled = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk and System.objects.exists():
            raise ValidationError("Es darf nur eine Instanz von System geben.")
        return super(System, self).save(*args, **kwargs)

    def __str__(self):
        return f"Booking freigeschaltet: {self.enabled}"


class SystemConfiguration(models.Model):
    """
    Defines system-wide cancellation reimbursement rules for booth bookings.

    Fields:
        cancellation_reimbursement (int): Percentage (0-100) of the booking price that will be charged as a fee in the case of cancellation.
        cancellation_reimbursement_until (date): Latest date for eligibility for reimbursement. After this date, the entire booking price will be charged as a fee.

    Note:
        These values are typically used in cancellation modals or refund logic.
        Only one instance of this model should exist in the system.
    """
    cancellation_reimbursement = models.PositiveIntegerField(default=100)
    cancellation_reimbursement_until = models.DateField()

    def save(self, *args, **kwargs):
        if not self.pk and SystemConfiguration.objects.exists():
            raise ValidationError("Es darf nur eine Instanz von SystemConfiguration geben.")
        return super(SystemConfiguration, self).save(*args, **kwargs)

    def __str__(self):
        return "System Configuration"


class User(AbstractUser):
    """
    Custom user model extending Django's built-in AbstractUser.

    Fields:
        phone (str): Phone number of the user (max. 20 characters).
        privacy_policy_accepted (bool): Indicates whether the user has accepted the privacy policy.
        company (Company): Company the user is assigned to. May be null for admins.
    """
    phone = models.TextField(max_length=20, blank=True, null=True)
    privacy_policy_accepted = models.BooleanField(default=False, blank=False, null=False)
    company = models.ForeignKey('Company', on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')

    def __str__(self):
        return self.username


class Location(models.Model):
    """
    Represents a physical location where booths are placed (e.g., Aula, Tent 1).

    Fields:
        location (str): Name or label of the location. Must be unique.
        site_plan (Image): Optional site plan image, used for visual display in the frontend.
    """
    location = models.CharField(unique=True, max_length=200)
    site_plan = models.ImageField(upload_to='site_plan/', blank=False, null=False)

    def __str__(self):
        return self.location


class ServicePackage(models.Model):
    """
    Represents a service package that can be assigned to one or more booths.

    Fields:
        name (str): Name of the package (e.g., Standard, Premium).
        price (decimal): Price of the package in EUR.
        description (str): Short summary of what's included in the package.
    """
    name = models.CharField(max_length=255, blank=False, null=False)
    price = models.DecimalField(max_digits=21, decimal_places=2, blank=False, null=False)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class TermsUpdateLog(models.Model):
    """
    Log entry that records each time the terms of service are updated.

    Fields:
        updated_at (datetime): Timestamp of the update. Set automatically on creation.
    """
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Aktualisiert am {self.updated_at.strftime('%d.%m.%Y %H:%M:%S')}"
