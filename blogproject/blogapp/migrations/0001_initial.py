# Generated by Django 5.0.2 on 2024-02-17 17:00

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PostTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('body_blog', models.TextField()),
                ('publish_blog', models.DateField(default=django.utils.timezone.now)),
                ('creation_blog', models.DateField(auto_now_add=True)),
                ('updation_blog', models.DateField(auto_now=True)),
                ('slug', models.SlugField(unique_for_date='publish')),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='draft', max_length=50)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_posts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-publish_blog',),
            },
        ),
    ]