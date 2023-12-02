# Generated by Django 4.2.7 on 2023-12-02 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bookings", "0003_booking_total_price"),
    ]

    operations = [
        migrations.AddField(
            model_name="booking",
            name="payment_status",
            field=models.CharField(
                choices=[
                    ("Pending", "Pending"),
                    ("Paid", "Paid"),
                    ("Failed", "Failed"),
                    ("Refunded", "Refunded"),
                ],
                default="Pending",
                max_length=10,
            ),
        ),
    ]
