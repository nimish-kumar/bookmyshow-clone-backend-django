# BookMyShow Django Backend

This is a Django Graphene project that utilizes Firebase for Google authentication. It provides a starting point for building GraphQL APIs with Django, integrating Firebase for user authentication using Google accounts, and uses Poetry for package management.

## Project Setup
1. Clone the repository:

    ```shell
    git clone https://github.com/nimish-kumar/bookmyshow-clone-backend-django.git
    ```

2. Install Poetry as mentioned in the docs [here](https://python-poetry.org/docs/) if poetry not present on system.
   ```shell
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. Change to the project directory:
    ```shell
    cd bookmyshow-clone-backend-django
    ```

4. Install python packages using Poetry
    ```shell
    poetry install
    ```

5. Create a Firebase auth web project and download the Firebase Admin SDK JSON file.

6. Place the downloaded JSON file in the project root directory and rename it as firebase-adminsdk.json.

7. Add environment variable to active shell
   ```shell
   export GOOGLE_APPLICATION_CREDENTIALS="./firebase-adminsdk.json"
   ```

8. Verify the following environment variables in .env file, it should present in root directory and crate one if it does not exist.

    ```.env
    DATABASE_URL=<DB CREDENTIALS>
    FIREBASE_API_KEY=<FIREBASE API KEY>
    FIREBASE_PROJECT_ID=<FIREBASE PROJECT ID>
    FIREBASE_APP_ID=<FIREBASE APP ID>
    ```
    All of the firebase credentials can be found under firebase auth web app console.

9.  Inside the project shell, activate the environment and run the server
    ```shell
    python manage.py runserver <URL:PORT>
    ```


## Project Structure
The project structure follows the standard Django application structure, with additional files and directories for GraphQL integration, Firebase authentication, and Poetry package management.

- `bms_backend/`: This directory contains the Django project configuration.
  - `settings.py`: Includes Django and Firebase settings.
  - `asgi.py`: Contains configuration for ASGI server.
  - `wsgi.py`: Contains configuration for WSGI server.
  - `urls.py`: Contains root level URL parents/endpoints
  - `backends.py`: Contains extended backend token implementation for custom firebase token authentication.
- `firebase-adminsdk.json`: Firebase Admin SDK configuration file.
- `pyproject.toml`: Poetry configuration file.
- `poetry.lock`: Poetry lock file.

## Contributing
Contributions are welcome! If you find any issues or want to add new features, please open an issue or submit a pull request.



