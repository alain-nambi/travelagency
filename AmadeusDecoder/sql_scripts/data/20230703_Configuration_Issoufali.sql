-- company information
insert into t_configuration(environment, name, to_be_applied_on, value_name, single_value, created_on, last_update, is_active) values
('all', 'Company Information', 'Global', 'Name', 'Issoufali', now(), now(), true),
('all', 'Company Information', 'Global', 'Currency name', 'EURO', now(), now(), true),
('all', 'Company Information', 'Global', 'Currency code', 'EUR', now(), now(), true),
('all', 'Company Information', 'Global', 'Language code', 'fr', now(), now(), true);

-- email source
insert into t_configuration(environment, name, to_be_applied_on, value_name, array_value, dict_value, created_on, last_update, is_active) values
('prod', 'Email Source', 'Global', 'Email PNR', null,
'"address"=>"issoufali.pnr@gmail.com", "password"=>"lhlyyumveqvyqhqo"' , now(), now(), true),
('all', 'Email Source', 'Global', 'Email sending error notification recipients', ARRAY[
    'nasolo@phidia.onmicrosoft.com',
     'mihaja@phidia.onmicrosoft.com',
     'alain@phidia.onmicrosoft.com',
     'remi@phidia.onmicrosoft.com',
     'famenontsoa@outlook.com',
     'tahina@phidia.onmicrosoft.com',
     'pp@phidia.onmicrosoft.com'
], null , now(), now(), true),
('prod', 'Email Source', 'Global', 'Email sending error notification', null,
'"address"=>"errorreport.issoufali.pnr@gmail.com", "password"=>"chnversafifnzagp", "smtp"=>"smtp.gmail.com", "port"=>"587"' , now(), now(), true),
('prod', 'Email Source', 'Global', 'Anomaly email sender', null,
'"address"=>"anomalie.issoufali.pnr@gmail.com", "password"=>"qczyzeytdvlbcysq", "smtp"=>"smtp.gmail.com", "port"=>"587"' , now(), now(), true),
('prod', 'Email Source', 'Global', 'PNR not fetched notification sender', null,
'"address"=>"anomalie.issoufali.pnr@gmail.com", "password"=>"qczyzeytdvlbcysq", "smtp"=>"smtp.gmail.com", "port"=>"587"' , now(), now(), true),
('prod', 'Email Source', 'Global', 'Fee request sender', null,
'"address"=>"feerequest.issoufali.pnr@gmail.com", "password"=>"tnkunwvygtdkxfxg", "smtp"=>"smtp.gmail.com", "port"=>"587"' , now(), now(), true),
('prod', 'Email Source', 'Global', 'PNR parsing error notification sender', null,
'"address"=>"errorreport.issoufali.pnr@gmail.com", "password"=>"chnversafifnzagp", "smtp"=>"smtp.gmail.com", "port"=>"587"' , now(), now(), true),
('all', 'Email Source', 'Global', 'PNR parsing error notification recipients', ARRAY[
    'nasolo@phidia.onmicrosoft.com',
    'mihaja@phidia.onmicrosoft.com',
    'alain@phidia.onmicrosoft.com',
    'remi@phidia.onmicrosoft.com',
    'famenontsoa@outlook.com',
    'tahina@phidia.onmicrosoft.com'
    'pp@phidia.onmicrosoft.com'
], null , now(), now(), true);

-- EMD parser tools
insert into t_configuration(environment, name, to_be_applied_on, value_name, array_value, dict_value, created_on, last_update, is_active) values
('all', 'EMD Parser Tools', 'Global', 'Airport agency code', ARRAY['DZAUU000B'], null, now(), now(), true),
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

