## Instant search autocomplete application with sequence matcher

First install the required modules with

`pip install -r requirements.txt`

To run the application, first include the current directory in `PYTHONPATH` to make imports work (skip this step if you're running the server with `python flask_server.py`)

`export PYTHONPATH="$(pwd):$PYTHONPATH`

Then, add the server file name to the env variable `PTHONPATH` with 

`export FLASK_APP=flask_server.py`

And run the server with

`flask run -p 8080`