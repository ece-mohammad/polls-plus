from django.urls import path

from ads.views import (
    HomePageView,
    AdDetailView,
    AdCreateView,
    AdUpdateView,
    AdDeleteView,
    AdCommentCreateView,
    AdCommentUpdateView,
    AdCommentDeleteView,
    AdFavoriteAddView,
    AdFavoriteRemoveView,
    AdFavoriteListView,
)

app_name = "ads"

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("<int:pk>/", AdDetailView.as_view(), name="ad_details"),
    path("create/", AdCreateView.as_view(), name="ad_create"),
    path("<int:pk>/update/", AdUpdateView.as_view(), name="ad_update"),
    path("<int:pk>/delete/", AdDeleteView.as_view(), name="ad_delete"),
    path("<int:pk>/comment/", AdCommentCreateView.as_view(), name="ad_comment_create"),
    path("<int:pk>/comment/<int:comment_pk>/update/", AdCommentUpdateView.as_view(), name="ad_comment_update"),
    path("<int:pk>/comment/<int:comment_pk>/delete/", AdCommentDeleteView.as_view(), name="ad_comment_delete"),
    path("<int:pk>/favorite/", AdFavoriteAddView.as_view(), name="add_favorite"),
    path("<int:pk>/unfavorite/", AdFavoriteRemoveView.as_view(), name="remove_favorite"),
    path("favorites/", AdFavoriteListView.as_view(), name="favorites_list"),
]