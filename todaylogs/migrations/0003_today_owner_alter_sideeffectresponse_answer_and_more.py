# Generated by Django 5.0.7 on 2024-08-15 17:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todaylogs', '0002_question_remove_survey_today_alter_selfrecord_today_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='today',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sideeffectresponse',
            name='answer',
            field=models.CharField(choices=[('1', '전혀 없음'), ('2', '거의 없음'), ('3', '조금 있음'), ('4', '꽤 있음'), ('5', '많이 있음')], max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='surveyresponse',
            name='answer',
            field=models.CharField(choices=[('1', '매우 나쁨'), ('2', '나쁨'), ('3', '보통'), ('4', '좋음'), ('5', '매우 좋음')], max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='today',
            name='next_appointment_date',
            field=models.DateField(null=True),
        ),
    ]