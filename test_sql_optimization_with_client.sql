-- Création de la vue SQL
CREATE VIEW optimised_pnr_list AS
WITH 
    last_tuc AS (
        -- Cette CTE récupère le dernier émetteur pour chaque document dans la table t_user_copying
        SELECT DISTINCT ON (tuc1.document) 
            tuc1.document,  -- Identifiant du document
            tuc1.user_id_id,  -- ID de l'utilisateur (émetteur)
            tu2.username AS "Emetteur"  -- Nom d'utilisateur de l'émetteur
        FROM
            t_user_copying tuc1
        LEFT JOIN
            t_user tu2 ON tuc1.user_id_id = tu2.id  -- Jointure pour obtenir le nom de l'émetteur
        ORDER BY
            tuc1.document, tuc1.id DESC  -- Trier pour obtenir la dernière entrée pour chaque document
    ),
    latest_ticket_emitter AS (
        -- Cette CTE récupère le dernier émetteur pour chaque PNR dans la table t_ticket
        SELECT
            tt.pnr_id,  -- ID du PNR
            tt.emitter_id,  -- ID de l'émetteur
            ROW_NUMBER() OVER (PARTITION BY tt.pnr_id ORDER BY tt.id DESC) AS rn,  -- Numéro de ligne pour chaque PNR
            tu.username AS "Emetteur"  -- Nom d'utilisateur de l'émetteur
        FROM
            t_ticket tt
        LEFT JOIN
            t_user tu ON tt.emitter_id = tu.id  -- Jointure pour obtenir le nom de l'émetteur
        WHERE
            tt.ticket_status = 1 OR tt.is_invoiced = TRUE  -- Filtrage des tickets actifs ou facturés
    ),
    latest_other_fee_emitter AS (
        -- Cette CTE récupère le dernier émetteur pour chaque PNR dans la table t_other_fee
        SELECT
            tof.pnr_id,  -- ID du PNR
            tof.emitter_id,  -- ID de l'émetteur
            ROW_NUMBER() OVER (PARTITION BY tof.pnr_id ORDER BY tof.id DESC) AS rn,  -- Numéro de ligne pour chaque PNR
            tu.username AS "Emetteur"  -- Nom d'utilisateur de l'émetteur
        FROM
            t_other_fee tof
        LEFT JOIN
            t_user tu ON tof.emitter_id = tu.id  -- Jointure pour obtenir le nom de l'émetteur
        WHERE
            tof.other_fee_status = 1 OR tof.is_invoiced = TRUE  -- Filtrage des frais supplémentaires actifs ou facturés
    ),
    PNR_PASSENGERS AS (
        -- Cette CTE construit la vue finale en combinant les informations sur les PNR, les passagers, et d'autres détails
        SELECT
            tp.id AS "pnr_id",  -- ID du PNR
            tp."number" AS "number",  -- Numéro du PNR
            tp.system_creation_date AS "date_of_creation",  -- Date de création du PNR
            tp.status AS "status",  -- Statut du PNR
            tp."type" AS "type",  -- Type du PNR
            tu.username AS "creator",  -- Nom d'utilisateur du créateur du PNR
            to2."name" AS "agency_office_name",  -- Nom de l'agence associée au PNR
            to2."code" as "agency_office_code",
            tp.is_invoiced as "is_invoiced",
            tp.is_read as "is_read",
            tp.status_value as "status_value",
            tp.state as "state",
            tp.agency_name as "agency_name",
            
            -- COALESCE(tp2."name" || ' ' || tp2.surname, '') AS "passengers",  
            CASE 
		        WHEN tp2.surname IS NULL THEN tp2."name"
		        ELSE tp2."name" || ' ' || tp2.surname
		    END AS "passengers", -- Nom complet du passager

            
            
            COALESCE(
                last_tuc."Emetteur",
                latest_ticket_emitter."Emetteur",
                latest_other_fee_emitter."Emetteur"
            ) AS "emitter",  -- Ajout de l'émetteur à partir des CTE
            ROW_NUMBER() OVER (PARTITION BY tp.id ORDER BY tp2."name") AS rn  -- Numéro de ligne pour chaque passager pour chaque PNR
        FROM
            t_pnr tp  -- Table principale des PNR
        LEFT JOIN
            t_pnr_passengers tpp ON tp.id = tpp.pnr_id  -- Jointure avec t_pnr_passengers pour obtenir les passagers associés à chaque PNR
        LEFT JOIN
            t_passengers tp2 ON tp2.id = tpp.passenger_id  -- Jointure avec t_passengers pour obtenir les détails des passagers
        LEFT JOIN
            t_user tu ON tp.agent_id = tu.id  -- Jointure avec t_user pour obtenir les informations sur l'utilisateur créateur du PNR
        LEFT JOIN
            t_office to2 ON tp.agency_code = to2.code  -- Jointure avec t_office pour obtenir les informations sur l'agence
        LEFT JOIN
            last_tuc ON tp."number" = last_tuc.document  -- Jointure avec last_tuc pour obtenir l'émetteur à partir de la CTE last_tuc
        LEFT JOIN
            latest_ticket_emitter ON tp.id = latest_ticket_emitter.pnr_id AND latest_ticket_emitter.rn = 1  -- Jointure avec latest_ticket_emitter pour obtenir l'émetteur le plus récent des tickets
        LEFT JOIN
            latest_other_fee_emitter ON tp.id = latest_other_fee_emitter.pnr_id AND latest_other_fee_emitter.rn = 1  -- Jointure avec latest_other_fee_emitter pour obtenir l'émetteur le plus récent des frais supplémentaires
        WHERE
            tp.system_creation_date >= '2023-01-01'  -- Filtrage des PNR créés après le 1er janvier 2023
    ),
    clients AS (
        SELECT
            tpi.pnr_id,
            tc.intitule AS "client",
            ROW_NUMBER() OVER (PARTITION BY tpi.pnr_id ORDER BY tpi.id) AS rn
        FROM
            t_passenger_invoice tpi
        LEFT JOIN
            t_client tc ON tpi.client_id = tc.id
    )
