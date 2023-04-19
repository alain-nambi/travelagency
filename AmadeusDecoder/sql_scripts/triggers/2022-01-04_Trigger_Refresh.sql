CREATE OR REPLACE FUNCTION refresh_total()
  RETURNS void AS
$BODY$
DECLARE
  r record;
  result double precision;
BEGIN
  -- r is a structure that contains an element for each column in the select list
  FOR r IN select * from t_ticket
  LOOP
    result := r.total;
	
    update t_ticket 
      set total = result 
    WHERE id = r.id; -- note the where condition that uses the value from the record variable
  END LOOP;
END
$BODY$
LANGUAGE plpgsql;