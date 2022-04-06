# Generated by Django 3.1.7 on 2022-04-06 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ymca', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventWeekDay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_id', models.IntegerField(default=0)),
                ('weedday_id', models.PositiveSmallIntegerField(choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (7, 'Sunday')])),
            ],
        ),
    ]
