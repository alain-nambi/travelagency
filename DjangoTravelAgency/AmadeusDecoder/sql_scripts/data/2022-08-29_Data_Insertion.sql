-- To be executed on SQL Shell

-- Airports list
COPY t_airports(iata_code,ident,type,name,elevation_ft,continent,iso_country,iso_region,municipality,gps_code,local_code,coordinates)
FROM 'F:\Projects\Django\TravelAgency\DjangoTravelAgency\AmadeusDecoder\data\airports_1.csv'
DELIMITER ','
CSV HEADER;

-- Countries list
COPY t_countries(name, code)
FROM 'F:\Projects\Django\TravelAgency\DjangoTravelAgency\AmadeusDecoder\data\data_csv.csv'
DELIMITER ','
CSV HEADER;

-- Continents list
COPY t_continents(code, name)
FROM 'F:\Projects\Django\TravelAgency\DjangoTravelAgency\AmadeusDecoder\data\continent-codes_csv.csv'
DELIMITER ','
CSV HEADER;

-- Airline companies list
COPY t_airlines(name,alias,iata,icao,callsign,country,active)
FROM 'F:\Projects\Django\TravelAgency\DjangoTravelAgency\AmadeusDecoder\data\airlines.csv'
DELIMITER ','
CSV HEADER;