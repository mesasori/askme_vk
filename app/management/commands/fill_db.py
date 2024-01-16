from datetime import datetime

from django.db import transaction
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Profile, Tag, Question, Answer, QuestionLike, AnswerLike
from faker import Faker
import random


class Command(BaseCommand):
    help = 'Fill the database with random'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Coefficient for data filling')

    def handle(self, *args, **options):
        ratio = options['ratio']
        faker = Faker()

        users_count = ratio
        question_count = ratio * 10
        answers_count = ratio * 100
        tags_count = ratio
        likes_count = ratio * 200



        # Create Users
        users = []
        for i in range(users_count):
            username = f"{faker.user_name()}{i}"
            user = User.objects.create_user(username=username)
            users.append(user)

        self.stdout.write(f'Users filled. Time:{datetime.now().strftime("%H:%M:%S")}\n')

        # Create Profiles
        # Avatars
        avatars = ["avatar1.jpg", "avatar2.jpg", "avatar3.jpg",
                   "avatar4.jpg", "avatar5.jpg", "avatar6.jpg", "dz1.jpg"]
        avatars = [f"static/img/avatar/{avatar}" for avatar in avatars]

        profiles = []
        for user in users:
            photo = random.choice(avatars)
            profiles.append(Profile(user=user, photo=photo))

        Profile.objects.bulk_create(profiles)
        self.stdout.write(f'Profiles filled. Time:{datetime.now().strftime("%H:%M:%S")}\n')

        # Create Tags
        tags = []
        for i in range(tags_count):
            tag = Tag(title=faker.word())
            tags.append(tag)

        Tag.objects.bulk_create(tags)
        self.stdout.write(f'Tags filled. Time:{datetime.now().strftime("%H:%M:%S")}\n')

        # Create Questions
        questions = []
        for i in range(question_count):
            question = Question.objects.create(
                title=faker.sentence()[:50],
                content=faker.text()[:300],
                upload_date=faker.date_time_this_decade(),
                user=random.choice(profiles),
                like=0
            )
            question.tags.set(random.sample(tags, random.randint(1, 4)))
            questions.append(question)
            if i == question_count // 2:
                self.stdout.write(f'50% of Questions. Time:{datetime.now().strftime("%H:%M:%S")}\n')

        self.stdout.write(f'Questions 100% filled. Time:{datetime.now().strftime("%H:%M:%S")}\n')

        # Create Answers
        answers = []
        for i in range(answers_count):
            answer = Answer(
                content=faker.text()[:300],
                upload_date=faker.date_time_this_decade(),
                valid=random.choice([True, False]),
                question=random.choice(questions),
                user=random.choice(profiles),
                like=0,
            )
            answers.append(answer)
            if i == answers_count // 2:
                self.stdout.write(f'Answers 50%. Time:{datetime.now().strftime("%H:%M:%S")}\n')

        Answer.objects.bulk_create(answers)
        self.stdout.write(f'Answers filled 100%. Time:{datetime.now().strftime("%H:%M:%S")}\n')

        # Create Likes
        answerLikes = []
        questionLikes = []
        weights = []
        for i in range(likes_count // 2):
            if random.choice([0, 1]) == 1:
                weights = [0.7, 0.3]
            else:
                weights = [0.3, 0.7]
            question_index = random.randint(0, len(questions) - 1)
            answer_index = random.randint(0, len(answers) - 1)

            questionLike = QuestionLike(
                question=questions[question_index],
                user=random.choice(profiles),
                is_like=random.choices([True, False], weights)[0]
            )
            answerLike = AnswerLike(
                answer=answers[answer_index],
                user=random.choice(profiles),
                is_like=random.choices([True, False], weights)[0]
            )
            questionLikes.append(questionLike)
            answerLikes.append(answerLike)

            if questionLike.is_like:
                questions[question_index].like = questions[question_index].like + 1
            else:
                questions[question_index].like = questions[question_index].like - 1

            if answerLike.is_like:
                answers[answer_index].like = answers[answer_index].like + 1
            else:
                answers[answer_index].like = answers[answer_index].like - 1

            if i == likes_count // 4:
                self.stdout.write(f'Like filled 50% Time:{datetime.now().strftime("%H:%M:%S")}\n')

        QuestionLike.objects.bulk_create(questionLikes)
        AnswerLike.objects.bulk_create(answerLikes)

        self.stdout.write(f'Likes bulked. Time:{datetime.now().strftime("%H:%M:%S")}\n')

        with transaction.atomic():
            for question in questions:
                Question.objects.filter(id=question.id).update(like=question.like)

            self.stdout.write(f'Questions are updated. Time:{datetime.now().strftime("%H:%M:%S")}\n')

            for answer in answers:
                Answer.objects.filter(id=answer.id).update(like=answer.like)

        self.stdout.write(self.style.SUCCESS(f'Finish. Time:{datetime.now().strftime("%H:%M:%S")}\n'))