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
('test', 'Email Source', 'Global', 'Email PNR', null,
'"address"=>"tjq.issoufali@gmail.com", "password"=>"sboptodqazliqabj"' , now(), now(), true),
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

-- TST parser tools
insert into t_configuration(environment, name, to_be_applied_on, value_name, array_value, dict_value, created_on, last_update, is_active) values
('all', 'TST Parser Tools', 'TST', 'Special agency code', ARRAY['PARFT278Z'], null, now(), now(), true),
('all', 'TST Parser Tools', 'TST', 'Passenger designations', ARRAY['MR', 'MS', 'MRS', 'DR', 'ML', 'ADT', 'INF', 'YTH', 'MSTR'], null, now(), now(), true),
('all', 'TST Parser Tools', 'TST', 'TST identifier', ARRAY['TST'], null, now(), now(), true),
('all', 'TST Parser Tools', 'TST', 'Ticket identifier', ARRAY['TKT'], null, now(), now(), true),
('all', 'TST Parser Tools', 'TST', 'Cost identifier', ARRAY['FARE', 'EQUIV', 'GRAND', 'TOTAL'], null, now(), now(), true);

-- Zenith parser tools
insert into t_configuration(environment, name, to_be_applied_on, value_name, array_value, array_of_array_value, dict_value, created_on, last_update, is_active) values
('all', 'Zenith Parser Tools', 'Zenith', 'Passenger type', ARRAY['Adulte(s)', 'Enfant(s)', 'Bébé(s)', 'Mineur(s) non accompagné'], null, null, now(), now(), true),
('all', 'Zenith Parser Tools', 'Zenith', 'Passenger designations', ARRAY['M.', 'Mme', 'Enfant', 'Bébé', 'Mlle', 'Ms.'], null, null, now(), now(), true),
('all', 'Zenith Parser Tools', 'Zenith', 'E-ticket possible format', ARRAY['e-ticket', 'e‐ĕcket', 'e‐韜���cket', 'e‐⁛cket', 'e‐�cket', 'e‐଀cket', 'e‐෶���cket', 'e‐➄cket', 'e‐ᬘ���cket', 'e‐痴���cket'], null, null, now(), now(), true),
('all', 'Zenith Parser Tools', 'Zenith', 'Itinerary header possible format', null, ARRAY[
	  ARRAY['Itinéraire', 'Vol', 'Enregistrement', 'De', 'A', 'Départ', 'Arrivée CabineEscales', null, null],
	  ARRAY['Itinéraire', 'Vol', 'Enregistrement', 'De', 'A', 'Départ', 'Arrivée', 'CabineEscales', null],
	  ARRAY['Itinéraire', 'Vol', 'Enregistrement', 'De', 'A', 'Départ', 'Arrivée', 'Cabine Escales', null],
	  ARRAY['Itinéraire', 'Vol', 'Enregistrement', 'De', 'A', 'Départ', 'Arrivée', 'Cabine', 'Escales']
], null, now(), now(), true),
('all', 'Zenith Parser Tools', 'Zenith', 'Header names', ARRAY['Itinéraire', 'Détails du tarif', 'Conditions tarifaires', 'Reçu de paiement'], null, null, now(), now(), true),
('all', 'Zenith Parser Tools', 'Zenith', 'Service carrier', ARRAY['ZD', 'TZ'], null, null, now(), now(), true),
('all', 'Zenith Parser Tools', 'Zenith', 'Airport agency code', ARRAY['DZAUU000B'], null, null, now(), now(), true),
('all', 'Zenith Parser Tools', 'Zenith', 'Current travel agency identifier', ARRAY['Issoufali', 'ISSOUFALI', 'Mayotte ATO'], null, null, now(), now(), true),
('all', 'Zenith Parser Tools', 'Zenith', 'Non relevant identifier for passenger', ARRAY['N° FFP'], null, null, now(), now(), true),
('all', 'Zenith Parser Tools', 'Zenith', 'Itinerary name', ARRAY['Itinéraire'], null, null, now(), now(), true),
('all', 'Zenith Parser Tools', 'Zenith', 'Cost detail identifier', ARRAY['Détails du tarif'], null, null, now(), now(), true),
('all', 'Zenith Parser Tools', 'Zenith', 'Ancillaries identifier', ARRAY['Ancillaries'], null, null, now(), now(), true),
('all', 'Zenith Parser Tools', 'Zenith', 'Not emitted PNR start identifier', ARRAY['VOTRE NUMERO DE DOSSIER'], null, null, now(), now(), true),
('all', 'Zenith Parser Tools', 'Zenith', 'Not emitted PNR start passenger', ARRAY['Noms des passagers'], null, null, now(), now(), true),
('all', 'Zenith Parser Tools', 'Zenith', 'Not emitted PNR start booking', ARRAY['Votre réservation :'], null, null, now(), now(), true),
('all', 'Zenith Parser Tools', 'Zenith', 'Not emitted PNR start booking cost', ARRAY['Coût total de la réservation :'], null, null, now(), now(), true),
('all', 'Zenith Parser Tools', 'Zenith', 'Not emitted pnr start opc', ARRAY['Si vous ne payez pas votre réservation avant'], null, null, now(), now(), true),
('all', 'Zenith Parser Tools', 'Zenith', 'Not emitted pnr end opc', ARRAY['(heure locale de DZA), celle-ci sera AUTOMATIQUEMENT ANNULEE.'], null, null, now(), now(), true),
('all', 'Zenith Parser Tools', 'Zenith', 'To be excluded recipient email', ARRAY['issoufali.pnr@outlook.com'], null, null, now(), now(), true),
('all', 'Zenith Parser Tools', 'Zenith', 'EMD reference start', ARRAY['Référence PNR'], null, null, now(), now(), true),
('all', 'Zenith Parser Tools', 'Zenith', 'EMD expiry date start', ARRAY['Date d''expiration'], null, null, now(), now(), true),
('all', 'Zenith Parser Tools', 'Zenith', 'EMD comment start', ARRAY['Commentaire'], null, null, now(), now(), true),
('all', 'Zenith Parser Tools', 'Zenith', 'EMD cost start', ARRAY['Montant'], null, null, now(), now(), true),
('all', 'Zenith Parser Tools', 'Zenith', 'Main pnr start identifier', ARRAY['Dossier N'], null, null, now(), now(), true),
('all', 'Zenith Parser Tools', 'Zenith', 'Passport identifier', ARRAY['passeport'], null, null, now(), now(), true),
('all', 'Zenith Parser Tools', 'Zenith', 'Passenger identifier', ARRAY['Nom du passager', 'Numéro de billet', 'Numéro de billet Service(s)', 'Numéro de billetService(s)', 'Numéro de', 'billet'], null, null, now(), now(), true),
('all', 'Zenith Parser Tools', 'Zenith', 'Payment receipt identifier', ARRAY['Reçu de paiement'], null, null, now(), now(), true),
('all', 'Zenith Parser Tools', 'Zenith', 'Total identifier', ARRAY['Total'], null, null, now(), now(), true),
('all', 'Zenith Parser Tools', 'Zenith', 'Passenger word identifier', ARRAY['passager'], null, null, now(), now(), true),
('all', 'Zenith Parser Tools', 'Zenith', 'Payment method identifier', ARRAY['Forme de', 'paiement'], null, null, now(), now(), true),
('all', 'Zenith Parser Tools', 'Zenith', 'Issuing date identifier', ARRAY['Date d''émission'], null, null, now(), now(), true),
('all', 'Zenith Parser Tools', 'Zenith', 'Issuing office identifier', ARRAY['Lieu d''émission'], null, null, now(), now(), true),
('all', 'Zenith Parser Tools', 'Zenith', 'Cost word identifier', ARRAY['Tarif'], null, null, now(), now(), true),
('all', 'Zenith Parser Tools', 'Zenith', 'Modification identifier', ARRAY['Différence tarifaire', 'Pénalité d''échange'], null, null, now(), now(), true),
('all', 'Zenith Parser Tools', 'Zenith', 'Tax identifier', ARRAY['Taxes'], null, null, now(), now(), true),
('all', 'Zenith Parser Tools', 'Zenith', 'Receipt identifier', ARRAY['Transaction/Synthèse des éléments financiers'], null, null, now(), now(), true),
('all', 'Zenith Parser Tools', 'Zenith', 'Customer name identifier', ARRAY['Nom du client'], null, null, now(), now(), true);

