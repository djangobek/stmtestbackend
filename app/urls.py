from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *
router = DefaultRouter()
router.register('botuser',BotUserViewset)
router.register('channels',TelegramChannelViewset)
urlpatterns = [
    path('',include(router.urls)),
    path('user/',GetUser.as_view()),
    path('lang/',ChangeUserLanguage.as_view()),
    path('channel/',GetTelegramChannel.as_view()),
    path('delete_channel/',DeleteTelegramChannel.as_view()),
    path('update-user-details/', UpdateUserDetails.as_view(), name='update_user_details'),
    path('tests/', TestCreateAPIView.as_view(), name='tests-list'),
    path('test/participations/', TestParticipationView.as_view(), name='test-participations'),
    path('test/participations/<str:test_code>/', TestParticipationView.as_view(), name='test-participation-detail'),
    path('test/', GetTestByCodeView.as_view(), name='get_test_by_code'),
    # path('test/<int:test_id>/participations/', TestParticipationView.as_view(), name='test_participations'),
    path('test/<str:code>/', GetTestByCodeView.as_view(), name='get_test_by_code'),
    path('test/<int:test_id>/participation/', TestParticipationView.as_view(), name='test_participations'),
    path('test/<int:test_id>/participations/', get_test_participations, name='get_test_participations'),
    path('test/participationes/create/', create_test_participation, name='create_test_participation'),
    path('test/participationers/post/', TestParticipationCreateAPIView.as_view(), name='create_test_participationer'),
    path('get/test/', TestListAPIView.as_view(), name='get_test'),
    path('update-test-status/<int:test_id>/', UpdateTestStatusAPIView.as_view(), name='update_test_status'),
    path('files/', get_files, name='get_files'),
]

