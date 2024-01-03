# neo4j
Example neo4j app with flask.

## development
The repository have setuped [dev container](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers), so it's recommend to use this plugin in vscode.
## dev container
1) open the repository in vscode as container (It will suggest automatically. If not you have to do it manually in status bar)
2) hit f5 to start the app in debug mode
### manual
1) start the services
    ```
    docker compose -f docker-compose.base -f docker-compose.dev up -d
    ```
2) connect to the running app
    ```
    docker run -it neo4j-app-1 /bin/sh
    ```
3) run the flask app as python module
    ```
    python -m app.src
    ```
## deploy
### run
run the app in deployment from source run
    ```
    docker compose -f docker-compose.base -f docker-compose.prod up -d
    ```
### build
To build deploy container independently run
    ```
    docker compose -f docker-compose.prod.yml build app
    ```
## problems
### creating files/folders
If you create new file/folder in container/vscode it will create as root user. So to avoid permissions problems you should change the owner or create it outside the container.