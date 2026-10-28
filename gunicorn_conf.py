import multiprocessing
import os


bind = f"0.0.0.0:{os.getenv('PORT', '8080')}"


workers_per_core = 2
cores = multiprocessing.cpu_count()
default_workers = (cores * workers_per_core) + 1
workers = int(os.getenv("WEB_CONCURRENCY", default_workers))


worker_class = "uvicorn.workers.UvicornWorker"


keepalive = 120
timeout = 120  #
graceful_timeout = 30


loglevel = os.getenv("LOG_LEVEL", "info")
accesslog = "-"
errorlog = "-"