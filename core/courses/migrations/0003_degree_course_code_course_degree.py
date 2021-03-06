# Generated by Django 4.0.3 on 2022-04-05 18:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_course_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Degree',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Академиялық дәреже')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='code',
            field=models.IntegerField(blank=True, null=True, unique=True, verbose_name='Курс коды'),
        ),
        migrations.AddField(
            model_name='course',
            name='degree',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='courses.degree'),
        ),
    ]
