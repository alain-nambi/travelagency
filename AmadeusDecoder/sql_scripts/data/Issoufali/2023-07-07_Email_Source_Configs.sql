delete from t_configuration where name = 'Email Source';
-- email source
insert into t_configuration(environment, name, to_be_applied_on, value_name, array_value, dict_value, created_on, last_update, is_active) values
-- PNR source
('prod', 'Email Source', 'Global', 'Email PNR', null,
'"address"=>"issoufali.pnr@gmail.com", "password"=>"lhlyyumveqvyqhqo"' , now(), now(), true),
('test', 'Email Source', 'Global', 'Email PNR', null,
'"address"=>"tjq.issoufali@gmail.com", "password"=>"sboptodqazliqabj"' , now(), now(), true),
-- Error notification recipients
('prod', 'Email Source', 'Global', 'Email sending error notification recipients', ARRAY[
    'nasolo@phidia.onmicrosoft.com',
     'mihaja@phidia.onmicrosoft.com',
     'alain@phidia.onmicrosoft.com',
     'remi@phidia.onmicrosoft.com',
     'famenontsoa@outlook.com',
     'tahina@phidia.onmicrosoft.com',
     'pp@phidia.onmicrosoft.com'
], null , now(), now(), true),
('test', 'Email Source', 'Global', 'Email sending error notification recipients', ARRAY[
    'nasolo@phidia.onmicrosoft.com',
     'mihaja@phidia.onmicrosoft.com',
     'alain@phidia.onmicrosoft.com',
     'remi@phidia.onmicrosoft.com',
     'famenontsoa@outlook.com'
], null , now(), now(), true),
-- Error notification sender
('prod', 'Email Source', 'Global', 'Email sending error notification', null,
'"address"=>"errorreport.issoufali.pnr@gmail.com", "password"=>"chnversafifnzagp", "smtp"=>"smtp.gmail.com", "port"=>"587"' , now(), now(), true),
('test', 'Email Source', 'Global', 'Email sending error notification', null,
'"address"=>"errorreport.issoufali.pnr@gmail.com", "password"=>"chnversafifnzagp", "smtp"=>"smtp.gmail.com", "port"=>"587"' , now(), now(), true),
-- Anomaly sender
('prod', 'Email Source', 'Global', 'Anomaly email sender', null,
'"address"=>"anomalie.issoufali.pnr@gmail.com", "password"=>"qczyzeytdvlbcysq", "smtp"=>"smtp.gmail.com", "port"=>"587"' , now(), now(), true),
('test', 'Email Source', 'Global', 'Anomaly email sender', null,
'"address"=>"anomalie.issoufali.pnr@gmail.com", "password"=>"qczyzeytdvlbcysq", "smtp"=>"smtp.gmail.com", "port"=>"587"' , now(), now(), true),
-- PNR fetching error notification sender
('prod', 'Email Source', 'Global', 'PNR not fetched notification sender', null,
'"address"=>"anomalie.issoufali.pnr@gmail.com", "password"=>"qczyzeytdvlbcysq", "smtp"=>"smtp.gmail.com", "port"=>"587"' , now(), now(), true),
('test', 'Email Source', 'Global', 'PNR not fetched notification sender', null,
'"address"=>"anomalie.issoufali.pnr@gmail.com", "password"=>"qczyzeytdvlbcysq", "smtp"=>"smtp.gmail.com", "port"=>"587"' , now(), now(), true),
-- Fee request sender
('prod', 'Email Source', 'Global', 'Fee request sender', null,
'"address"=>"feerequest.issoufali.pnr@gmail.com", "password"=>"tnkunwvygtdkxfxg", "smtp"=>"smtp.gmail.com", "port"=>"587"' , now(), now(), true),
('test', 'Email Source', 'Global', 'Fee request sender', null,
'"address"=>"feerequest.issoufali.pnr@gmail.com", "password"=>"tnkunwvygtdkxfxg", "smtp"=>"smtp.gmail.com", "port"=>"587"' , now(), now(), true),
-- Fee request recipients
('prod', 'Email Source', 'Global', 'Fee request recipient', ARRAY[
    'superviseur@agences-issoufali.com',
    'pp@phidia.onmicrosoft.com',
    'mihaja@phidia.onmicrosoft.com',
    'tahina@phidia.onmicrosoft.com'
], null , now(), now(), true),
('test', 'Email Source', 'Global', 'Fee request recipient', ARRAY[
    'mihaja@phidia.onmicrosoft.com',
    'tahina@phidia.onmicrosoft.com',
    'famenontsoa@outlook.com'
], null , now(), now(), true),
-- PNR parsing error notification sender
('prod', 'Email Source', 'Global', 'PNR parsing error notification sender', null,
'"address"=>"errorreport.issoufali.pnr@gmail.com", "password"=>"chnversafifnzagp", "smtp"=>"smtp.gmail.com", "port"=>"587"' , now(), now(), true),
('test', 'Email Source', 'Global', 'PNR parsing error notification sender', null,
'"address"=>"errorreport.issoufali.pnr@gmail.com", "password"=>"chnversafifnzagp", "smtp"=>"smtp.gmail.com", "port"=>"587"' , now(), now(), true),
-- PNR parsing error notification recipients
('prod', 'Email Source', 'Global', 'PNR parsing error notification recipients', ARRAY[
    'nasolo@phidia.onmicrosoft.com',
    'mihaja@phidia.onmicrosoft.com',
    'alain@phidia.onmicrosoft.com',
    'remi@phidia.onmicrosoft.com',
    'famenontsoa@outlook.com',
    'tahina@phidia.onmicrosoft.com'
    'pp@phidia.onmicrosoft.com'
], null , now(), now(), true),
('test', 'Email Source', 'Global', 'PNR parsing error notification recipients', ARRAY[
    'nasolo@phidia.onmicrosoft.com',
    'mihaja@phidia.onmicrosoft.com',
    'alain@phidia.onmicrosoft.com',
    'remi@phidia.onmicrosoft.com',
    'famenontsoa@outlook.com',
    'tahina@phidia.onmicrosoft.com'
], null , now(), now(), true);