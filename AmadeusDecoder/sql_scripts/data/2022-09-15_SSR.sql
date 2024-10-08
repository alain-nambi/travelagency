-- insert all SSRs code
insert into t_ssr(code, freeflowtext, suppliedbyairline) values
('ADTK', FALSE, TRUE ),
('AVHI', TRUE, FALSE ),
('AVML', FALSE, FALSE ),
('BBML', FALSE, FALSE ),
('BIKE', FALSE, FALSE ),
('BLML', FALSE, FALSE ),
('BLND', FALSE, FALSE ),
('BSCT', FALSE, FALSE ),
('BULK', TRUE, FALSE ),
('CBBG', TRUE, FALSE ),
('CHLD', FALSE, FALSE ),
('CHML', FALSE, FALSE ),
('CKIN', TRUE, FALSE ),
('CLID', FALSE, FALSE ),
('COUR', FALSE, FALSE ),
('CRUZ', FALSE, FALSE ),
('DBML', FALSE, FALSE ),
('DEAF', FALSE, FALSE ),
('DEPA', FALSE, FALSE ),
('DEPU', FALSE, FALSE ),
('DOCA', FALSE, FALSE ),
('DOCO', FALSE, FALSE ),
('DOCS', FALSE, FALSE ),
('DPNA', TRUE, FALSE ),
('EPAY', FALSE, FALSE ),
('ESAN', TRUE, FALSE ),
('EXST', TRUE, FALSE ),
('FOID', TRUE, FALSE ),
('FPML', FALSE, FALSE ),
('FQTR', FALSE, FALSE ),
('FQTS', FALSE, FALSE ),
('FQTU', FALSE, FALSE ),
('FQTV', FALSE, FALSE ),
('FRAG', TRUE, FALSE ),
('FRAV', FALSE, FALSE ),
('GFML', FALSE, FALSE ),
('GPST', FALSE, FALSE ),
('GRPF', TRUE, FALSE ),
('GRPS', FALSE, FALSE ),
('HNML', FALSE, FALSE ),
('INFT', TRUE, FALSE ),
('JPML', FALSE, FALSE ),
('KSML', FALSE, FALSE ),
('LANG', TRUE, FALSE ),
('LCML', FALSE, FALSE ),
('LFML', FALSE, FALSE ),
('LSML', FALSE, FALSE ),
('MAAS', TRUE, FALSE ),
('MEDA', FALSE, FALSE ),
('MOML', FALSE, FALSE ),
('NAME', FALSE, FALSE ),
('NFML', FALSE, FALSE ),
('NLML', FALSE, FALSE ),
('NSSA', FALSE, FALSE ),
('NSSB', FALSE, FALSE ),
('NSST', FALSE, FALSE ),
('NSSW', FALSE, FALSE ),
('OTHS', FALSE, FALSE ),
('PCTC', FALSE, FALSE ),
('PETC', FALSE, FALSE ),
('PICA', FALSE, FALSE ),
('PICU', FALSE, FALSE ),
('RQST', FALSE, FALSE ),
('RVML', FALSE, FALSE ),
('SEAT', TRUE, FALSE ),
('SEMN', TRUE, FALSE ),
('SFML', FALSE, FALSE ),
('SLPR', FALSE, FALSE ),
('SMSA', FALSE, FALSE ),
('SMSB', FALSE, FALSE ),
('SMST', FALSE, FALSE ),
('SMSW', FALSE, FALSE ),
('SPEQ', TRUE, FALSE ),
('SPML', TRUE, FALSE ),
('STCR', FALSE, FALSE ),
('SVAN', FALSE, FALSE ),
('TKNA', FALSE, TRUE ),
('TKNC', FALSE, TRUE ),
('TKNE', FALSE, TRUE ),
('TKNM', FALSE, TRUE ),
('TKTL', FALSE, FALSE ),
('TWOV', FALSE, FALSE ),
('UMNR', TRUE, FALSE ),
('VGML', FALSE, FALSE ),
('VJML', FALSE, FALSE ),
('VLML', FALSE, FALSE ),
('VOML', FALSE, FALSE ),
('WCBD', FALSE, FALSE ),
('WCBW', FALSE, FALSE ),
('WCHC', FALSE, FALSE ),
('WCHR', FALSE, FALSE ),
('WCHS', FALSE, FALSE ),
('WCMP', FALSE, FALSE ),
('WCOB', FALSE, FALSE ),
('XBAG', TRUE, FALSE ),
('WEAP', FALSE, FALSE );

