# Generated by Django 2.1.2 on 2018-10-15 14:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('slug', models.CharField(max_length=250, unique=True)),
                ('type', models.CharField(choices=[('anime', 'Anime'), ('anime-season', 'Anime Seasons'), ('anime-tag', 'Anime Tags'), ('movie', 'Movies'), ('tv', 'TV Shows')], default='unknown', max_length=20)),
                ('description', models.TextField(blank=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'tag',
            },
        ),
        migrations.CreateModel(
            name='TagChildren',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('child', models.ForeignKey(db_column='child_tag_id', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='data.Tag')),
                ('parent', models.ForeignKey(db_column='parent_tag_id', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='data.Tag')),
            ],
            options={
                'db_table': 'tag_children',
            },
        ),
        migrations.AddField(
            model_name='tag',
            name='children',
            field=models.ManyToManyField(related_name='parents', through='data.TagChildren', to='data.Tag'),
        ),
    ]
