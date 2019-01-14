# Generated by Django 2.1.3 on 2018-11-26 23:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0002_auto_20181126_2312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='section',
            field=models.ForeignKey(blank=True, limit_choices_to={'course': models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scheduler.Course')}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='students', to='scheduler.Section'),
        ),
    ]