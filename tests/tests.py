from django.test import TestCase
from django.urls import reverse
from django.utils.html import escape

from neapolitan.views import CRUDView

from .models import Bookmark


class BookmarkView(CRUDView):
    model = Bookmark
    fields = ["url", "title", "note"]


urlpatterns = [] + BookmarkView.get_urls()


class BasicTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.homepage = Bookmark.objects.create(
            url="https://noumenal.es/",
            title="Noumenal • Dr Carlton Gibson",
            note="Carlton Gibson's homepage. Blog, Contact and Project links.",
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