-- Zenith receipt parser
insert into t_configuration(environment, name, to_be_applied_on, value_name, date_value, array_value, array_of_array_value, dict_value, created_on, last_update, is_active) values
('all', 'Zenith Receipt Parser Tools', 'Zenith', 'Payment option', null, ARRAY['Comptant', 'En compte', 'Virement'], null, null, now(), now(), true),
('all', 'Zenith Receipt Parser Tools', 'Zenith', 'Ticket number prefix', null, ARRAY['Echange billet', 'EMD'], null, null, now(), now(), true),
('all', 'Zenith Receipt Parser Tools', 'Zenith', 'To be excluded keywords', null, ARRAY['Encaissement transaction', 'Encaissement Modification', 'Encaissement des suppléments'], null, null, now(), now(), true),
('all', 'Zenith Receipt Parser Tools', 'Zenith', 'Aiport agency code', null, ARRAY['DZAUU000B', 'Mayotte ATO'], null, null, now(), now(), true),
('all', 'Zenith Receipt Parser Tools', 'Zenith', 'Started process date', '2023-01-01'::timestamp, null, null, null, now(), now(), true),
('all', 'Zenith Receipt Parser Tools', 'Zenith', 'Current travel agency identifier', null, ARRAY['Issoufali', 'ISSOUFALI', 'Mayotte ATO'], null, null, now(), now(), true),
('all', 'Zenith Receipt Parser Tools', 'Zenith', 'Ticket payment part', null, ARRAY['Paiement Billet'], null, null, now(), now(), true),
('all', 'Zenith Receipt Parser Tools', 'Zenith', 'Adjustment part', null, ARRAY['Reissuance Adjustment'], null, null, now(), now(), true),
('all', 'Zenith Receipt Parser Tools', 'Zenith', 'EMD cancellation part', null, ARRAY['Annulation ancillaries'], null, null, now(), now(), true),
('all', 'Zenith Receipt Parser Tools', 'Zenith', 'Ticket cancellation part', null, ARRAY['Ticket void', 'Remboursement'], null, null, now(), now(), true),
('all', 'Zenith Receipt Parser Tools', 'Zenith', 'Penalty part', null, ARRAY['Pénalité'], null, null, now(), now(), true),
('all', 'Zenith Receipt Parser Tools', 'Zenith', 'Agency fee part', null, ARRAY['Frais d''agence'], null, null, now(), now(), true),
('all', 'Zenith Receipt Parser Tools', 'Zenith', 'EMD no number possible designation', null, ARRAY['bagage', 'equipement', 'instrument'], null, null, now(), now(), true),
('all', 'Zenith Receipt Parser Tools', 'Zenith', 'Default passenger on object', null, ARRAY['Adulte(s)'], null, null, now(), now(), true),
('all', 'Zenith Receipt Parser Tools', 'Zenith', 'EMD balancing statement part', null, ARRAY['Balancing'], null, null, now(), now(), true);

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

