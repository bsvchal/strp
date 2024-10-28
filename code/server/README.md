## Requirements Updated

- Python 3
- [Configured .env file](../../README.md)

## How to run

1. Create and activate a new virtual environment

**MacOS / Unix**

```
python3 -m venv env
source env/bin/activate
```

**Windows (PowerShell)**

```
python3 -m venv env
.\env\Scripts\activate.bat
```

2. Install dependencies

```
pip install -r requirements.txt
```

3. Export and run the application

**MacOS / Unix**

```
export FLASK_APP=server.py
python3 -m flask --debug run --port=4242
```

**Windows (PowerShell)**

```
$env:FLASK_APP=“server.py"
python3 -m flask run --port=4242
```

4. Go to `localhost:4242` in your browser

5. Linting
The python dependencies include the [black code formatter](https://black.readthedocs.io/).  You can run this against your code, and also configure the [pre-commit](https://pre-commit.com/) hook to automatically format your code on a commit. 
Both `black` and `pre-commit` commands need to be run within your virtual environment, but once you install the pre-commit hook black will be run whenever you make a commit.  

To set up the pre-commit hook running black:
```
pre-commit install
```

Now when you make a git commit you should see something like the following: 
```git commit -m 'testing hook'
black....................................................................Passed
```

If necessary, you can run black manually and see the changes:
```
black .
```

To see what would change prior to running black 
```
black . --diff --color
```

