delete from t_configuration where name = 'TST Parser Tools';
-- TST parser tools
insert into t_configuration(environment, name, to_be_applied_on, value_name, array_value, dict_value, created_on, last_update, is_active) values
('all', 'TST Parser Tools', 'TST', 'Special agency code', ARRAY['PARFT278Z'], null, now(), now(), true),
('all', 'TST Parser Tools', 'TST', 'Passenger designations', ARRAY['MR', 'MS', 'MRS', 'DR', 'ML', 'ADT', 'INF', 'YTH', 'MSTR'], null, now(), now(), true),
('all', 'TST Parser Tools', 'TST', 'TST identifier', ARRAY['TST'], null, now(), now(), true),
('all', 'TST Parser Tools', 'TST', 'Ticket identifier', ARRAY['TKT'], null, now(), now(), true),
('all', 'TST Parser Tools', 'TST', 'Cost identifier', ARRAY['FARE', 'EQUIV', 'GRAND', 'TOTAL'], null, now(), now(), true),
('all', 'TST Parser Tools', 'TST', 'Fare identifier', ARRAY['FARE'], null, now(), now(), true),
('all', 'TST Parser Tools', 'TST', 'Fare equiv identifier', ARRAY['EQUIV'], null, now(), now(), true),
('all', 'TST Parser Tools', 'TST', 'Total identifier', ARRAY['TOTAL'], null, now(), now(), true),
('all', 'TST Parser Tools', 'TST', 'Grand Total identifier', ARRAY['GRAND', 'TOTAL'], null, now(), now(), true);