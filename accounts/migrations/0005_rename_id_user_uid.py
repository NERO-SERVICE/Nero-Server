# Generated by Django 5.0.7 on 2024-08-09 00:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_rename_kakao_id_user_kakaoid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='id',
            new_name='uid',
        ),
    ]