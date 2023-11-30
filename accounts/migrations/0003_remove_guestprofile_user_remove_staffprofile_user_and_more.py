# Generated by Django 4.2.7 on 2023-11-30 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_user_managers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guestprofile',
            name='user',
        ),
        migrations.RemoveField(
            model_name='staffprofile',
            name='user',
        ),
        migrations.DeleteModel(
            name='Guest',
        ),
        migrations.DeleteModel(
            name='Staff',
        ),
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('ADMIN', 'Admin'), ('GUEST', 'Guest'), ('STAFF', 'Staff'), ('SUPER', 'Super')], max_length=50),
        ),
        migrations.DeleteModel(
            name='GuestProfile',
        ),
        migrations.DeleteModel(
            name='StaffProfile',
        ),
    ]