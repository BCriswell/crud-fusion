crud_fusion
==============================

A demo application (Python/Django) with very basic CRUD functionality. This is only an example application, and is NOT production ready in it's current state.


LICENSE: BSD


Features
---------

* Django 1.8
* 100% test coverage
* Twitter Bootstrap_ v4.0.0 - alpha_
* End-to-end via Hitch_
* 12-Factor_ based settings via django-environ_
* Optimized development and production settings
* Registration via django-allauth_
* Custom user model AND separate Customer model with specified fields
* Grunt build for compass and livereload
* Basic e-mail configurations for sending emails via Mailgun_
* Media storage using Amazon S3
* Docker support using docker-compose_ for development and production
* Procfile_ for deploying to Heroku

Optional Integrations
---------------------

*These features can be enabled during initial project setup.*

* Serve static files from Amazon S3 or Whitenoise_
* Configuration for Celery_
* Integration with Maildump_ for local email testing
* Integration with Sentry_ for error logging
* Integration with NewRelic_ for performance monitoring
* Integration with Opbeat_ for performance monitoring

.. _alpha: http://blog.getbootstrap.com/2015/08/19/bootstrap-4-alpha/
.. _Hitch: https://github.com/hitchtest/hitchtest
.. _Bootstrap: https://github.com/twbs/bootstrap
.. _django-environ: https://github.com/joke2k/django-environ
.. _12-Factor: http://12factor.net/
.. _django-allauth: https://github.com/pennersr/django-allauth
.. _django-avatar: https://github.com/jezdez/django-avatar/
.. _Procfile: https://devcenter.heroku.com/articles/procfile
.. _Mailgun: https://mailgun.com/
.. _Whitenoise: https://whitenoise.readthedocs.org/
.. _Celery: http://www.celeryproject.org/
.. _Maildump: https://github.com/ThiefMaster/maildump
.. _Sentry: https://getsentry.com
.. _NewRelic: https://newrelic.com
.. _docker-compose: https://www.github.com/docker/compose
.. _Opbeat: https://opbeat.com/


Constraints
-----------

