
# Proximity Sensor API  
  
  
## Getting Started  
   

1. Clone the repository:  
```  
git clone https://github.com/DanielVorobiov/proximity-sensor-api
```

2. Launch the application from the project directory

For Compose V1:
```
docker-compose up -d
```
For Compose V2:
```
docker compose up -d
```

## Running the unit tests
To run the unit tests use the following command

For Compose V1:
```
docker-compose exec web python manage.py test
```
For Compose V2:
```
docker compose exec web python manage.py test
```

## Docs
The API Documentation is available via a Swagger schema at this endpoint:
```
http://0.0.0.0:8000/docs/
```

## Pipelines
The github actions are available at this URL:
```
https://github.com/DanielVorobiov/proximity-sensor-api/actions
```