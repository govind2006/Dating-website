# Generated by Django 4.1.5 on 2023-02-15 04:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Preference_show',
            fields=[
                ('username', models.CharField(max_length=150, primary_key=True, serialize=False, verbose_name='Username')),
                ('min_age', models.FloatField(blank=True, default=None, null=True, verbose_name='Min age')),
                ('max_age', models.FloatField(blank=True, default=None, null=True, verbose_name='Max age')),
                ('min_height', models.FloatField(blank=True, default=None, null=True, verbose_name='Min height')),
                ('max_height', models.FloatField(blank=True, default=None, null=True, verbose_name='Max height')),
                ('gender', models.CharField(choices=[('Other', 'Other'), ('Male', 'Male'), ('Female', 'Female')], default='NA', max_length=6, verbose_name='gender')),
                ('religion', models.CharField(choices=[('None', 'None'), ('Islam', 'Islam'), ('Hindu', 'Hindu'), ('Jain', 'Jain'), ('Christian', 'Christian'), ('Zoroastrianism', 'Zoroastrianism'), ('Sikh', 'Sikh'), ('Buddhist', 'Buddhist')], default='NA', max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Show',
            fields=[
                ('username', models.CharField(max_length=150, primary_key=True, serialize=False)),
                ('age', models.FloatField()),
                ('height', models.FloatField(blank=True)),
                ('Country', models.CharField(blank=True, max_length=120)),
                ('City', models.CharField(blank=True, max_length=120)),
                ('Distance', models.FloatField(blank=True, max_length=120)),
                ('education', models.CharField(blank=True, max_length=120)),
                ('gender', models.CharField(choices=[('Other', 'Other'), ('Male', 'Male'), ('Female', 'Female')], default='NA', max_length=6)),
                ('religion', models.CharField(choices=[('None', 'None'), ('Islam', 'Islam'), ('Hindu', 'Hindu'), ('Jain', 'Jain'), ('Christian', 'Christian'), ('Zoroastrianism', 'Zoroastrianism'), ('Sikh', 'Sikh'), ('Buddhist', 'Buddhist')], default='NA', max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='UploadedImage1',
            fields=[
                ('title', models.CharField(help_text='Enter an image title', max_length=150, primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.IntegerField(default=0)),
                ('user', models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
