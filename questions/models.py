from django.db import models

class Question(models.Model):
    q_id = models.BigAutoField(primary_key=True, auto_created=True)
    text = models.CharField(max_length=255)
    section = models.PositiveIntegerField(default=1)
    QUESTION_TYPES = (
        ("multiple_choice_single", "Multiple Choice Single"),
        ("multiple_choice_multiple", "Multiple Choice Multiple"), 
        ("open_ended", "Open Ended")
    )
    q_type = models.CharField(max_length=24, choices=QUESTION_TYPES, default="open_ended")

    def __str__(self) -> str:
        return self.text

class Choice(models.Model):
    c_id = models.BigAutoField(primary_key=True, auto_created=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    text = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.text

class UserSession(models.Model):
    session_key = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    nickname = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    matching_code = models.CharField(max_length=10, unique=True)

    def __str__(self) -> str:
        return self.nickname

class AnalyzableData(models.Model):
    session = models.OneToOneField(UserSession, on_delete=models.CASCADE, related_name='analyzable_data')
    age_min = models.PositiveIntegerField(null=True, blank=True)
    age_max = models.PositiveIntegerField(null=True, blank=True)
    height_min = models.PositiveIntegerField(null=True, blank=True)
    height_max = models.PositiveIntegerField(null=True, blank=True)
    zodiac_sign = models.CharField(max_length=20, blank=True, null=True)
    romance_score = models.FloatField(null=True, blank=True)
    relationship_status = models.CharField(max_length=50, blank=True, null=True)
    desired_relationship_type = models.CharField(max_length=50, blank=True, null=True)
    libido_score = models.FloatField(null=True, blank=True)
    extroversion_score = models.FloatField(null=True, blank=True)

    def __str__(self) -> str:
        return f"Analyzable Data for {self.session.nickname}"

class Answer(models.Model):
    a_id = models.BigAutoField(primary_key=True, auto_created=True)
    session = models.ForeignKey(UserSession, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField(blank=True, null=True)
    selected_choice = models.ForeignKey(Choice,
                                      on_delete=models.SET_NULL,
                                      null=True,
                                      blank=True,
                                      related_name="single_choice_answers")
    selected_choices = models.ManyToManyField(Choice, blank=True, related_name="multiple_choice_answers")

    def __str__(self) -> str:
        return f"{self.session.nickname} - {self.question.text}"
