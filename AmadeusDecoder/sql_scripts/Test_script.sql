-- find the minimum cancellation date of segments or ssrs for one PNR
select
	min(t_confirmation_deadline.doc_date)
from
	t_confirmation_deadline, t_pnr, t_pnrairsegments, t_ssr_base
where
	t_pnrairsegments.pnr_id = t_pnr.id
	and
	t_ssr_base.pnr_id = t_pnr.id
	and(
	t_confirmation_deadline.segment_id = t_pnrairsegments.id
	or
	t_confirmation_deadline.ssr_id = t_ssr_base.id)
	and
	t_confirmation_deadline.type = 'OPC'
	and
	t_pnr.id = 40;

-- find related pnr from passengers and air segments
(((
SELECT 
	"t_pnr"."id", "t_pnr"."agent_id", "t_pnr"."agency_code", "t_pnr"."currency_code", "t_pnr"."state", "t_pnr"."number", "t_pnr"."gds_creation_date", "t_pnr"."system_creation_date", "t_pnr"."status", "t_pnr"."status_value", "t_pnr"."exportdate", "t_pnr"."type", "t_pnr"."validationstatus", "t_pnr"."dateexport", "t_pnr"."changedate", "t_pnr"."lasttransactiondate", "t_pnr"."otherinformations", "t_pnr"."ssr", "t_pnr"."openingstatus", "t_pnr"."is_splitted", "t_pnr"."is_duplicated", "t_pnr"."is_parent", "t_pnr"."is_child", "t_pnr"."is_read", "t_pnr"."parent_pnr_id" 
FROM 
	"t_pnr" 
INNER JOIN 
	"t_pnrairsegments" 
	ON (
	"t_pnr"."id" = "t_pnrairsegments"."pnr_id") 
	WHERE 
	("t_pnrairsegments"."codedest_id" = 'CDG' 
	AND 
	"t_pnrairsegments"."codeorg_id" = 'DZA' 
	AND 
	"t_pnrairsegments"."flightno" = '977' 
	AND "t_pnrairsegments"."servicecarrier_id" = 1190
	)
) 
INTERSECT 
(
SELECT
	 "t_pnr"."id", "t_pnr"."agent_id", "t_pnr"."agency_code", "t_pnr"."currency_code", "t_pnr"."state", "t_pnr"."number", "t_pnr"."gds_creation_date", "t_pnr"."system_creation_date", "t_pnr"."status", "t_pnr"."status_value", "t_pnr"."exportdate", "t_pnr"."type", "t_pnr"."validationstatus", "t_pnr"."dateexport", "t_pnr"."changedate", "t_pnr"."lasttransactiondate", "t_pnr"."otherinformations", "t_pnr"."ssr", "t_pnr"."openingstatus", "t_pnr"."is_splitted", "t_pnr"."is_duplicated", "t_pnr"."is_parent", "t_pnr"."is_child", "t_pnr"."is_read", "t_pnr"."parent_pnr_id" 
FROM 
	"t_pnr" 
INNER JOIN 
	"t_pnrairsegments" 
	ON (
	"t_pnr"."id" = "t_pnrairsegments"."pnr_id") 
	WHERE (
	"t_pnrairsegments"."codedest_id" = 'RUN' 
	AND 
	"t_pnrairsegments"."codeorg_id" = 'CDG' 
	AND 
	"t_pnrairsegments"."flightno" = '972' 
	AND 
	"t_pnrairsegments"."servicecarrier_id" = 1190)
)) 
INTERSECT (
SELECT 
	"t_pnr"."id", "t_pnr"."agent_id", "t_pnr"."agency_code", "t_pnr"."currency_code", "t_pnr"."state", "t_pnr"."number", "t_pnr"."gds_creation_date", "t_pnr"."system_creation_date", "t_pnr"."status", "t_pnr"."status_value", "t_pnr"."exportdate", "t_pnr"."type", "t_pnr"."validationstatus", "t_pnr"."dateexport", "t_pnr"."changedate", "t_pnr"."lasttransactiondate", "t_pnr"."otherinformations", "t_pnr"."ssr", "t_pnr"."openingstatus", "t_pnr"."is_splitted", "t_pnr"."is_duplicated", "t_pnr"."is_parent", "t_pnr"."is_child", "t_pnr"."is_read", "t_pnr"."parent_pnr_id" 
FROM 
	"t_pnr" 
INNER JOIN 
	"t_pnrairsegments" 
	ON (
	"t_pnr"."id" = "t_pnrairsegments"."pnr_id") 
	WHERE (
	"t_pnrairsegments"."codedest_id" = 'DZA' 
	AND 
	"t_pnrairsegments"."codeorg_id" = 'RUN' 
	AND 
	"t_pnrairsegments"."flightno" = '276' 
	AND 
	"t_pnrairsegments"."servicecarrier_id" = 1190)
)) 
INTERSECT (
SELECT 
	"t_pnr"."id", "t_pnr"."agent_id", "t_pnr"."agency_code", "t_pnr"."currency_code", "t_pnr"."state", "t_pnr"."number", "t_pnr"."gds_creation_date", "t_pnr"."system_creation_date", "t_pnr"."status", "t_pnr"."status_value", "t_pnr"."exportdate", "t_pnr"."type", "t_pnr"."validationstatus", "t_pnr"."dateexport", "t_pnr"."changedate", "t_pnr"."lasttransactiondate", "t_pnr"."otherinformations", "t_pnr"."ssr", "t_pnr"."openingstatus", "t_pnr"."is_splitted", "t_pnr"."is_duplicated", "t_pnr"."is_parent", "t_pnr"."is_child", "t_pnr"."is_read", "t_pnr"."parent_pnr_id" 
FROM 
	"t_pnr" 
INNER JOIN 
	"t_pnr_passengers" 
	ON (
	"t_pnr"."id" = "t_pnr_passengers"."pnr_id") 
INNER JOIN 
	"t_passengers" 
	ON (
	"t_pnr_passengers"."passenger_id" = "t_passengers"."id") 
	WHERE (
	"t_passengers"."designation" = 'MR' 
	AND 
	"t_passengers"."name" = 'HANAFFI' 
	AND 
	"t_passengers"."surname" = 'MARIB' 
))
