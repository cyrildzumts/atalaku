
UNSPLASH_CREDENTIALS_KEY = "unsplash"
UNSPLASH_CACHE_KEY = f"credentials.{UNSPLASH_CREDENTIALS_KEY}"
UNSPLASH_ACCESS_KEY = "access_key"
UNSPLASH_SECRET_KEY = "secret_key"

MAX_RECENT = 5
TOP_VIEWS_MAX = 10
EMAIL_VALIDATION_DELAY = 5 #days

headers = ["", "h1","h2", "h3", "h4", "h5", "h6"]
LIST_TYPE_MAPPING = {
    'ordered': 'ol',
    'checklist': 'ul'
}

CELERY_LOGGER_HANDLER_NAME = "async"
CELERY_LOGGER_NAME = "async"
CELERY_FILE_HANDLER_CONF = {
    'level': 'INFO',
    'class': 'logging.handlers.TimedRotatingFileHandler',
    'formatter': 'file',
    'filename':'logs/atalaku.log',
    'when' : 'midnight'
}

"""BLOCK_MAPPING = {
        'header': render_header,
        'paragraph': render_paragraph,
        'table': render_table,
        'list': render_list,
        'linkTool': render_linkTool,
        'checklist': render_checklist,
        'quote': render_quote
}"""

