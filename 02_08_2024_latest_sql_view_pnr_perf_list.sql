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
    pnr_comment_state AS (
        -- Cette CTE calcule l'état des commentaires pour chaque PNR
        SELECT
            tp.id AS pnr_id,  -- ID du PNR
            CASE 
                WHEN COUNT(t_comment.id) = 0 THEN -1  -- Aucun commentaire
                WHEN SUM(CASE WHEN t_comment.state = FALSE THEN 1 ELSE 0 END) > 0 THEN 0  -- Au moins un commentaire non validé
                ELSE 1  -- Tous les commentaires sont validés
            END AS pnr_comment_state
        FROM
            t_pnr tp  -- Table des PNR
        LEFT JOIN
            t_comment ON tp.id = t_comment.pnr_id_id  -- Jointure avec la table des commentaires
        GROUP BY
            tp.id  -- Grouper par ID de PNR
    ),
    pnr_min_doc_state AS (
        -- Cette CTE calcule la date minimum des documents de confirmation pour chaque PNR
        SELECT 
            tp.pnr_id,  -- ID du PNR
            MIN(cd.doc_date) AS min_doc_date  -- Date minimum des documents
        FROM 
            t_confirmation_deadline cd  -- Table des échéances de confirmation
        LEFT JOIN
            t_pnrairsegments tp ON cd.segment_id = tp.id  -- Jointure avec la table des segments de PNR
        WHERE 
            cd.type = 'OPC'  -- Filtrer par type de document
        GROUP BY 
            tp.pnr_id  -- Grouper par ID de PNR
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
            to2."code" AS "agency_office_code",  -- Code de l'agence associée au PNR
            tp.is_invoiced AS "is_invoiced",  -- Indique si le PNR est facturé
            tp.is_read AS "is_read",  -- Indique si le PNR est lu
            tp.status_value AS "status_value",  -- Valeur du statut du PNR
            tp.state AS "state",  -- État du PNR
            tp.agency_name AS "agency_name",  -- Nom de l'agence
            pnr_comment_state AS "pnr_comment_state",  -- État des commentaires du PNR
            pnr_min_doc_state.min_doc_date as "pnr_min_doc_state",  -- Date minimum des documents du PNR
            CASE 
                WHEN tp2.surname IS NULL THEN tp2."name"  -- Si pas de nom de famille, utiliser le prénom
                ELSE tp2."name" || ' ' || tp2.surname  -- Sinon, utiliser le prénom et le nom de famille
            END AS "passengers", -- Nom complet du passager
            COALESCE(
                last_tuc."Emetteur",  -- Émetteur de la dernière copie utilisateur
                latest_ticket_emitter."Emetteur",  -- Émetteur du dernier ticket
                latest_other_fee_emitter."Emetteur"  -- Émetteur du dernier frais supplémentaire
            ) AS "emitter",  -- Nom de l'émetteur à partir des différentes sources
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
        LEFT JOIN
            pnr_comment_state ON tp.id = pnr_comment_state.pnr_id  -- Jointure avec pnr_comment_state pour obtenir l'état des commentaires
        LEFT JOIN
            pnr_min_doc_state ON tp.id = pnr_min_doc_state.pnr_id  -- Jointure avec pnr_min_doc_state pour obtenir la date minimum des documents
        WHERE
            tp.system_creation_date >= '2023-01-01'  -- Filtrage des PNR créés après le 1er janvier 2023
    ),
    clients AS (
        -- Cette CTE récupère le nom du client pour chaque PNR
        SELECT
            tpi.pnr_id,  -- ID du PNR
            tc.intitule AS "client",  -- Nom du client
            ROW_NUMBER() OVER (PARTITION BY tpi.pnr_id ORDER BY tpi.id) AS rn  -- Numéro de ligne pour chaque client pour chaque PNR
        FROM
            t_passenger_invoice tpi  -- Table des factures passagers
        LEFT JOIN
            t_client tc ON tpi.client_id = tc.id  -- Jointure avec la table des clients
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
    PNR_PASSENGERS."is_invoiced",  -- Indique si le PNR est facturé
    PNR_PASSENGERS."is_read",  -- Indique si le PNR est lu
    PNR_PASSENGERS."status_value",  -- Valeur du statut du PNR
    PNR_PASSENGERS."state",  -- État du PNR
    PNR_PASSENGERS.pnr_comment_state,  -- État des commentaires pour chaque PNR
    PNR_PASSENGERS.pnr_min_doc_state,  -- Date minimum des documents pour chaque PNR
    clients."client"  -- Nom du client
FROM
    PNR_PASSENGERS  -- Utilisation de la CTE définie précédemment
LEFT JOIN
    clients ON PNR_PASSENGERS.pnr_id = clients.pnr_id AND clients.rn = 1  -- Jointure avec la CTE clients pour obtenir le nom du client unique par PNR
WHERE
    PNR_PASSENGERS.rn = 1;  -- Filtrage pour ne sélectionner que le premier passager (ou la première ligne) pour chaque PNR
