-- Définition des CTE avec une seule clause WITH
WITH last_tuc AS (
    -- Cette CTE récupère le dernier émetteur pour chaque document dans la table t_user_copying
    SELECT DISTINCT ON (tuc1.document)  -- Sélection distincte pour chaque document
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
        tp.id AS pnr_id,  -- ID du PNR
        tp."number" AS "Numéro",  -- Numéro du PNR
        tp.system_creation_date AS "Date de création",  -- Date de création du PNR
        tp.status AS "Status",  -- Statut du PNR
        tp."type" AS "Type",  -- Type du PNR
        tp.agency_code AS "Code",  -- Code de l'agence associée au PNR
        tu.username AS "Créateur",  -- Nom d'utilisateur du créateur du PNR
        to2."name" AS "Agence",  -- Nom de l'agence associée au PNR
        -- Concaténation du nom et du prénom du passager pour obtenir le nom complet
        COALESCE(tp2."name" || ' ' || tp2.surname, '') AS "Passagers",
        -- Ajout de l'émetteur à partir des CTE last_tuc, latest_ticket_emitter ou latest_other_fee_emitter
        COALESCE(
        	last_tuc."Emetteur",
            latest_ticket_emitter."Emetteur",
            latest_other_fee_emitter."Emetteur"
        ) AS "Emetteur",
        -- Attribue un numéro de ligne à chaque passager pour chaque PNR, 
        -- partitionné par l'ID du PNR et ordonné par le nom du passager
        ROW_NUMBER() OVER (PARTITION BY tp.id ORDER BY tp2."name") AS rn
    FROM
        t_pnr tp  -- Table principale des PNR
    -- Jointure avec t_pnr_passengers pour obtenir les passagers associés à chaque PNR
    LEFT JOIN
        t_pnr_passengers tpp ON tp.id = tpp.pnr_id
    -- Jointure avec t_passengers pour obtenir les détails des passagers
    LEFT JOIN
        t_passengers tp2 ON tp2.id = tpp.passenger_id
    -- Jointure avec t_user pour obtenir les informations sur l'utilisateur créateur du PNR
    LEFT JOIN
        t_user tu ON tp.agent_id = tu.id
    -- Jointure avec t_office pour obtenir les informations sur l'agence
    LEFT JOIN
        t_office to2 ON tp.agency_code = to2.code
    -- Jointure avec last_tuc pour obtenir l'émetteur à partir de la CTE last_tuc
    LEFT JOIN
        last_tuc ON tp."number" = last_tuc.document
    -- Jointure avec latest_ticket_emitter pour obtenir l'émetteur le plus récent des tickets
    LEFT JOIN
        latest_ticket_emitter ON tp.id = latest_ticket_emitter.pnr_id AND latest_ticket_emitter.rn = 1
    -- Jointure avec latest_other_fee_emitter pour obtenir l'émetteur le plus récent des frais supplémentaires
    LEFT JOIN
        latest_other_fee_emitter ON tp.id = latest_other_fee_emitter.pnr_id AND latest_other_fee_emitter.rn = 1
    -- Filtrage des PNR créés après le 1er janvier 2023
    WHERE
        tp.system_creation_date >= '2023-01-01'
)
-- Sélection finale des colonnes de la CTE PNR_PASSENGERS
SELECT
    "Numéro",  -- Numéro du PNR
    "Passagers",  -- Nom complet du passager
    "Date de création",  -- Date de création du PNR
    "Status",  -- Statut du PNR
    "Type",  -- Type du PNR
    "Code",  -- Code de l'agence associée au PNR
    "Créateur",  -- Nom d'utilisateur du créateur du PNR
    "Emetteur",  -- Nom de l'émetteur (soit de t_user_copying, soit de t_ticket, soit de t_other_fee)
    "Agence"  -- Nom de l'agence associée au PNR
FROM
    PNR_PASSENGERS  -- Utilisation de la CTE définie précédemment
-- Filtrage pour ne sélectionner que le premier passager (ou la première ligne) pour chaque PNR
WHERE
    rn = 1;
