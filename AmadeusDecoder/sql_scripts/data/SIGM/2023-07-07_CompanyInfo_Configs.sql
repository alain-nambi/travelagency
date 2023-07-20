delete from t_configuration where name = 'Company Information';
-- company information
insert into t_configuration(environment, name, to_be_applied_on, value_name, single_value, created_on, last_update, is_active) values
('all', 'Company Information', 'Global', 'Name', 'Mercure Voyages', now(), now(), true),
('all', 'Company Information', 'Global', 'Currency name', 'Malagasy Ariary', now(), now(), true),
('all', 'Company Information', 'Global', 'Currency code', 'MGA', now(), now(), true),
('all', 'Company Information', 'Global', 'Language code', 'fr', now(), now(), true);