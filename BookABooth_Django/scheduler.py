from apscheduler.schedulers.background import BackgroundScheduler
from django.utils.timezone import now
from datetime import timedelta
from .models import Booking

def delete_blocked_bookings():
    """
    Method which identifies and deletes blocked Bookings older than 5 minutes.
    Sets the associated booth back to available, when Booking is deleted.
    """
    threshold = now() - timedelta(minutes=5)
    expired_bookings = Booking.objects.filter(status='blocked', received__lt=threshold)

    for booking in expired_bookings:
        if booking.booth:
            booking.booth.available = True
            booking.booth.save()

    deleted_count = expired_bookings.delete()
    print(f'[Scheduler] Deleted {deleted_count} blocked bookings')

scheduler = BackgroundScheduler()

def start():
    """
    Task is scheduled to run every minute.
    """
    scheduler.add_job(delete_blocked_bookings, 'interval', minutes=1, id='delete_blocked_expired_bookings')
    scheduler.start()