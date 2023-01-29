from http import HTTPStatus

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
            text=" текст",
            author=User.objects.create(username="testuser"),
            group=Group.objects.create(
                title="testgroup",
                slug="testgroup",
                description="testdescription"
            ),
        )
        cls.form = PostForm()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username="testuser2")
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.group = Group.objects.create(
            title="testgroup2",
            slug="testgroup2",
            description="testdescription2"
        )

    def test_create_post(self):
        """Валидная форма создает запись в Post."""
        posts_count = Post.objects.count()
        form_data = {"text": "Test text", "group": self.group.pk}
        response = self.authorized_client.post(
            reverse("posts:post_create"), data=form_data, follow=True
        )

        self.assertRedirects(
            response, reverse("posts:profile",
                              kwargs={"username": self.user.username})
        )
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(
            Post.objects.filter(
                text="Test text",
            ).exists()
        )
        self.assertEqual(HTTPStatus.OK.value, 200)
        new_post = Post.objects.first()
        self.assertEqual(new_post.author, self.user)
        self.assertEqual(new_post.group, self.group)

    def test_post_edit(self):
        """Валидная форма редактирует запись в Post"""
        self.post = Post.objects.create(
            author=self.user,
            text="Test text",
            group=self.group
        )
        self.other_group = Group.objects.create(
            title="Title text",
            slug="text-slug",
            description="Text description",
        )
        form_data = {"text": "New test text", "group": self.other_group.pk}
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
        old_group_response = self.authorized_client.get(
            reverse("posts:group_list", args=(self.group.slug,))
        )
        self.assertEqual(
            old_group_response.context["page_obj"].paginator.count, 0
        )
