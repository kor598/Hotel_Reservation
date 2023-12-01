# Generated by Django 4.2.7 on 2023-12-01 12:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0003_remove_hotel_rooms_hotelroom'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='hotel',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='hotel.hotel'),
        ),
    ]
