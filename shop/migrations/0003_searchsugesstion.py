# Generated by Django 3.2.3 on 2021-06-04 11:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20210602_2127'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchSugesstion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prod_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.productselling')),
            ],
        ),
    ]
