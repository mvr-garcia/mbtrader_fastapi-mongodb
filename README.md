# MB Trader API

## How to start up app
Define environment variables in `.env` file
```shell
MONGODB_USER=...
MONGODB_PASSWORD=...
MONGOEXPRESS_USER=...
MONGOEXPRESS_PASSWORD=...
MONGODB_URL=mongodb://<user>:<pass>@localhost:27017/
MONGODB_URL_IN_DOCKER=mongodb://<user>:<pass>@mongo-db:27017/
MB_TAPI_ID=<get your TAPI_ID from Mercado Bitcoin>
MB_TAPI_SECRET=<get your TAPI_SECRET from Mercado Bitcoin>
```
_____________

### Deploy in docker
Start up docker-compose services
```shell
docker-compose up -d
```
_____________

### Run in dev mode
If it's the first time, create venv
```shel
python -m venv venv
```

Start venv
```shell
source venv/bin/activate
```

Export environmet variables
```shell
`make envvars`
```

Run mongo-stack in docker-compose
```shell
docker-compose up -d mongo-stack
```

Run python app
```shell
uvicorn src.app:app --port 8080 --reload
```