-- Service fee decrease request
insert into t_configuration(environment, name, to_be_applied_on, value_name, date_value, array_value, array_of_array_value, dict_value, created_on, last_update, is_active) values
('all', 'Fee Request Tools', 'Fee', 'Fee request response recipient', null, ARRAY['issoufali.pnr@gmail.com'], null, null, now(), now(), true),
('all', 'Fee Request Tools', 'Fee', 'Fee decrease request response sender', null, ARRAY['feerequest.issoufali.pnr@outlook.com'], null, null, now(), now(), true),
('all', 'Fee Request Tools', 'Fee', 'Fee request request response recipient', null, ARRAY[
	'pp@phidia.onmicrosoft.com', 
	'mihaja@phidia.onmicrosoft.com', 
	'tahina@phidia.onmicrosoft.com'
], null, null, now(), now(), true);

-- Report email
insert into t_configuration(environment, name, to_be_applied_on, value_name, date_value, array_value, array_of_array_value, dict_value, created_on, last_update, is_active) values
('all', 'Report Email', 'Fee', 'Fee history report local recipients', null, ARRAY[
	'phpr974@gmail.com',
    'pp@phidia.onmicrosoft.com',
    'mihaja@phidia.onmicrosoft.com',
    'tahina@phidia.onmicrosoft.com'
], null, null, now(), now(), true),
('all', 'Report Email', 'Fee', 'Fee history report customer recipients', null, ARRAY[
	'issoufali.pnr@outlook.com'
], null, null, now(), now(), true);

