# Generated by Django 4.2.6 on 2023-11-29 17:52

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
            name='LoyaltySystem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_points', models.IntegerField(default=0)),
                ('membership_tier', models.CharField(default='Standard', max_length=50)),
                ('user', models.OneToOneField(limit_choices_to={'role': 'GUEST'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DiamondGuest',
            fields=[
                ('loyaltysystem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='loyaltySystem.loyaltysystem')),
            ],
            bases=('loyaltySystem.loyaltysystem',),
        ),
        migrations.CreateModel(
            name='GoldGuest',
            fields=[
                ('loyaltysystem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='loyaltySystem.loyaltysystem')),
            ],
            bases=('loyaltySystem.loyaltysystem',),
        ),
        migrations.CreateModel(
            name='SilverGuest',
            fields=[
                ('loyaltysystem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='loyaltySystem.loyaltysystem')),
            ],
            bases=('loyaltySystem.loyaltysystem',),
        ),
        migrations.CreateModel(
            name='StandardGuest',
            fields=[
                ('loyaltysystem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='loyaltySystem.loyaltysystem')),
            ],
            bases=('loyaltySystem.loyaltysystem',),
        ),
    ]