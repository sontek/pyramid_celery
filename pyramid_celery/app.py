from celery import current_app


#: The Pyramid_Celery app instance.
app = current_app._get_current_object()
