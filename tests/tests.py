from django.test import TestCase
from django.urls import reverse
from django.utils.html import escape

from neapolitan.views import CRUDView

from .models import Bookmark


class BookmarkView(CRUDView):
    model = Bookmark
    fields = ["url", "title", "note"]
    filterset_fields = [
        "favourite",
    ]


urlpatterns = [] + BookmarkView.get_urls()


class BasicTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.homepage = Bookmark.objects.create(
            url="https://noumenal.es/",
            title="Noumenal • Dr Carlton Gibson",
            note="Carlton Gibson's homepage. Blog, Contact and Project links.",
            favourite=True,
        )
        cls.github = Bookmark.objects.create(
            url="https://github.com/carltongibson",
            title="Carlton Gibson - GitHub",
            note="Carlton Gibson on GitHub",
        )
        cls.fosstodon = Bookmark.objects.create(
            url="https://fosstodon.org/@carlton",
            title="Carlton Gibson - Fosstodon",
            note="Carlton Gibson on Fosstodon",
        )

    def test_list(self):
        response = self.client.get("/bookmark/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.homepage.title)
        self.assertContains(response, self.github.title)
        self.assertContains(response, self.fosstodon.title)
        self.assertContains(
            response, '<a href="/bookmark/new/">Add a new bookmark</a>', html=True
        )

    def test_list_empty(self):
        Bookmark.objects.all().delete()
        response = self.client.get("/bookmark/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no bookmarks. Create one now?")
        self.assertContains(
            response, '<a href="/bookmark/new/">Add a new bookmark</a>', html=True
        )

    def test_detail(self):
        response = self.client.get(f"/bookmark/{self.homepage.pk}/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.homepage.title)
        self.assertContains(response, escape(self.homepage.note))

    def test_create(self):
        create_url = reverse("bookmark-create")

        # Load the form.
        response = self.client.get(create_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form method="POST" action="/bookmark/new/">')

        # Submit the form.
        response = self.client.post(
            create_url,
            {
                "url": "https://example.com/",
                "title": "Example",
                "note": "Example note",
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.url_name, "bookmark-detail")

    def test_delete(self):
        delete_url = reverse("bookmark-delete", args=[self.homepage.pk])

        # Load the form.
        response = self.client.get(delete_url)
        self.assertEqual(response.status_code, 200)

        # Submit the form.
        response = self.client.post(delete_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.url_name, "bookmark-list")

    def test_update(self):
        update_url = reverse("bookmark-update", args=[self.homepage.pk])

        # Load the form.
        response = self.client.get(update_url)
        self.assertEqual(response.status_code, 200)

        # Submit the form.
        response = self.client.post(
            update_url,
            {
                "url": "https://example.com/",
                "title": "Example",
                "note": "Example note",
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(
            response, reverse("bookmark-detail", args=[self.homepage.pk])
        )
        self.assertContains(response, "Example")

    def test_filter(self):
        response = self.client.get("/bookmark/?favourite=true")
        self.assertEqual(response.status_code, 200)
        self.assertSequenceEqual([self.homepage], response.context["bookmark_list"])
        self.assertContains(response, self.homepage.title)
        self.assertNotContains(response, self.github.title)
        self.assertNotContains(response, self.fosstodon.title)
