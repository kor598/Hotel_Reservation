# Generated by Django 4.2.7 on 2023-12-04 02:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_guest_remove_user_username_alter_user_email_cleaner'),
        ('loyaltySystem', '0002_remove_diamondguest_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loyaltysystem',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.guest'),
        ),
    ]
