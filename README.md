# Nerdfacts web application

The container set is based on the official [python:3-onbuild](https://hub.docker.com/_/python/) image.

## Running the app locally

- Make sure you have docker-compose installed on your machine.
- Open a terminal window in the project directory.
- Next, run `docker-compose up`. Requrirements will download automatically, and both the database and web app will start.
- Open the local IP adress as shown (if two are shown, choose the lower one).
- A large amount of pokémon will download in the background. This may take up to two hours. 
- Note: The webpage will show facts and graphs, but the information won't be reliable until after the download is finished. This may take up to two hours.