from invoke import task

import settings
from fixtures.db import DbFixture
from settings import ENVIRONMENT


@task
def run(ctx):
    ctx.run(
        'FLASK_APP=app.py FLASK_DEBUG={debug} flask run --host {host} --port {port}'.format(
            debug=settings.DEBUG,
            host=settings.LOCALHOST,
            port=settings.PORT,
        )
    )


@task
def deploy_secure_settings(ctx):
    import secure_settings
    for item in secure_settings.__deploy_list__:
        ctx.run(
            'heroku config:set {item}={value}'.format(item=item, value=getattr(secure_settings, item))
        )


@task
def deploy(ctx):
    ctx.run('git push heroku master --force')


@task
def reset_db(ctx):
    if ENVIRONMENT == 'production':
        ctx.run('heroku pg:reset DATABASE --confirm clearing-house')
    elif ENVIRONMENT == 'development':
        ctx.run("psql -U ppodolsky -c 'DROP DATABASE IF EXISTS clearing_house;' postgres")
        ctx.run("psql -U ppodolsky -c 'CREATE DATABASE clearing_house;' postgres")


@task
def fill_db(ctx):
    from app import app
    DbFixture(app).commit()


@task
def tests(ctx):
    ctx.run('ENV_TYPE=testing nosetests --with-coverage --cover-package=. --cover-html --cover-erase -s')
