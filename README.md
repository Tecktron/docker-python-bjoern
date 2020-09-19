# Python bjoern Docker Container

A Docker container to run a WSGI Python application using
[bjoern](https://github.com/jonashaag/bjoern). Images support python 3.6+ and are
based on the [official python containers](https://hub.docker.com/_/python). The `-slim` versions are based on the similarly named python versions.

[Pull from Docker Hub](https://hub.docker.com/r/tecktron/python-bjoern/)

[View on GitHub](https://github.com/Tecktron/docker-python-bjoern)

## How to use

* You don't need to clone the GitHub repo. You can use this image as a base image for other images, using this in your `Dockerfile`:

```Dockerfile
FROM tecktron/python-bjoern:latest

COPY ./ /app
```

It will expect a file at `/app/app/wsgi.py`.

Or otherwise a file at `/app/wsgi.py`.

And will expect it to contain a variable `application` with your "WSGI" application.

Then you can build your image from the directory that has your `Dockerfile`, e.g:

```bash
docker build -t myimage ./
```

## Options

All options can be set using environment variables. These can be passed either in a wrapper dockerfile, passing in a .env file or passing them with the
-e flag to the docker call.

### Prestart Script
If you need to run any startup commands before Waitress runs (an example might be running migrations) you can override the `prestart.sh` script. This script should live within the `/app` directory in the container. The image will automatically detect and run it before starting Waitress.


### Variables

#### `MODULE_NAME`

The Python "module" (file) to be imported by Waitress, this module would contain the actual application in a variable.

By default:

* `app.wsgi` if there's a file `/app/app/main.py` or
* `wsgi` if there's a file `/app/wsgi.py`

For example, if your main file was at `/app/custom_app/custom_script.py`, you could set it like:

```bash
docker run -d -p 80:80 -e MODULE_NAME="custom_app.custom_script" myimage
```

#### `VARIABLE_NAME`

The variable inside of the Python module that contains the WSGI application.

By default:

* `application`

For example, if your main Python file has something like:

```Python
from flask import Flask
api = Flask(__name__)

@api.route("/")
def hello():
    return "Hello World from Flask"
```

In this case `api` would be the variable with the "WSGI application". You could set it like:

```bash
docker run -d -p 80:80 -e VARIABLE_NAME="api" myimage
```

#### `APP_MODULE`

The string with the Python module and the variable name passed to Waitress.

By default, set based on the variables `MODULE_NAME` and `VARIABLE_NAME`:

* `app.wsgi:application` or
* `wsgi:application`

You can set it like:

```bash
docker run -d -p 80:80 -e APP_MODULE="custom_app.custom_script:api" myimage
```

#### Host & Port Setup
By default, bjoern has been setup to server on all hostnames on port 80 using address `0.0.0.0`. This works for most applications using the basic setups listed above.

You may have different needs, so you can adjust and manipulate this by passing in environment variables to adjust the settings.

##### `BJOERN_HOST` / `BJOERN_PORT`
Pass the host and port separately as `BJOERN_HOST` and/or `BJOERN_PORT`. If the port is left out, it will default to 80.

```bash
docker run -d -p 80:8080 -e BJOERN_PORT=8080 myimage
```

#### Other

##### `BJOERN_REUSEPORT`

Bjoern supports enabling SO_REUSEPORT if available. This is set to false by default, send a `false` value to disable it.

```bash
docker run -d -p 80:80 -e BJOERN_REUSEPORT="false" myimage
```


# Credits
This dockerfile setup is based on https://github.com/tiangolo/meinheld-gunicorn-docker

bjoern is by Jonas Haag: https://github.com/jonashaag/bjoern

Python is by the Python Software Foundation. https://python.org

Docker is by Docker, Inc. https://docker.com

Built using open source software.
