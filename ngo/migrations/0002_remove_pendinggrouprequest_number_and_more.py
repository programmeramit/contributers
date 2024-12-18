# Generated by Django 5.1.3 on 2024-12-14 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ngo', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pendinggrouprequest',
            name='number',
        ),
        migrations.AddField(
            model_name='pendinggrouprequest',
            name='email',
            field=models.EmailField(blank=True, help_text='Enter your email', max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='pendinggrouprequest',
            name='phone_number',
            field=models.IntegerField(blank=True, help_text='Enter your phone number', null=True),
        ),
        migrations.AlterField(
            model_name='pendinggrouprequest',
            name='name',
            field=models.CharField(help_text='Enter your full name', max_length=20),
        ),
        migrations.AlterField(
            model_name='pendinggrouprequest',
            name='password',
            field=models.CharField(help_text='Enter your password', max_length=20),
        ),
    ]
