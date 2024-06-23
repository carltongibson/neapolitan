from neapolitan.views import CRUDView

from .models import Bookmark, NamedCollection


class BookmarkView(CRUDView):
    model = Bookmark
    fields = ["url", "title", "note"]
    filterset_fields = [
        "favourite",
    ]


class NamedCollectionView(CRUDView):
    model = NamedCollection
    fields = ["name", "code"]

    lookup_field = "code"
    path_converter = "uuid"

    url_base = "named_collections"
