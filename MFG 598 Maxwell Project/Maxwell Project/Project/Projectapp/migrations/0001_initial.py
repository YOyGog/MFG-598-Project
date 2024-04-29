# Generated by Django 4.0.2 on 2024-04-07 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SignUp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.TextField(default=None)),
                ('lastname', models.TextField(default=None)),
                ('username', models.TextField(default=None)),
                ('password', models.TextField(default=None)),
                ('confirmpassword', models.TextField(blank=True, default='0', null=True)),
                ('mailbox', models.TextField(blank=True, default='0', null=True)),
            ],
        ),
    ]