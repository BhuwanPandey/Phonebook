# Generated by Django 2.1.4 on 2020-01-29 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phonebook',
            name='images',
            field=models.ImageField(null=True, upload_to='images'),
        ),
    ]