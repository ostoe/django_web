# Generated by Django 4.1 on 2023-03-13 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blogs',
            fields=[
                ('id', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('user_id', models.CharField(max_length=64)),
                ('user_name', models.CharField(max_length=50)),
                ('user_image', models.ImageField(upload_to='blogimg')),
                ('title', models.CharField(max_length=50)),
                ('content', models.TextField()),
                ('abstract', models.TextField()),
                ('created_at', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('blog_id', models.CharField(max_length=64)),
                ('user_id', models.CharField(max_length=64)),
                ('user_name', models.CharField(max_length=50)),
                ('user_image', models.ImageField(upload_to='commentimg')),
                ('content', models.TextField()),
                ('created_at', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50)),
                ('passwd', models.CharField(max_length=50)),
                ('head_img', models.ImageField(upload_to='headimg')),
                ('admin', models.IntegerField(default=0)),
                ('created_at', models.FloatField(default=0.0)),
            ],
        ),
    ]
