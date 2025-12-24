"""
Add description and archived fields to the Form model.

This migration introduces two new optional fields on the Form model:

* ``description`` – a text field that allows administrators to provide a short
  description or instructions for respondents.  The field is optional and
  defaults to an empty string.
* ``archived`` – a boolean flag used to hide responses to a form without
  deleting them.  When set to ``True`` the form's responses will no longer
  be accessible through the administrative interface.

Existing records will have ``description`` set to ``None`` and ``archived``
set to ``False``.  This migration does not alter any existing data.
"""
from django.db import migrations, models


class Migration(migrations.Migration):
    # This migration depends on the initial migration that created the Form model.
    dependencies = [
        ("formsapp", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="form",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="form",
            name="archived",
            field=models.BooleanField(default=False),
        ),
    ]