delete from t_configuration where name = 'Company Information';
-- company information
insert into t_configuration(environment, name, to_be_applied_on, value_name, single_value, created_on, last_update, is_active) values
('all', 'Company Information', 'Global', 'Name', 'Issoufali', now(), now(), true),
('all', 'Company Information', 'Global', 'Currency name', 'EURO', now(), now(), true),
('all', 'Company Information', 'Global', 'Currency code', 'EUR', now(), now(), true),
('all', 'Company Information', 'Global', 'Language code', 'fr', now(), now(), true);

-- related regional countries
INSERT INTO t_configuration(environment, name, to_be_applied_on, value_name, array_value, created_on, last_update, is_active) VALUES
('all', 'Company Information', 'Global', 'Regional country', ARRAY[
	'Madagascar', 'Mayotte', 'Réunion'
], now(), now(), true);