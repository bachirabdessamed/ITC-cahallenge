from django.db import migrations, models
import uuid

def convert_user_id_to_uuid(apps, schema_editor):
    schema_editor.execute("""
        ALTER TABLE main_actionlog
        ALTER COLUMN user_id TYPE uuid
        USING (uuid_generate_v4());
    """)

class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_rename_created_at_actionlog_timestamp_and_more'),  # Adjust to your migration dependencies
    ]

    operations = [
        migrations.RunPython(convert_user_id_to_uuid, migrations.RunPython.noop),
    ]
