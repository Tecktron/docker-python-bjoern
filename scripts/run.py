import importlib
import os

import bjoern


host = os.getenv("BJOERN_HOST", "0.0.0.0")
port = int(os.getenv("BJOERN_PORT", "80"))
reuse_port = str(os.getenv("BJOERN_REUSEPORT", "true")).lower() == "true"
app_module = os.getenv("APP_MODULE", "")

try:
    path, application = app_module.rsplit(":", 1)
except ValueError:
    raise RuntimeError("APP_MODULE is not in valid path.to:application format")
try:
    wsgi_application = getattr(importlib.import_module(path), application)
except (AttributeError, ImportError) as e:
    raise ImportError("{} could not be imported from {}. {}".format(application, path, e))

bjoern.run(wsgi_application, host, port, reuse_port=reuse_port)
