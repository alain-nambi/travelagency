delete from t_configuration where name = 'Ticket Parser Tools';
-- Ticket parser
insert into t_configuration(environment, name, to_be_applied_on, value_name, date_value, array_value, array_of_array_value, dict_value, created_on, last_update, is_active) values
('all', 'Ticket Parser Tools', 'Ticket', 'Ticket identifier', null, ARRAY['TKT'], null, null, now(), now(), true),
('all', 'Ticket Parser Tools', 'Ticket', 'Related PNR number identifier', null, ARRAY['LOC'], null, null, now(), now(), true),
('all', 'Ticket Parser Tools', 'Ticket', 'Ticket issuing date identifier', null, ARRAY['DOI'], null, null, now(), now(), true),
('all', 'Ticket Parser Tools', 'Ticket', 'All possible ticket statuses', null, ARRAY['OK', 'SA', 'NS'], null, null, now(), now(), true),
('all', 'Ticket Parser Tools', 'Ticket', 'IT fare identifier', null, ARRAY['IT'], null, null, now(), now(), true),
('all', 'Ticket Parser Tools', 'Ticket', 'NO ADC identifier', null, ARRAY['NO', 'ADC', 'NO ADC'], null, null, now(), now(), true),
('all', 'Ticket Parser Tools', 'Ticket', 'Cost modification identifier', null, ARRAY['A'], null, null, now(), now(), true),
('all', 'Ticket Parser Tools', 'Ticket', 'Prime ticket identifier', null, ARRAY['FE', 'BP', 'PRIME'], null, null, now(), now(), true),
('all', 'Ticket Parser Tools', 'Ticket', 'Invol remote identifier', null, ARRAY['INVOL REMOTE'], null, null, now(), now(), true),
('all', 'Ticket Parser Tools', 'Ticket', 'Credit note ticket identifier', null, ARRAY['760901', '760-901'], null, null, now(), now(), true),
('all', 'Ticket Parser Tools', 'Ticket', 'GP ticket identifier', null, ARRAY['FP OE'], null, null, now(), now(), true),
('all', 'Ticket Parser Tools', 'Ticket', 'Cost detail identifier', null, ARRAY['FARE', 'TOTALTAX', 'TOTAL'], null, null, now(), now(), true);