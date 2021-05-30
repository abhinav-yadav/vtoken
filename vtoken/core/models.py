from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from django.shortcuts import  get_object_or_404


QUESTION_TYPE = [
    ('MCQ' , 'multiple_choices'),
    ('C-Box', 'checkboxe'),
]

class Quiz(models.Model):
    COURSE = [
    ('CSE','computer science and engineering'),
    ('IT','information technology'),
    ('ECE','electrical and communications engineering'),
    ('EEE','electrical and electronic engineering'),
    ('Mech', 'mechanical engineering'),
    ]
    author = models.ForeignKey(User, default=None, on_delete = models.SET_NULL, null =True)
    slug = models.SlugField(unique = True)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to = 'quiz_banner',
            null=True,
            blank=True,
            width_field="width_field",
            height_field="height_field",
            default='default.jpg')
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    department = models.CharField(max_length=5, choices = COURSE,default='CSE')
    year = models.IntegerField(default=0)
    deadline = models.DateField(auto_now=False,help_text = "Please use the following format: <em>YYYY-MM-DD</em>",null =True)


    def __str__(self):
        return self.title

    def get_total_no_of_questions(self):
        questions_count = len(Question.objects.filter(quiz = self))
        return questions_count

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, default=None, on_delete = models.SET_NULL, null = True)
    type = models.CharField(choices = QUESTION_TYPE, max_length = 10)
    question = models.CharField(max_length  = 1000, null = False)
    image = models.ImageField(upload_to = 'question_banner',
            null=True,
            blank=True,
            width_field="width_field",
            height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    time = models.IntegerField(default = 45)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return str(self.id)

    def get_options(self):
        options = Option.objects.filter(question=self)
        return options


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete = models.CASCADE,null = True)
    answer = models.BooleanField(default = False)
    option  = models.CharField(max_length = 400, blank = True)

    def __str__(self):
        # return 'q-'+ str(self.question.id) +'--'+self.option
        return str(self.id)

class Record(models.Model):
    user = models.ForeignKey(User, default = None, on_delete = models.SET_NULL, null = True)
    quiz = models.ForeignKey(Quiz, default = None, on_delete = models.SET_NULL, null = True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    questions = ArrayField(models.IntegerField(default = list))
    key = ArrayField(models.CharField(max_length=400, default=None))

    def __str__(self):
        s=''
        for i in self.questions:
            s +=str(i)+', '
        s = s[:-2]
        return s

    def get_record(self):
        record = get_object_or_404(Record, record=self)
        return record

class Response(models.Model):
    record = models.ForeignKey(Record, default = None, on_delete = models.CASCADE)
    answers = ArrayField(models.CharField(max_length=400, default=None, null = True))
    total_questions = models.IntegerField(default = 0)
    correct = models.IntegerField(default=0)

    def get_quiz(self):
        record = get_object_or_404(Record, record = self.record)
        quiz = get_object_or_404(Quiz, quiz = record.quiz)
        return quiz
