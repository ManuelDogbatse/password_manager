# Password Manager by Manuel Dogbatse
Hi, this is my custom password manager made with Python and Docker.

To use this, make sure you have Docker Desktop installed on your computer. If not, click this link to download and install it: [Docker](https://docs.docker.com/get-docker/)

Then while Docker is open, enter the terminal and go to the directory where you have saved this repository:
```
cd <PATH_TO_DIRECTORY>
```
Build the Docker images:
```
docker compose build
```
Start the application:
```
docker compose run --rm app
```
After exiting the app, make sure to close the database:
```
docker compose stop
```