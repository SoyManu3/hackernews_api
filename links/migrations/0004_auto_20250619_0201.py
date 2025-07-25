# Generated by Django 3.1.3 on 2025-06-19 02:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('links', '0003_vote'),
    ]

    operations = [
        migrations.RenameField(
            model_name='link',
            old_name='description',
            new_name='creador',
        ),
        migrations.AddField(
            model_name='link',
            name='fecha_lanzamiento',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='link',
            name='genero',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='link',
            name='nombre',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='link',
            name='plataforma',
            field=models.TextField(blank=True),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('link', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='links.link')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
