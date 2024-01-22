@REM docker compose build
docker compose down
docker compose up -d
docker exec -it travelagency_db bash
cd var/lib/postgresql/backup && psql -U postgres -d db_flight_issoufali < db_flight_issoufali01122023.sql
