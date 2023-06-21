# Chat Room

- CRUD operations on Room, Message models using FBV views
- Users can search rooms by topic name, room name, and room description
- Users can filter rooms based on Topic
- User authentication via email and authorization
- Users can upload profile pictures, view and edit their user profile
- Users can post comments on rooms
- Activities and Participants feeds to view recent activities and participants users of a room

# To run this project

> Note: for Windows, use `py` instead of `python`.

## Migrations

```
$ python manage.py migrate
```

```
$ python manage.py makemigrations
```

## Create Superuser

```
$ python manage.py createsuperuser
```

## Run Server

```
$ python manage.py runserver
```
