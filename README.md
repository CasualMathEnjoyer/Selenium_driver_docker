# Selenium_driver_docker
A simple scraping script and how to run it using docker

# What is this
a simple scraping script that loads several instances from sreality.cz using Selenium and Beautifulsoup

# How to run
we need two running containers:
1. the selenium/standalone-chrome container
2. container for the script

Initialization for the chrome container:
```
docker run -d -p 4444:4444 selenium/standalone-chrome
```

then in the folder with the dockerfile:
```
docker build -t img_name .
```

lastly:
```
docker run --network=host -it --name srealitysoupscraper img_name
```

we need to set network=host, so the container with the script sees the second container and has access to the chrome
it seems that we need always manually restart the chrome container, otherwise the script does not work

the data extracted are only saved in the container, and will be deleted when the container is deleted

this entire process can probably be simplified using docker compose
