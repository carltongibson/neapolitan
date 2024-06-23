from .views import BookmarkView, NamedCollectionView


urlpatterns = [
    *BookmarkView.get_urls(),
    *NamedCollectionView.get_urls(),
]