-- insert all SSRs description
insert into t_ssr_description(ssr_id, lang, description) values
(1, 'en', 'Advise if ticketed (PNR will be placed in queue 1, category 6 of the responsible office)'),
(1, 'fr', 'Indiquer si le billet est entré (le PNR sera placé dans la file d''appel 1, catégorie 6 du bureau responsable)'),
(2, 'en', 'Animal in hold'),
(2, 'fr', 'Animal en cale'),
(3, 'en', 'Vegetarian Hindu meal'),
(3, 'fr', 'Repas hindou végétarien'),
(4, 'en', 'Baby meal'),
(4, 'fr', 'Repas pour bébé'),
(5, 'en', 'Bicycle in hold'),
(5, 'fr', 'Vélo en soute'),
(6, 'en', 'Bland meal'),
(6, 'fr', 'Repas Bland'),
(7, 'en', 'Blind passenger'),
(7, 'fr', 'Passager aveugle'),
(8, 'en', 'Bassinet/carrycot/baby basket'),
(8, 'fr', 'Berceau/landeau/couffin pour bébé'),
(9, 'en', 'Bulky baggage'),
(9, 'fr', 'Bagages encombrants'),
(10, 'en', 'Cabin baggage requiring seats'),
(10, 'fr', 'Bagage cabine nécessitant des sièges'),
(11, 'en', 'Child'),
(11, 'fr', 'Enfant'),
(12, 'en', 'Child meal'),
(12, 'fr', 'Repas pour enfants'),
(13, 'en', 'Information for airport personnel'),
(13, 'fr', 'Informations destinées au personnel de l''aéroport'),
(14, 'en', 'Corporate client code used by all GDSs'),
(14, 'fr', 'Code client d''entreprise utilisé par tous les GDS'),
(15, 'en', 'Commercial courier'),
(15, 'fr', 'Coursier commercial'),
(16, 'en', 'Cruise passenger'),
(16, 'fr', 'Passager de croisière'),
(17, 'en', 'Diabetic meal'),
(17, 'fr', 'Repas pour diabétiques'),
(18, 'en', 'Deaf passenger'),
(18, 'fr', 'Passager sourd'),
(19, 'en', 'Deportee, accompanied by an escort'),
(19, 'fr', 'Déporté sous escorte'),
(20, 'en', 'Deportee, unaccompanied'),
(20, 'fr', 'Déporté non accompagné'),
(21, 'en', 'Advance Passenger Information System (APIS) address details'),
(21, 'fr', 'Détails de l''adresse du système d''informations préalables sur les passagers (APIS)'),
(22, 'en', 'Advance Passenger Information System (APIS) visa'),
(22, 'fr', 'Visa du système d''informations préalables sur les passagers (APIS)'),
(23, 'en', 'Advance Passenger Information System (APIS) passport or identity card'),
(23, 'fr', 'Carte d''identité ou passeport du Système d''informations préalables sur les passagers (API)'),
(24, 'en', 'Disabled passenger with intellectual or development disability needing assistance'),
(24, 'fr', 'Passager handicapé moteur ou mental nécessitant une aide'),
(25, 'en', 'Electronic payment for ticketless carriers'),
(25, 'fr', 'Paiement ELECTRONIQUE pour transporteurs sans billet'),
(26, 'en', 'Passenger with emotional support/psychiatric assistance or animal in cabin'),
(26, 'fr', 'Passager avec soutien émotionnel/assistance psychiatrique ou animal en cabine'),
(27, 'en', 'Extra seat'),
(27, 'fr', 'Siège supplémentaire'),
(28, 'en', 'Form of ID'),
(28, 'fr', 'Forme de pièce d''identité'),
(29, 'en', 'Fruit platter meal'),
(29, 'fr', 'Plat de fruits'),
(30, 'en', 'Frequent Flyer mileage program redemption'),
(30, 'fr', 'Remboursement du programme de fidélisation'),
(31, 'en', 'Frequent Flyer service request'),
(31, 'fr', 'Demande de service de carte de fidélité'),
(32, 'en', 'Frequent Flyer upgrade and accrual'),
(32, 'fr', 'Mise à niveau de la carte de fidélité et comptabilité d''exercice'),
(33, 'en', 'Frequent Flyer mileage program accrual'),
(33, 'fr', 'Accumulation du programme de kilométrage de la carte de fidélité'),
(34, 'en', 'Fragile baggage'),
(34, 'fr', 'Bagage fragile'),
(35, 'en', 'First available'),
(35, 'fr', 'Premier disponible'),
(36, 'en', 'Gluten intolerant meal'),
(36, 'fr', 'Repas intolérant au gluten'),
(37, 'en', 'Group seat request'),
(37, 'fr', 'Demande de siège groupe'),
(38, 'en', 'Group fare '),
(38, 'fr', 'Tarif de groupe'),
(39, 'en', 'Passengers traveling together using a common identity'),
(39, 'fr', 'Passagers voyageant ensemble en utilisant une identité commune'),
(40, 'en', 'Hindu meal'),
(40, 'fr', 'Repas hindou'),
(41, 'en', 'Infant '),
(41, 'fr', 'Bébé'),
(42, 'en', 'Japanese meal'),
(42, 'fr', 'Repas japonais'),
(43, 'en', 'Kosher meal'),
(43, 'fr', 'Repas casher'),
(44, 'en', 'Languages spoken'),
(44, 'fr', 'Langues parlées'),
(45, 'en', 'Low calorie meal'),
(45, 'fr', 'Repas faible en calories'),
(46, 'en', 'Low fat meal'),
(46, 'fr', 'Repas à faible teneur en matières grasses'),
(47, 'en', 'Low salt meal'),
(47, 'fr', 'Repas à faible teneur en sel'),
(48, 'en', 'Meet and assist'),
(48, 'fr', 'Service d''assistance'),
(49, 'en', 'Medical case'),
(49, 'fr', 'Valise médicale'),
(50, 'en', 'Muslim meal'),
(50, 'fr', 'Repas musulman'),
(51, 'en', 'Name'),
(51, 'fr', 'Nom'),
(52, 'en', 'No fish meal'),
(52, 'fr', 'Repas sans poisson'),
(53, 'en', 'Low lactose meal'),
(53, 'fr', 'Repas à faible teneur en lactose'),
(54, 'en', 'Non smoking aisle seat'),
(54, 'fr', 'Siège couloir non-fumeur'),
(55, 'en', 'Non smoking bulkhead seat'),
(55, 'fr', 'Siège non fumeur à côté d''une cloison'),
(56, 'en', 'Non smoking seat'),
(56, 'fr', 'Siège non fumeur'),
(57, 'en', 'Non smoking window seat'),
(57, 'fr', 'Siège hublot non fumeur'),
(58, 'en', 'Other service not specified by any other SSR code'),
(58, 'fr', 'Autre service non spécifié par un autre code SSR'),
(59, 'en', 'Emergency contact details for passenger'),
(59, 'fr', 'Informations de contact en cas d''urgence pour le passager'),
(60, 'en', 'Animal in cabin'),
(60, 'fr', 'Animal en cabine'),
(61, 'en', 'Passenger in custody, accompanied'),
(61, 'fr', 'Passager en garde à vue, accompagné'),
(62, 'en', 'Passenger in custody, unaccompanied'),
(62, 'fr', 'Passager en garde à vue non accompagné'),
(63, 'en', 'Seat request'),
(63, 'fr', 'Demande de siège'),
(64, 'en', 'Raw vegetarian meal'),
(64, 'fr', 'Repas végétarien cru'),
(65, 'en', 'Pre-reserved seat with boarding pass issued or to be issued'),
(65, 'fr', 'Siège pré-réservé avec carte d''embarquement émise ou à émettre'),
(66, 'en', 'Seaman - ship''s crew'),
(66, 'fr', 'Matelot - Equipage du navire'),
(67, 'en', 'Seafood meal'),
(67, 'fr', 'Repas de poisson'),
(68, 'en', 'Bed/berth in cabin'),
(68, 'fr', 'Lit/couchette en cabine'),
(69, 'en', 'Smoking aisle seat'),
(69, 'fr', 'Siège fumeur côté couloir'),
(70, 'en', 'Smoking bulkhead seat'),
(70, 'fr', 'Siège fumeur, à côté d''une cloison'),
(71, 'en', 'Smoking seat'),
(71, 'fr', 'Siège fumeur'),
(72, 'en', 'Smoking window seat'),
(72, 'fr', 'Siège hublot fumeur'),
(73, 'en', 'Sports equipment'),
(73, 'fr', 'Équipement de sport'),
(74, 'en', 'Special meal'),
(74, 'fr', 'Repas spécial'),
(75, 'en', 'Stretcher passenger'),
(75, 'fr', 'Passager en civière'),
(76, 'en', 'Passenger with service animal in cabin (LH specific)'),
(76, 'fr', 'Passager avec animal d''assistance en cabine (spécifique LH )'),
(77, 'en', 'Ticket number in FA element'),
(77, 'fr', 'Numéro de billet dans l''élément FA'),
(78, 'en', 'Ticket number transmission'),
(78, 'fr', 'Transmission du numéro de billet'),
(79, 'en', 'E-ticket number in FA element'),
(79, 'fr', 'Numéro de billet électronique dans l''élément FA'),
(80, 'en', 'Ticket number in FH element'), 
(80, 'fr', 'Numéro de billet dans l''élément FH'),
(81, 'en', 'Ticketing time limit'),
(81, 'fr', 'Heure limite d''émission de billet'),
(82, 'en', 'Transit or transfer without visa'),
(82, 'fr', 'Transit ou transfert sans visa'),
(83, 'en', 'Unaccompanied minor'), 
(83, 'fr', 'Mineur non accompagné'),
(84, 'en', 'Vegetarian vegan meal'), 
(84, 'fr', 'Repas végétarien végétalien'),
(85, 'en', 'Vegetarian Jain meal'), 
(85, 'fr', 'Repas végétarien Jaïn'),
(86, 'en', 'Vegetarian lacto-ovo meal'), 
(86, 'fr', 'Repas végétarien (lait et oeufs)'),
(87, 'en', 'Vegetarian Oriental meal'), 
(87, 'fr', 'Repas végétarien oriental'),
(88, 'en', 'Wheelchair - dry cell battery'), 
(88, 'fr', 'Fauteuil roulant - pile sèche'),
(89, 'en', 'Wheelchair - wet cell battery'), 
(89, 'fr', 'Fauteuil roulant - pile liquide'),
(90, 'en', 'Wheelchair - all the way to seat'), 
(90, 'fr', 'Fauteuil roulant - jusqu''au siège'),
(91, 'en', 'Wheelchair - for ramp'), 
(91, 'fr', 'Fauteuil roulant - pour rampe'),
(92, 'en', 'Wheelchair - up and down steps'), 
(92, 'fr', 'Fauteuil roulant - pour les escaliers'),
(93, 'en', 'Wheelchair - manual power (US carriers only)'), 
(93, 'fr', 'Fauteuil roulant - alimentation manuelle (transporteurs américains uniquement)'),
(94, 'en', 'Wheelchair - on board'), 
(94, 'fr', 'Fauteuil roulant - à bord'),
(95, 'en', 'Excess baggage'), 
(95, 'fr', 'Excédent de bagages'),
(96, 'en', 'Weapons, firearms or ammunition carried as checked baggage');