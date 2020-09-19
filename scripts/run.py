import importlib
import os

import bjoern


host = os.getenv("BJOERN_HOST", "0.0.0.0")
port = int(os.getenv("BJOERN_PORT", "80"))
app_module = os.getenv("APP_MODULE", "")

try:
    path, application = app_module.rsplit(":", 1)
except ValueError:
    print("APP_MODULE is not in valid path.to:application format")
    exit(1)
try:
    wsgi_application = getattr(importlib.import_module(path), application)
except (AttributeError, ImportError) as e:
    print("{} could not be imported from {}. {}".format(application, path, e))
    exit(8)

bjoern.run(wsgi_application, host, port)
