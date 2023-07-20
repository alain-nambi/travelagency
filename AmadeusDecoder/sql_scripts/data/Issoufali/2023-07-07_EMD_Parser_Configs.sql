delete from t_configuration where name = 'EMD Parser Tools';
-- EMD parser tools
insert into t_configuration(environment, name, to_be_applied_on, value_name, array_value, dict_value, created_on, last_update, is_active) values
('all', 'EMD Parser Tools', 'Global', 'Airport agency code', ARRAY['DZAUU000B', 'Mayotte ATO'], null, now(), now(), true),
('all', 'EMD Parser Tools', 'Global', 'Special EMD description', ARRAY['DEPOSIT'], null, now(), now(), true),
('all', 'EMD Parser Tools', 'Global', 'Not feed', ARRAY['RESIDUAL VALUE', 'DISCOUNT CARD'], null, now(), now(), true),
('all', 'EMD Parser Tools', 'Global', 'EMD identifier', ARRAY['EMD'], null, now(), now(), true),
('all', 'EMD Parser Tools', 'Global', 'PNR number identifier', ARRAY['LOC'], null, now(), now(), true),
('all', 'EMD Parser Tools', 'Global', 'PNR type', ARRAY['Altea'], null, now(), now(), true),
('all', 'EMD Parser Tools', 'Global', 'EMD statuses', null,
'"O"=>1, "A"=>2, "F"=>3, "V"=>0, "R"=>4, "E"=>5, "P"=>6' , now(), now(), true),
('all', 'EMD Parser Tools', 'Global', 'EMD description identifier', ARRAY['RFIC', 'DESCRIPTION'], null, now(), now(), true),
('all', 'EMD Parser Tools', 'Global', 'EMD issuing date identifier', ARRAY['DOI'], null, now(), now(), true),
('all', 'EMD Parser Tools', 'Global', 'EMD payment method identifier', ARRAY['FP'], null, now(), now(), true),
('all', 'EMD Parser Tools', 'Global', 'NO ADC identifier', ARRAY['NO', 'ADC', 'NO ADC', 'ADC'], null, now(), now(), true),
('all', 'EMD Parser Tools', 'Global', 'Cost modification identifier', ARRAY['A'], null, now(), now(), true),
('all', 'EMD Parser Tools', 'Global', 'Cost detail identifier', ARRAY['FARE', 'EXCH VAL', 'RFND VAL', 'RFND', 'TOTAL'], null, now(), now(), true);