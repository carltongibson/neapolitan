from django.test import TestCase

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
