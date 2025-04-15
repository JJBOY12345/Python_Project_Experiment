# core/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Student, Faculty

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal to create a profile when a user is created based on their role.
    """
    if created:
        if instance.role == User.STUDENT:
            # Student ID format: "S" + user_id padded to 6 digits
            student_id = f"S{instance.id:06d}"
            Student.objects.create(
                user=instance,
                student_id=student_id,
                department="Not Set",
                year_of_admission=2023  # Default value
            )
        elif instance.role == User.FACULTY:
            # Faculty ID format: "F" + user_id padded to 6 digits
            faculty_id = f"F{instance.id:06d}"
            Faculty.objects.create(
                user=instance,
                faculty_id=faculty_id,
                department="Not Set",
                designation="Not Set"
            )
