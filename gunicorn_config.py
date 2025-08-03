wsgi_app = "app:create_app()"
bind = "127.0.0.1:8000"
workers = 3
accesslog = "-"
errorlog = "-"
loglevel = "info"
