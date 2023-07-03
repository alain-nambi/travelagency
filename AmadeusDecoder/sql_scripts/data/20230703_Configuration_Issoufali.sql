-- company information
insert into t_configuration(environment, name, to_be_applied_on, value_name, single_value, created_on, last_update, is_active) values
(null, 'Company Information', 'Global', 'Name', 'Issoufali', now(), now(), true),
(null, 'Company Information', 'Global', 'Currency name', 'EURO', now(), now(), true),
(null, 'Company Information', 'Global', 'Currency code', 'EUR', now(), now(), true),
(null, 'Company Information', 'Global', 'Language code', 'fr', now(), now(), true);