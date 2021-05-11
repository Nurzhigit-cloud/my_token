# Generated by Django 3.1 on 2021-05-10 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('title', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(max_length=100, primary_key=True, serialize=False)),
                ('image', models.ImageField(blank=True, null=True, upload_to='category/')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('image', models.ImageField(null=True, upload_to='products/')),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('active', models.BooleanField(default=True)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]