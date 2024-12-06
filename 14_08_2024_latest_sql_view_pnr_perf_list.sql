-- Création de la vue SQL
CREATE VIEW optimised_pnr_list AS
WITH 
    last_tuc AS (
        -- Récupère le dernier émetteur pour chaque document dans t_user_copying
        SELECT DISTINCT ON (tuc1.document) 
            tuc1.document,
            tuc1.user_id_id,
            tu2.username AS "Emetteur"
        FROM
            t_user_copying tuc1
        LEFT JOIN
            t_user tu2 ON tuc1.user_id_id = tu2.id
        ORDER BY
            tuc1.document, tuc1.id DESC
    ),
    latest_ticket_emitter AS (
        -- Récupère le dernier émetteur pour chaque PNR dans t_ticket
        SELECT
            tt.pnr_id,
            tt.emitter_id,
            ROW_NUMBER() OVER (PARTITION BY tt.pnr_id ORDER BY tt.id DESC) AS rn,
            tu.username AS "Emetteur"
        FROM
            t_ticket tt
        LEFT JOIN
            t_user tu ON tt.emitter_id = tu.id
        WHERE
            tt.ticket_status = 1 OR tt.is_invoiced = TRUE
    ),
    latest_other_fee_emitter AS (
        -- Récupère le dernier émetteur pour chaque PNR dans t_other_fee
        SELECT
            tof.pnr_id,
            tof.emitter_id,
            ROW_NUMBER() OVER (PARTITION BY tof.pnr_id ORDER BY tof.id DESC) AS rn,
            tu.username AS "Emetteur"
        FROM
            t_other_fee tof
        LEFT JOIN
            t_user tu ON tof.emitter_id = tu.id
        WHERE
            tof.other_fee_status = 1 OR tof.is_invoiced = TRUE
    ),
    max_ticket_issuing_date AS (
        -- Récupère la date d'émission maximale pour chaque PNR dans t_ticket
        SELECT
            tt.pnr_id,
            MAX(tt.issuing_date) AS max_issuing_date
        FROM
            t_ticket tt
        WHERE
            tt.ticket_status != 0
        GROUP BY
            tt.pnr_id
    ),
    max_other_fee_creation_date AS (
        -- Récupère la date de création maximale pour chaque PNR dans t_other_fee
        SELECT
            tof.pnr_id,
            MAX(tof.creation_date) AS max_creation_date
        FROM
            t_other_fee tof
        WHERE
            tof.other_fee_status != 0
        GROUP BY
            tof.pnr_id
    ),
    pnr_comment_state AS (
        -- Calcule l'état des commentaires pour chaque PNR
        SELECT
            tp.id AS pnr_id,
            CASE 
                WHEN COUNT(t_comment.id) = 0 THEN -1
                WHEN SUM(CASE WHEN t_comment.state = FALSE THEN 1 ELSE 0 END) > 0 THEN 0
                ELSE 1
            END AS pnr_comment_state
        FROM
            t_pnr tp
        LEFT JOIN
            t_comment ON tp.id = t_comment.pnr_id_id
        GROUP BY
            tp.id
    ),
    pnr_min_doc_state AS (
        -- Calcule la date minimum des documents de confirmation pour chaque PNR
        SELECT 
            tp.pnr_id,
            MIN(cd.doc_date) AS min_doc_date
        FROM 
            t_confirmation_deadline cd
        LEFT JOIN
            t_pnrairsegments tp ON cd.segment_id = tp.id
        WHERE 
            cd.type = 'OPC'
        GROUP BY 
            tp.pnr_id
    ),
    PNR_PASSENGERS AS (
        -- Construction de la vue finale en combinant les informations sur les PNR, les passagers, et d'autres détails
        SELECT
            tp.id AS "pnr_id",
            tp."number" AS "number",
            tp.system_creation_date AS "date_of_creation",
            tp.status AS "status",
            tp."type" AS "type",
            tu.username AS "creator",
            to2."name" AS "agency_office_name",
            to2."code" AS "agency_office_code",
            tp.is_invoiced AS "is_invoiced",
            tp.is_read AS "is_read",
            tp.status_value AS "status_value",
            tp.state AS "state",
            tp.agency_name AS "agency_name",
            pnr_comment_state AS "pnr_comment_state",
            pnr_min_doc_state.min_doc_date AS "pnr_min_doc_state",
            CASE 
                WHEN tp2.surname IS NULL THEN tp2."name"
                ELSE tp2."name" || ' ' || tp2.surname
            END AS "passengers",
            COALESCE(
                last_tuc."Emetteur",
                latest_ticket_emitter."Emetteur",
                latest_other_fee_emitter."Emetteur"
            ) AS "emitter",
            -- Ajouter la logique pour obtenir la date maximale d'émission
            COALESCE(
                max_ticket_issuing_date.max_issuing_date,
                max_other_fee_creation_date.max_creation_date
            ) AS "max_issuing_date",
            ROW_NUMBER() OVER (PARTITION BY tp.id ORDER BY tp2."name") AS rn
        FROM
            t_pnr tp
        LEFT JOIN
            t_pnr_passengers tpp ON tp.id = tpp.pnr_id
        LEFT JOIN
            t_passengers tp2 ON tp2.id = tpp.passenger_id
        LEFT JOIN
            t_user tu ON tp.agent_id = tu.id
        LEFT JOIN
            t_office to2 ON tp.agency_code = to2.code
        LEFT JOIN
            last_tuc ON tp."number" = last_tuc.document
        LEFT JOIN
            latest_ticket_emitter ON tp.id = latest_ticket_emitter.pnr_id AND latest_ticket_emitter.rn = 1
        LEFT JOIN
            latest_other_fee_emitter ON tp.id = latest_other_fee_emitter.pnr_id AND latest_other_fee_emitter.rn = 1
        LEFT JOIN
            pnr_comment_state ON tp.id = pnr_comment_state.pnr_id
        LEFT JOIN
            pnr_min_doc_state ON tp.id = pnr_min_doc_state.pnr_id
        LEFT JOIN
            max_ticket_issuing_date ON tp.id = max_ticket_issuing_date.pnr_id
        LEFT JOIN
            max_other_fee_creation_date ON tp.id = max_other_fee_creation_date.pnr_id
        WHERE
            tp.system_creation_date >= '2023-01-01'
    ),
    clients AS (
        -- Récupère le nom du client pour chaque PNR
        SELECT
            tpi.pnr_id,
            tc.intitule AS "client",
            ROW_NUMBER() OVER (PARTITION BY tpi.pnr_id ORDER BY tpi.id) AS rn
        FROM
            t_passenger_invoice tpi
        LEFT JOIN
            t_client tc ON tpi.client_id = tc.id
    )
SELECT
    PNR_PASSENGERS."pnr_id" AS "id",
    PNR_PASSENGERS."number",
    PNR_PASSENGERS."passengers",
    PNR_PASSENGERS."date_of_creation",
    PNR_PASSENGERS."status",
    PNR_PASSENGERS."type",
    PNR_PASSENGERS."creator",
    PNR_PASSENGERS."emitter",
    PNR_PASSENGERS."max_issuing_date", -- Ajouter la colonne pour la date d'émission maximale
    PNR_PASSENGERS."agency_office_code",
    PNR_PASSENGERS."agency_office_name",
    PNR_PASSENGERS."agency_name",
    PNR_PASSENGERS."is_invoiced",
    PNR_PASSENGERS."is_read",
    PNR_PASSENGERS."status_value",
    PNR_PASSENGERS."state",
    PNR_PASSENGERS.pnr_comment_state,
    PNR_PASSENGERS.pnr_min_doc_state,
    clients."client"
FROM
    PNR_PASSENGERS
LEFT JOIN
    clients ON PNR_PASSENGERS.pnr_id = clients.pnr_id AND clients.rn = 1
WHERE
    PNR_PASSENGERS.rn = 1;
