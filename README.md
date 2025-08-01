# Flask Social Media

This is a social media application built with Flask.

## Useful Commands

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

## Improvements

- [ ] Implement Celery task queue to send batch emails.
