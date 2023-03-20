# Django Mastery

Source code of Project from the Django Mastery Youtube Channel

### Requirements

- Python

### Installation

_Follow the steps below to get the program working on your system locally._

1. Clone the repo
    ```sh
    git clone https://github.com/Pythonian/django_mastery.git
    ```
2. Change into the directory of the cloned repo
    ```sh
    cd django_mastery
    ```
3. Build the docker image and spin up the container
    ```sh
    docker-compose -f docker-compose.yml up -d --build
    ```
4. Create your database migrations
    ```sh
    docker-compose -f docker-compose.yml exec web python manage.py migrate --noinput
    docker-compose -f docker-compose.yml exec web python manage.py collectstatic --no-input --clear
    ```
5. Populate database with Fake data
    ```sh
    docker-compose -f docker-compose.yml exec web python manage.py create_admin
    docker-compose -f docker-compose.yml exec web python manage.py create_categories
    docker-compose -f docker-compose.yml exec web python manage.py create_posts 100
    ```
6. Visit the URL via the browser
    ```sh
    http://localhost:8000/
    ```