* Only maintained 3rd party libraries are used.
* PostgreSQL everywhere (9.0+)
* Environment variables for configuration (This won't work with Apache/mod_wsgi).

Basic Commands
--------------

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

To create an **superuser account**, use this command::

    $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run manage.py test
    $ coverage html
    $ open htmlcov/index.html



Running end to end integration tests
------------------------------------

N.B. The integration tests will not run on Windows.

To install the test runner::

  $ pip install hitch

To run the tests, enter the crud_fusion/tests directory and run the following commands::

  $ hitch init

Then run the stub test::

  $ hitch test stub.test

This will download and compile python, postgres and redis and install all python requirements so the first time it runs it may take a while.

Subsequent test runs will be much quicker.

The testing framework runs Django, Celery (if enabled), Postgres, HitchSMTP (a mock SMTP server), Firefox/Selenium and Redis.


Deployment
----------

Tools and instructions for deploying using Docker and Heroku:

Heroku
^^^^^^

.. image:: https://www.herokucdn.com/deploy/button.png
    :target: https://heroku.com/deploy

You can either push the 'deploy' button in your generated README.rst or run these commands to deploy the project to Heroku:

.. code-block:: bash

    heroku create --buildpack https://github.com/heroku/heroku-buildpack-python

    heroku addons:create heroku-postgresql:hobby-dev
    heroku pg:backups schedule --at '02:00 America/Los_Angeles' DATABASE_URL
    heroku pg:promote DATABASE_URL

    heroku addons:create heroku-redis:hobby-dev
    heroku addons:create mailgun

    heroku config:set DJANGO_ADMIN_URL=`openssl rand -base64 32`
    heroku config:set DJANGO_SECRET_KEY=`openssl rand -base64 32`
    heroku config:set DJANGO_SETTINGS_MODULE='config.settings.production'
    heroku config:set DJANGO_ALLOWED_HOSTS='.herokuapp.com'

    heroku config:set DJANGO_AWS_ACCESS_KEY_ID=YOUR_AWS_ID_HERE
    heroku config:set DJANGO_AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_ACCESS_KEY_HERE
    heroku config:set DJANGO_AWS_STORAGE_BUCKET_NAME=YOUR_AWS_S3_BUCKET_NAME_HERE

    heroku config:set DJANGO_MAILGUN_SERVER_NAME=YOUR_MALGUN_SERVER
    heroku config:set DJANGO_MAILGUN_API_KEY=YOUR_MAILGUN_API_KEY

    heroku config:set PYTHONHASHSEED=random
    heroku config:set DJANGO_ADMIN_URL=\^somelocation/

    git push heroku master
    heroku run python manage.py migrate
    heroku run python manage.py check --deploy
    heroku run python manage.py createsuperuser
    heroku open

Docker
^^^^^^

TODO: Review and revise

**Warning**

Docker is evolving extremely fast, but it has still some rough edges here and there. Compose is currently (as of version 1.4)
not considered production ready. That means you won't be able to scale to multiple servers and you won't be able to run
zero downtime deployments out of the box. Consider all this as experimental until you understand all the  implications
to run docker (with compose) on production.

**Run your app with docker-compose**

Prerequisites:

* docker (tested with 1.8)
* docker-compose (tested with 0.4)

Before you start, check out the `docker-compose.yml` file in the root of this project. This is where each component
of this application gets its configuration from. It consists of a `postgres` service that runs the database, `redis`
for caching, `nginx` as reverse proxy and last but not least the `django` application run by gunicorn.
{% if cookiecutter.use_celery == 'y' -%}
Since this application also runs Celery, there are two more services with a service called `celeryworker` that runs the
celery worker process and `celerybeat` that runs the celery beat process.
{% endif %}


All of these services except `redis` rely on environment variables set by you. There is an `env.example` file in the
root directory of this project as a starting point. Add your own variables to the file and rename it to `.env`. This
file won't be tracked by git by default so you'll have to make sure to use some other mechanism to copy your secret if
you are relying solely on git.


By default, the application is configured to listen on all interfaces on port 80. If you want to change that, open the
`docker-compose.yml` file and replace `0.0.0.0` with your own ip. If you are using `nginx-proxy`_ to run multiple
application stacks on one host, remove the port setting entirely and add `VIRTUAL_HOST={{cookiecutter.domain_name}}` to your env file.
This pass all incoming requests on `nginx-proxy`_ to the nginx service your application is using.

.. _nginx-proxy: https://github.com/jwilder/nginx-proxy

Postgres is saving its database files to `/data/{{cookiecutter.repo_name}}/postgres` by default. Change that if you wan't
something else and make sure to make backups since this is not done automatically.

To get started, pull your code from source control (don't forget the `.env` file) and change to your projects root
directory.

You'll need to build the stack first. To do that, run::

    docker-compose build

Once this is ready, you can run it with::

    docker-compose up


To run a migration, open up a second terminal and run::

   docker-compose run django python manage.py migrate

To create a superuser, run::

   docker-compose run django python manage.py createsuperuser


If you need a shell, run::

   docker-compose run django python manage.py shell_plus

To get an output of all running containers.

To check your logs, run::

   docker-compose logs

If you want to scale your application, run::

   docker-compose scale django=4
   docker-compose scale celeryworker=2


**Don't run the scale command on postgres or celerybeat**

Once you are ready with your initial setup, you wan't to make sure that your application is run by a process manager to
survive reboots and auto restarts in case of an error. You can use the process manager you are most familiar with. All
it needs to do is to run `docker-compose up` in your projects root directory.

If you are using `supervisor`, you can use this file as a starting point::

    [program:{{cookiecutter.repo_name}}]
    command=docker-compose up
    directory=/path/to/{{cookiecutter.repo_name}}
    redirect_stderr=true
    autostart=true
    autorestart=true
    priority=10


Place it in `/etc/supervisor/conf.d/{{cookiecutter.repo_name}}.conf` and run::

    supervisorctl reread
    supervisorctl start {{cookiecutter.repo_name}}

To get the status, run::

    supervisorctl status

If you have errors, you can always check your stack with `docker-compose`. Switch to your projects root directory and run::

    docker-compose ps
