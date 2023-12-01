# Generated by Django 4.2.7 on 2023-11-30 18:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_status', models.CharField(choices=[('checked_in', 'CHECKED_IN'), ('checked_out', 'CHECKED_OUT'), ('cleaned', 'CLEANED')], default='cleaned', max_length=20)),
                ('room_number', models.IntegerField()),
                ('room_type', models.CharField(choices=[('SINGLE', 'Single'), ('DOUBLE', 'Double'), ('FAMILY', 'Family')], max_length=20)),
                ('room_beds', models.IntegerField()),
                ('room_capacity', models.IntegerField()),
                ('room_price', models.IntegerField()),
                ('room_description', models.TextField()),
                ('room_image', models.ImageField(upload_to='static/images')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_in_date', models.DateTimeField()),
                ('check_out_date', models.DateTimeField()),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookings.room')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
