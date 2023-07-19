-- Fligth type
insert into t_flighttype (type) values ('Domestic'), ('International'), ('Regional');

-- Flight class
insert into t_flightclass (flightclass) values 
('Simple economic class'), 
('Simple business class'), 
('Round trip economic class'), 
('Round trip business class');

-- Flight cabin
insert into t_class_cabin(type, gdsprovider, sign) values
('Economic', 'Zenith', '{I,X,K,E,L,D,S,M,C,Y}'),
('Business', 'Zenith', '{C,J}'),
('Economic', 'Altea', '{U,K,L,Q,T,E,N,R,V,XG,Y,B,M,H}'),
('Economic Premium', 'Altea', '{W,S,A}'),
('Business', 'Altea', '{J,C,D,I,Z,O}');