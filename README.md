# Installing local dependencies

First, generate virtual venv:

Run:

```
python3 -m venv env
```

Start virtual venv:

```
source env/bin/activate
```

Install the required dependencies:

```
pip install -r requirements.txt
```

Install the required dependencies for tests:

```
pip install -r requirements-test.txt
```

# Running specific unit test file:

```
python3 -m unittest imdb_service_request_test.py
```

# Running functions locally(using the functions-framework):

Run:
```
functions-framework --target=init_scraping
```

Open http://localhost:8080/ in your browser


# Deploying init_scraping

Run:

```
gcloud functions deploy init_scraping --runtime python39 --trigger-http --allow-unauthenticated
```

# Update env var

Run:

```
gcloud functions deploy init_scraping --update-env-vars GOOGLE_CLOUD_PROJECT=<project_id>
```

# Creating scraping_pagination_topic

Run:

```
gcloud pubsub topics create scraping_pagination_topic
```

# Deploying scraping_pagination

run:
```
gcloud functions deploy scraping_pagination --runtime python39 --trigger-topic scraping_pagination_topic
```