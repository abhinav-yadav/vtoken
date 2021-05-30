from django.urls import path,include
from .views import(
    ScriblerAdd,
    ScriblerDelete,
    BlobView,
    ArticleFiles,
    ArticleFilesEdit,
    FileDelete,
    tagged,
    PostLikeToggle,
    PostLikeAPIToggle,
    ArticleCreate,
    ArticleUpdate,
    ArticleDetail,
    ArticleDelete,
    ArticleSetting,
    articleContentCreate,
    fileUpload,
    articleContentUpdate,
)


app_name='articles'

urlpatterns = [
    path('author/add/<slug>/', ScriblerAdd.as_view(), name='edit_scribler'),
    path('author/delete/<int:pk>/', ScriblerDelete.as_view(), name='delete_scribler'),

    path('blob/<int:pk>/<str:slug>', BlobView.as_view(), name='blob'),
    path('<int:pk>/<str:slug>', ArticleFiles.as_view() , name='attachment' ),
    path('attachment/<slug>/', ArticleFilesEdit.as_view() , name='edit_attachment' ),
    path('delete-attachment/<int:pk>/', FileDelete.as_view(), name='delete_attachment'),

    path('tag/<slug:slug>/', tagged, name="tagged"),

    path('<slug>/like/', PostLikeToggle.as_view(), name='like-toggle'),
    path('api/<slug>/like/', PostLikeAPIToggle.as_view(), name='like-api-toggle'),

    path('create/',ArticleCreate.as_view() , name='create'),
    path('card-update/<slug>/', ArticleUpdate, name='update'),
    path('detail/<slug>/',ArticleDetail.as_view() , name='detail'),
    path('delete/<slug>/',ArticleDelete.as_view() , name='delete'),

    path('settings/<int:pk>/', ArticleSetting.as_view(), name = 'article_setting'),
    path('content/<int:pk>/', articleContentCreate, name='article_content'),
    path('content_update/<int:pk>/', articleContentUpdate, name='article_content_update'),
    path('upload/<int:pk>/', fileUpload, name = 'file_upload'),
]