-- PNR parser tools
insert into t_configuration(environment, name, to_be_applied_on, value_name, date_value, array_value, array_of_array_value, dict_value, created_on, last_update, is_active) values
('all', 'PNR Parser Tools', 'PNR', 'PNR identifier', null, ARRAY['RP'], null, null, now(), now(), true),
('all', 'PNR Parser Tools', 'PNR', 'PNR type', null, ARRAY['Altea'], null, null, now(), now(), true),
('all', 'PNR Parser Tools', 'PNR', 'Duplicate PNR identifier', null, ARRAY['* RR'], null, null, now(), now(), true),
('all', 'PNR Parser Tools', 'PNR', 'Split PNR identifier', null, ARRAY['* SP'], null, null, now(), now(), true),
('all', 'PNR Parser Tools', 'PNR', 'To be excluded line', null, ARRAY['OPERATED BY', 'ETA', 'FOR TAX/FEE'], null, null, now(), now(), true),
('all', 'PNR Parser Tools', 'PNR', 'Contact types', null, ARRAY['AP', 'APE', 'APN'], null, null, now(), now(), true),
('all', 'PNR Parser Tools', 'PNR', 'Contact type names', null, null, null, '"AP"=>"Phone", "APE"=>"Email", "APN"=>"Notification contact"', now(), now(), true),
('all', 'PNR Parser Tools', 'PNR', 'Ticket line identifier', null, ARRAY['FA', 'FHE'], null, null, now(), now(), true),
('all', 'PNR Parser Tools', 'PNR', 'Second degree ticket line identifier', null, ARRAY['PAX', 'INF'], null, null, now(), now(), true),
('all', 'PNR Parser Tools', 'PNR', 'Remark identifier', null, ARRAY[
	'RM', 'RC', 'RIR', 'RX', 'RCF', 'RQ', 'RIA', 
    'RIS', 'RIT', 'RIU', 'RIF', 'RII', 'RIZ'
], null, null, now(), now(), true),
('all', 'PNR Parser Tools', 'PNR', 'Passenger designations', null, ARRAY['MR', 'MS', 'MRS', 'DR', 'ML', 'ADT', 'INF', 'YTH', 'MSTR'], null, null, now(), now(), true),
('all', 'PNR Parser Tools', 'PNR', 'Possible cost currency', null, ARRAY['EUR', 'MGA', 'USD', 'MUR'], null, null, now(), now(), true),
('all', 'PNR Parser Tools', 'PNR', 'AM H line identifier', null, ARRAY['AM/H'], null, null, now(), now(), true);
