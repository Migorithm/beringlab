from app.entrypoints import create_app

app = create_app()
celery = getattr(app, "celery_app", None)
