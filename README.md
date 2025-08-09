# Flask Social Media

This is a social media application built with Flask.

## Useful Commands

Lists the dependencies in a file called `requirements.txt`.

`pip freeze > requirements.txt`

Installs dependencies listed in `requirements.txt`.

`pip install -r requirements.txt`

Add support for database migrations.

`flask db init`

Creates an automatic migration script.

`flask db migrate -m "migration message"`

Applies database changes.

`flask db upgrade`

Marks an existing database as upgraded (use it if `flask db upgrade` fails for some reason, like when tables already exist).

`flask db stamp`

Removes the last migration from the database.

`flask db downgrade`

List the history of migrations.

`flask db history`

Executes unit tests.

`flask test`

Executes unit tests with coverage report.

`flask test --coverage`

## Improvements

- [ ] Implement Celery task queue to send batch emails.
- [ ] Implement markdown support for <pre> tag

## Bugs

- [ ] Add timezone=True argument to db.DateTime in all models and configure timezone functionality to make the test `test_follows` pass when testing if the follow timestamp works correctly.
