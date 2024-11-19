-- If the environment is TEST --

--If there is a line delete that before--
delete from t_configuration where name = 'Saving File Tools';

--Insert the new value of the configuartion--
insert into t_configuration (environment, name, to_be_applied_on, value_name, single_value, dict_value, created_on, last_update, is_active) values 
('test', 'Saving File Tools', 'Global', 'File protocol', 'Local', '"link"=>"https://testodoo.issoufali.phidia.fr/web/syncorders"', now(), now(), true);


-- If the environment is PROD --

--If there is a line delete that before--
delete from t_configuration where name = 'Saving File Tools';

--Insert the new value of the configuartion--
insert into t_configuration (environment, name, to_be_applied_on, value_name, single_value, dict_value, created_on, last_update, is_active) values 
('prod', 'Saving File Tools', 'Global', 'File protocol', 'Local', '"link"=>"https://odoo.issoufali.phidia.fr/web/syncorders"', now(), now(), true);

