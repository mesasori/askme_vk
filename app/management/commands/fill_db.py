# app/management/commands/fill_db.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Profile, Tag, Question, Answer, QuestionLike, AnswerLike
from faker import Faker
import random


class Command(BaseCommand):
    help = 'Fill the database with test data'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Coefficient for data filling')

    def handle(self, *args, **options):
        ratio = options['ratio']
        fake = Faker()

        users_count = ratio
        tags_count = ratio
        question_count = ratio * 10
        answers_count = ratio * 50
        likes_count = ratio * 50

        # Create Users
        users = []
        for i in range(users_count):
            username = f"{fake.user_name()}{i}"
            user = User.objects.create_user(username=username)
            users.append(user)

        self.stdout.write("Users filled\n")
        # Create Profiles
        avatars = ["avatar1.jpg", "avatar2.jpg", "avatar3.jpg", "avatar4.jpg", "avatar5.jpg", "avatar6.jpg", "dz1.jpg"]
        avatars = [f"static/img/avatar/{avatar}" for avatar in avatars]

        for user in users:
            photo = random.choice(avatars)
            Profile.objects.create(user=user, photo=photo)

        self.stdout.write("Profiles filled\n")

        # Create Tags
        tags = []
        for i in range(tags_count):
            tag = Tag.objects.create(title=fake.word())
            tags.append(tag)

        self.stdout.write("Tags filled\n")

        # Create Questions
        for i in range(question_count):
            question = Question.objects.create(
                title=fake.sentence()[:40],
                content=fake.text()[:200],
                upload_date=fake.date_time_this_decade(),
                user=random.choice(Profile.objects.all()),
                like=random.randint(-100, 100)
            )
            question.tags.set(random.sample(tags, random.randint(1, 3)))

        self.stdout.write("Questions filled\n")

        # Create Answers
        answers = [
            Answer(
                content=fake.text()[:200],
                # create_date = fake.date_time_this_decade(),
                valid=random.choice([True, False]),
                question=random.choice(Question.objects.all()),
                user=random.choice(Profile.objects.all()),
                like=random.randint(-100, 100),
            )
            for i in range(answers_count)
        ]

        Answer.objects.bulk_create(answers)
        self.stdout.write("Answers filled\n")

        # Create Likes
        questionLikes = [
            QuestionLike(
                question=random.choice(Question.objects.all()),
                user=random.choice(Profile.objects.all()),
            )
            for i in range(likes_count)
        ]

        answerLikes = [
            AnswerLike(
                answer=random.choice(Answer.objects.all()),
                user=random.choice(Profile.objects.all())
            )
            for i in range(likes_count)
        ]

        QuestionLike.objects.bulk_create(questionLikes)
        AnswerLike.objects.bulk_create(answerLikes)

        self.stdout.write(self.style.SUCCESS(f'Likes filled'))
