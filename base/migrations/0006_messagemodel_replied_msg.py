# Generated by Django 4.0.3 on 2022-03-17 21:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_alter_user_followers_alter_user_following'),
    ]

    operations = [
        migrations.AddField(
            model_name='messagemodel',
            name='replied_msg',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.messagemodel'),
        ),
    ]