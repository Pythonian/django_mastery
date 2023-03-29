# Django Mastery

Source code of Project from the Django Mastery Youtube Channel

### Requirements

- Python
- Docker
- Nginx
- Postgresql

_Follow the steps below to get the program working on your system locally._

### Local setup using Makefile utility commands

1. Clone the repo
    ```sh
    git clone https://github.com/Pythonian/django_mastery.git
    ```
2. Change into the directory of the cloned repo
    ```sh
    cd django_mastery
    ```
3. Create a virtual environment and activate it
    ```sh
    make venv
    source venv/bin/activate
    ```
4. Install the project requirements
    ```sh
    make install
    ```
5. Run your db migration and create an admin account
    ```sh
    make migrations
    make admin
    ```
6. Populate the database with fake data (optional step)
    ```sh
    python manage.py create_candidates 500
    ```
7. Start your development server
    ```sh
    make runserver
    ```

### Local setup with Docker

**You need to have Docker desktop up and running before you proceed**

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
    docker-compose up -d --build
    ```
4. Create your database migrations
    ```sh
    docker-compose exec web python manage.py migrate --noinput
    docker-compose exec web python manage.py collectstatic --no-input --clear
    ```
5. Create Superuser and populate database with Fake data
    ```sh
    docker-compose exec web python manage.py createsuperuser
    docker-compose exec web python manage.py create_candidates 500
    ```
6. Visit the URL via the browser
    ```sh
    http://localhost:1337/
    ```
7. To bring down the containers
    ```sh
    docker-compose down -v
    ```