from django.conf import settings


def add_context(request):
    return {'LOCAL_MEDIA_URL': settings.LOCAL_MEDIA_URL,
            'COMPRESS_URL': settings.COMPRESS_URL}
