# WarehouseTrack
WarehouseTrack is an application designed to automate delivery processes and help with warehouse management.
It is expected that WarehouseTrack will be available by the end of May.

## How to run (Linux)
In order to start this application using sqlite follow instructions below:
1. Clone this repository
2. In project root directory create file named `.env`
3. In `.env` file add line with your Django secret key. Example: `SECRET_KEY = <your_secret_key>`
4. Run `python manage.py migrate`
5. Run `ALLOWED_HOSTS="localhost" python manage.py runserver localhost:8080`

WarehouseTrack should be available through your browser at http://localhost:8080/

## How to run (Docker)
Docker image is not available at this moment but it is planned.
