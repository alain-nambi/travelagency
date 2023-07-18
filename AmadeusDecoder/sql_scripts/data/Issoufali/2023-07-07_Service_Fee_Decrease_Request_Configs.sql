delete from t_configuration where name = 'Fee Request Tools';
-- Service fee decrease request
insert into t_configuration(environment, name, to_be_applied_on, value_name, date_value, array_value, array_of_array_value, dict_value, created_on, last_update, is_active) values
('all', 'Fee Request Tools', 'Fee', 'Fee request response recipient', null, ARRAY['issoufali.pnr@gmail.com'], null, null, now(), now(), true),
('all', 'Fee Request Tools', 'Fee', 'Fee decrease request response sender', null, ARRAY['feerequest.issoufali.pnr@outlook.com'], null, null, now(), now(), true),
('all', 'Fee Request Tools', 'Fee', 'Fee request request response recipient', null, ARRAY[
	'pp@phidia.onmicrosoft.com', 
	'mihaja@phidia.onmicrosoft.com', 
	'tahina@phidia.onmicrosoft.com'
], null, null, now(), now(), true);