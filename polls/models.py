from django.db import models

# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("Date at which the question is published")

    def __str__(self):
        return f"<{self.id}> {self.question_text}"


class Choice(models.Model):
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    question = models.ForeignKey(
            "Question",
            on_delete=models.CASCADE,
            related_name="choices",
            related_query_name="choice",
    )

    def __str__(self):
        return f"<{self.id}> {self.choice_text}"


