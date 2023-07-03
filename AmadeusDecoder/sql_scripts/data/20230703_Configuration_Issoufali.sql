-- company information
insert into t_configuration(environment, name, to_be_applied_on, value_name, single_value, created_on, last_update) values
(null, 'Company Information', 'Global', 'Name', 'Issoufali', now(), now()),
(null, 'Company Information', 'Global', 'Currency name', 'EURO', now(), now()),
(null, 'Company Information', 'Global', 'Currency code', 'EUR', now(), now()),
(null, 'Company Information', 'Global', 'Language code', 'fr', now(), now());