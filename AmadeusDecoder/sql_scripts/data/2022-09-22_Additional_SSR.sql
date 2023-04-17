-- Additional SSR
insert into t_ssr(code, freeflowtext, suppliedbyairline) values
('CTCE', FALSE, FALSE ),
('CTCM', TRUE, FALSE ),
('CTCR', FALSE, FALSE );

insert into t_ssr_description(ssr_id, lang, description) values
((select id from t_ssr where code = 'CTCE'), 'en', 'Passenger''s email address'),
((select id from t_ssr where code = 'CTCE'), 'fr', 'Adresse email du passager'),
((select id from t_ssr where code = 'CTCM'), 'en', 'Passenger''s mobile number'),
((select id from t_ssr where code = 'CTCM'), 'fr', 'Numéro téléphone du passager'),
((select id from t_ssr where code = 'CTCR'), 'en', 'Passenger refuses to provide their contact'),
((select id from t_ssr where code = 'CTCR'), 'fr', 'Le passager a refusé de donner son contact');