from openedx.core.lib.celery import APP


def celery_ping():
    i = APP.control.inspect()
    status = i.ping()
    
    return bool(status)