-- Sélection finale des colonnes de la CTE PNR_PASSENGERS
SELECT
    PNR_PASSENGERS."pnr_id" AS "id",  -- Renommage pour éviter les ambiguïtés
    PNR_PASSENGERS."number",  -- Numéro du PNR
    PNR_PASSENGERS."passengers",  -- Nom complet du passager
    PNR_PASSENGERS."date_of_creation",  -- Date de création du PNR
    PNR_PASSENGERS."status",  -- Statut du PNR
    PNR_PASSENGERS."type",  -- Type du PNR
    PNR_PASSENGERS."creator",  -- Nom d'utilisateur du créateur du PNR
    PNR_PASSENGERS."emitter",  -- Nom de l'émetteur (soit de t_user_copying, soit de t_ticket, soit de t_other_fee)
    PNR_PASSENGERS."agency_office_code",  -- Code de l'agence associée au PNR
    PNR_PASSENGERS."agency_office_name",  -- Nom de l'agence associée au PNR
    PNR_PASSENGERS."agency_name",  -- Nom de l'agence
    PNR_PASSENGERS."is_invoiced",
    PNR_PASSENGERS."is_read",
    PNR_PASSENGERS."status_value",
    PNR_PASSENGERS."state",
    clients."client"  -- Nom du client
FROM
    PNR_PASSENGERS  -- Utilisation de la CTE définie précédemment
LEFT JOIN
    clients ON PNR_PASSENGERS.pnr_id = clients.pnr_id AND clients.rn = 1  -- Jointure avec la CTE clients pour obtenir le nom du client unique par PNR
WHERE
    PNR_PASSENGERS.rn = 1;  -- Filtrage pour ne sélectionner que le premier passager (ou la première ligne) pour chaque PNR
