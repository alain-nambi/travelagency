docker compose down
docker volume rm travelagency_postgres_data_travelagency
docker rmi travelagency-db:latest
docker rmi travelagency-web:latest
docker compose up