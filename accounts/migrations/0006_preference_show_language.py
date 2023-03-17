# Generated by Django 4.1.5 on 2023-03-14 13:21

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_show_occuption'),
    ]

    operations = [
        migrations.AddField(
            model_name='preference_show',
            name='Language',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('Assamese', 'Assamese'), ('Bengali', 'Bengali'), ('Bodo', 'Bodo'), ('Dogri', 'Dogri'), ('Gujarati', 'Gujarati'), ('Kannada', 'Kannada'), ('Kashmiri', 'Kashmiri'), ('Konkani', 'Konkani'), ('Maithili', 'Maithili'), ('Malayalam', 'Malayalam'), ('Marathi', 'Marathi'), ('Meitei', 'Meitei'), ('Nepali', 'Nepali'), ('Odia', 'Odia'), ('Punjabi', 'Punjabi'), ('Sanskrit', 'Sanskrit'), ('Santali', 'Santali'), ('Sindhi', 'Sindhi'), ('Tamil', 'Tamil'), ('Telugu', 'Telugu'), ('Urdu', 'Urdu')], default='NA', max_length=120),
        ),
    ]