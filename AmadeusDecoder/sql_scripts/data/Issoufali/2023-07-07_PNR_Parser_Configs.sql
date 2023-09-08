delete from t_configuration where name = 'PNR Parser Tools';
-- PNR parser tools
insert into t_configuration(environment, name, to_be_applied_on, value_name, date_value, array_value, array_of_array_value, dict_value, created_on, last_update, is_active) values
('all', 'PNR Parser Tools', 'PNR', 'PNR identifier', null, ARRAY['RP'], null, null, now(), now(), true),
('all', 'PNR Parser Tools', 'PNR', 'PNR type', null, ARRAY['Altea'], null, null, now(), now(), true),
('all', 'PNR Parser Tools', 'PNR', 'Duplicate PNR identifier', null, ARRAY['* RR'], null, null, now(), now(), true),
('all', 'PNR Parser Tools', 'PNR', 'Split PNR identifier', null, ARRAY['* SP'], null, null, now(), now(), true),
('all', 'PNR Parser Tools', 'PNR', 'To be excluded line', null, ARRAY['OPERATED BY', 'ETA', 'ETD', 'FOR TAX/FEE'], null, null, now(), now(), true),
('all', 'PNR Parser Tools', 'PNR', 'Contact types', null, ARRAY['AP', 'APE', 'APN'], null, null, now(), now(), true),
('all', 'PNR Parser Tools', 'PNR', 'Contact type names', null, null, null, '"AP"=>"Phone", "APE"=>"Email", "APN"=>"Notification contact"', now(), now(), true),
('all', 'PNR Parser Tools', 'PNR', 'Ticket line identifier', null, ARRAY['FA', 'FHE', 'FHD'], null, null, now(), now(), true),
('all', 'PNR Parser Tools', 'PNR', 'Second degree ticket line identifier', null, ARRAY['PAX', 'INF'], null, null, now(), now(), true),
('all', 'PNR Parser Tools', 'PNR', 'Remark identifier', null, ARRAY[
	'RM', 'RC', 'RIR', 'RX', 'RCF', 'RQ', 'RIA', 
    'RIS', 'RIT', 'RIU', 'RIF', 'RII', 'RIZ'
], null, null, now(), now(), true),
('all', 'PNR Parser Tools', 'PNR', 'Passenger designations', null, ARRAY['MR', 'MS', 'MRS', 'DR', 'ML', 'ADT', 'INF', 'YTH', 'MSTR'], null, null, now(), now(), true),
('all', 'PNR Parser Tools', 'PNR', 'Possible cost currency', null, ARRAY['EUR', 'MGA', 'USD', 'MUR'], null, null, now(), now(), true),
('all', 'PNR Parser Tools', 'PNR', 'AM H line identifier', null, ARRAY['AM/H'], null, null, now(), now(), true);
