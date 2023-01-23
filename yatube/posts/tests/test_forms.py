from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from posts.forms import PostForm
from posts.models import Group, Post


User = get_user_model()


class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Post.objects.create(
            text="Тестовый текст",
        )
        cls.form = PostForm()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username="testuser")
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        """Валидная форма создает запись в Post."""
        posts_count = Post.objects.count()
        form_data = {
            "text": "Тестовый текст",
        }
        response = self.authorized_client.post(
            reverse("posts:post_create"), data=form_data, follow=True
        )
        self.assertRedirects(
            response, reverse(
                "posts:profile", kwargs={"username": self.user.username})
        )
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(
            Post.objects.filter(
                text="Тестовый текст",
            ).exists()
        )
        self.assertEqual(response.status_code, 200)

    def test_post_edit(self):
        self.post = Post.objects.create(author=self.user, text="Test text")
        self.group = Group.objects.create(
            title="Title text",
            slug="text-slug",
            description="Text description",
        )
        form_data = {
            "text": "New test text",
        }
        response = self.authorized_client.post(
            reverse("posts:post_edit", args=({self.post.id})),
            data=form_data,
            follow=True,
        )
        self.assertTrue(
            Post.objects.filter(
                text="New test text",
            ).exists()
        )
        self.assertEqual(response.status_code, 200)
