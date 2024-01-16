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

        self.stdout.write("Users filled\n")

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
        self.stdout.write("Profiles filled\n")

        # Create Tags
        tags = []
        for i in range(tags_count):
            tag = Tag(title=faker.word())
            tags.append(tag)

        Tag.objects.bulk_create(tags)
        self.stdout.write("Tags filled\n")

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

        self.stdout.write("Questions filled\n")

        # Create Answers
        answers = [
            Answer(
                content=faker.text()[:300],
                upload_date=faker.date_time_this_decade(),
                valid=random.choice([True, False]),
                question=random.choice(questions),
                user=random.choice(profiles),
                like=0,
            )
            for i in range(answers_count)
        ]
        Answer.objects.bulk_create(answers)
        self.stdout.write("Answers filled\n")

        # Create Likes
        answerLikes = []
        questionLikes = []
        weights = []
        for i in range(likes_count//2):
            if random.choice([0, 1]) == 1:
                weights = [0.7, 0.3]
            else:
                weights = [0.3, 0.7]

            questionLike = QuestionLike(
                question=random.choice(questions),
                user=random.choice(profiles),
                is_like=random.choices([True, False], weights)[0]
            )
            answerLike = AnswerLike(
                answer=random.choice(answers),
                user=random.choice(profiles),
                is_like=random.choices([True, False], weights)[0]
            )
            questionLikes.append(questionLike)
            answerLikes.append(answerLike)

            needed_index = questions.index(questionLike.question)
            if questionLike.is_like:
                questions[needed_index].like = questions[needed_index].like + 1
            else:
                questions[needed_index].like = questions[needed_index].like - 1

            needed_index = answers.index(answerLike.answer)
            if answerLike.is_like:
                answers[needed_index].like = answers[needed_index].like + 1
            else:
                answers[needed_index].like = answers[needed_index].like - 1

        QuestionLike.objects.bulk_create(questionLikes)
        AnswerLike.objects.bulk_create(answerLikes)

        Question.objects.bulk_update(questions, ['like'])
        Answer.objects.bulk_update(answers, ['like'])

        self.stdout.write(self.style.SUCCESS(f'Likes filled'))