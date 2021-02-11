# Generated by Django 3.1.6 on 2021-02-11 09:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('resources', '0003_auto_20210211_1237'),
    ]

    state_operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(help_text='Enter a URL-friendly name', unique=True)),
                ('last_edit', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=50)),
                ('summary', models.TextField(blank=True, max_length=200, null=True)),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('url', models.URLField(help_text='Enter the video URL here', verbose_name='URL')),
                ('authors', models.ManyToManyField(related_name='videos_video_authors', related_query_name='videos_video_author', to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='resources.category')),
                ('tags', models.ManyToManyField(blank=True, help_text='Select some tags for this resource', related_name='videos_video_tags', related_query_name='videos_video_tag', to='resources.Tag')),
            ],
            options={
                'ordering': ['-date_posted'],
                'abstract': False,
            },
        ),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(state_operations=state_operations)
    ]
