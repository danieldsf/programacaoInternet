# Generated by Django 2.0.3 on 2018-03-22 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20180322_1014'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='is_favorite',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='subscription',
            name='rating',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=2),
        ),
        migrations.AlterField(
            model_name='discountcoupon',
            name='expiration_date',
            field=models.DateField(),
        ),
    ]
