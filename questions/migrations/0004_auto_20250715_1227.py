from django.db import migrations

def update_question_types(apps, schema_editor):
    Question = apps.get_model('questions', 'Question')
    
    questions_to_update = {
        "Romantiklik Seviyesi (5 Üzerinden)": "slider",
        "Çekicilik Seviyesi (10 Üzerinden)": "slider",
        "Dışa Dönüklük Seviyesi (5 Üzerinden)": "slider",
        "Libido Seviyesi (10 Üzerinden)": "slider",
    }

    for question_text, q_type in questions_to_update.items():
        Question.objects.filter(text=question_text).update(q_type=q_type)

class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0003_analyzabledata_attraction_score'),
    ]

    operations = [
        migrations.RunPython(update_question_types),
    ]