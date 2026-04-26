from django.db import migrations

def criar_superuser(apps, schema_editor):
    from django.contrib.auth.models import User
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@cesar.school',
            password='admin123'
        )

class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0016_alter_incidente_status'),
    ]

    operations = [
        migrations.RunPython(criar_superuser),
    ]