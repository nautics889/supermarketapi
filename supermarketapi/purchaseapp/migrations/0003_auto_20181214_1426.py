# Generated by Django 2.1.4 on 2018-12-14 11:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('purchaseapp', '0002_discounts'),
    ]

    operations = [
        migrations.CreateModel(
            name='Extra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_extra', models.SmallIntegerField(default=1)),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='purchaseapp.Product')),
            ],
        ),
        migrations.CreateModel(
            name='PromoProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_required', models.SmallIntegerField(default=2)),
                ('extra_product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='purchaseapp.Extra')),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='purchaseapp.Product')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='weight',
            field=models.DecimalField(decimal_places=1, default=None, max_digits=3),
        ),
        migrations.AlterField(
            model_name='discounts',
            name='coef',
            field=models.DecimalField(decimal_places=2, max_digits=3),
        ),
        migrations.AlterField(
            model_name='discounts',
            name='product',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='purchaseapp.Product'),
        ),
        migrations.AlterField(
            model_name='discounts',
            name='quantity',
            field=models.SmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='order',
            name='amount',
            field=models.SmallIntegerField(),
        ),
    ]
