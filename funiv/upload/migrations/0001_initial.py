# Generated by Django 2.2.3 on 2019-08-06 22:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import funiv.storage_backends


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('articles', '0002_auto_20190806_1854'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrivateDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('upload', models.FileField(storage=funiv.storage_backends.PrivateMediaStorage(), upload_to='')),
                ('user', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='documentsPrivate', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('upload', models.FileField(upload_to='')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('thumbnail', models.ImageField(upload_to='')),
                ('category', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='documentsCategory', to='articles.Category')),
                ('students', models.ManyToManyField(related_name='students', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='documents', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]