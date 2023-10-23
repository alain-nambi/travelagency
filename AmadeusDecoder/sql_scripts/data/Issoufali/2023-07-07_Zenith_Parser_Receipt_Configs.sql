delete from t_configuration where name = 'Zenith Receipt Parser Tools';
-- Zenith receipt parser
insert into t_configuration(environment, name, to_be_applied_on, value_name, date_value, array_value, array_of_array_value, dict_value, created_on, last_update, is_active) values
('all', 'Zenith Receipt Parser Tools', 'Zenith', 'Payment option', null, ARRAY['Comptant', 'En compte', 'Virement'], null, null, now(), now(), true),
('all', 'Zenith Receipt Parser Tools', 'Zenith', 'Ticket number prefix', null, ARRAY['Echange billet', 'EMD'], null, null, now(), now(), true),
('all', 'Zenith Receipt Parser Tools', 'Zenith', 'To be excluded keywords', null, ARRAY['Encaissement transaction', 'Encaissement Modification', 'Encaissement des suppléments', 'Décaissement transaction'], null, null, now(), now(), true),
('all', 'Zenith Receipt Parser Tools', 'Zenith', 'Aiport agency code', null, ARRAY['DZAUU000B', 'Mayotte ATO'], null, null, now(), now(), true),
('all', 'Zenith Receipt Parser Tools', 'Zenith', 'Started process date', '2023-01-01'::timestamp, null, null, null, now(), now(), true),
('all', 'Zenith Receipt Parser Tools', 'Zenith', 'Current travel agency identifier', null, ARRAY['Issoufali', 'ISSOUFALI', 'Mayotte ATO'], null, null, now(), now(), true),
('all', 'Zenith Receipt Parser Tools', 'Zenith', 'Ticket payment part', null, ARRAY['Paiement Billet'], null, null, now(), now(), true),
('all', 'Zenith Receipt Parser Tools', 'Zenith', 'Adjustment part', null, ARRAY['Reissuance Adjustment', 'Réajustement tarifaire'], null, null, now(), now(), true),
('all', 'Zenith Receipt Parser Tools', 'Zenith', 'EMD cancellation part', null, ARRAY['Annulation ancillaries'], null, null, now(), now(), true),
('all', 'Zenith Receipt Parser Tools', 'Zenith', 'Ticket cancellation part', null, ARRAY['Ticket void', 'Remboursement'], null, null, now(), now(), true),
('all', 'Zenith Receipt Parser Tools', 'Zenith', 'Penalty part', null, ARRAY['Pénalité'], null, null, now(), now(), true),
('all', 'Zenith Receipt Parser Tools', 'Zenith', 'Agency fee part', null, ARRAY['Frais d''agence'], null, null, now(), now(), true),
('all', 'Zenith Receipt Parser Tools', 'Zenith', 'EMD no number possible designation', null, ARRAY['bagage', 'equipement', 'instrument'], null, null, now(), now(), true),
('all', 'Zenith Receipt Parser Tools', 'Zenith', 'Default passenger on object', null, ARRAY['Adulte(s)'], null, null, now(), now(), true),
('all', 'Zenith Receipt Parser Tools', 'Zenith', 'EMD balancing statement part', null, ARRAY['Balancing'], null, null, now(), now(), true);