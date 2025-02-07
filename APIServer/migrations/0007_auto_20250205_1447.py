from django.db import migrations, models
import django.core.validators


def deduplicate_waybill_numbers(apps, schema_editor):
    NomecoDelivery = apps.get_model('APIServer', 'NomecoDelivery')
    NovonordisDelivery = apps.get_model('APIServer', 'NovonordisDelivery')
    
    # Handle Nomeco deliveries
    seen_waybills = set()
    for delivery in NomecoDelivery.objects.all():
        if delivery.waybill_number in seen_waybills:
            # Append a unique suffix
            base_waybill = delivery.waybill_number[:7]  # Leave room for suffix
            suffix = 1
            while f"{base_waybill}{suffix}" in seen_waybills:
                suffix += 1
            delivery.waybill_number = f"{base_waybill}{suffix}"
            delivery.save()
        seen_waybills.add(delivery.waybill_number)
    
    # Handle Novonordis deliveries
    seen_waybills = set()
    for delivery in NovonordisDelivery.objects.all():
        if delivery.waybill_number in seen_waybills:
            base_waybill = delivery.waybill_number[:7]
            suffix = 1
            while f"{base_waybill}{suffix}" in seen_waybills:
                suffix += 1
            delivery.waybill_number = f"{base_waybill}{suffix}"
            delivery.save()
        seen_waybills.add(delivery.waybill_number)


class Migration(migrations.Migration):

    dependencies = [
        ('APIServer', '0006_auto_20250205_1444'),
    ]

    operations = [
        # First, run the deduplication
        migrations.RunPython(deduplicate_waybill_numbers),
        
        # Then add the constraints and indexes
        migrations.AlterModelOptions(
            name='apikey',
            options={'ordering': ['-created_at'], 'verbose_name': 'API Key', 'verbose_name_plural': 'API Keys'},
        ),
        migrations.AlterModelOptions(
            name='nomecodelivery',
            options={'verbose_name': 'Nomeco Delivery', 'verbose_name_plural': 'Nomeco Deliveries'},
        ),
        migrations.AlterModelOptions(
            name='novonordisdelivery',
            options={'verbose_name': 'Novonordis Delivery', 'verbose_name_plural': 'Novonordis Deliveries'},
        ),
        migrations.AlterField(
            model_name='apikey',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='apikey',
            name='is_active',
            field=models.BooleanField(db_index=True, default=True),
        ),
        migrations.AlterField(
            model_name='apikey',
            name='key',
            field=models.CharField(db_index=True, max_length=40, unique=True, validators=[django.core.validators.MinLengthValidator(40)]),
        ),
        migrations.AlterField(
            model_name='apikey',
            name='name',
            field=models.CharField(db_index=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='nomecodelivery',
            name='customer_name',
            field=models.CharField(db_index=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='nomecodelivery',
            name='name',
            field=models.CharField(db_index=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='nomecodelivery',
            name='waybill_number',
            field=models.CharField(db_index=True, max_length=8, unique=True, validators=[django.core.validators.RegexValidator(message='Waybill number must be 8 alphanumeric characters', regex='^[A-Za-z0-9]{8}$')]),
        ),
        migrations.AlterField(
            model_name='novonordisdelivery',
            name='customer_name',
            field=models.CharField(db_index=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='novonordisdelivery',
            name='name',
            field=models.CharField(db_index=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='novonordisdelivery',
            name='waybill_number',
            field=models.CharField(db_index=True, max_length=8, unique=True, validators=[django.core.validators.RegexValidator(message='Waybill number must be 8 alphanumeric characters', regex='^[A-Za-z0-9]{8}$')]),
        ),
        migrations.AddIndex(
            model_name='apikey',
            index=models.Index(fields=['user', 'is_active'], name='APIServer_a_user_id_384961_idx'),
        ),
    ]
