--function to get the destination country of a ticket
create or replace function f_getDestinationCountry(ticket integer)
returns character varying(2)
as 
$body$
declare
	array_values character varying[];
begin
	 select array_agg(countrydest) into array_values from t_airsegments where ticketid = ticketid;
	 return array_values[1];
end;
$body$
language plpgsql;

--function to get the flight type : Domestic
create or replace function f_findflightype(ticket integer)
returns integer
as $body$
declare
	flight_type_id integer;
	destination_country character varying(2);
	result integer;
begin
	destination_country := f_getDestinationCountry(ticket);
	select coalesce((select flighttypeid from t_countryflighttype where countrycode = 'R'), 0) into flight_type_id;
	case
		when flight_type_id = 0 then result :=  2;
		else result := flight_type_id;
	end case;
	return result;
end;
$body$
language plpgsql; 

--function to get the flight class
create or replace function f_findflightclass(ticket integer)
returns integer
as $body$
declare
	gds_provider character varying(30); 
	flight_class character varying(2); --letter class Y, Z.....
	flight_class_type character varying(50); --Business,.... 
 	flight_segment character varying(100); --Original path e.g: TNR/CDG
 	flight_segment_split character varying[]; --To put the splitted path array
 	flight_path character varying(60); --simple or back-and-forth
 	arrayLength integer; --to put the length of flight_segment_split array
 	result integer;
begin
	select type into gds_provider from t_pnr where id = (select pnrid from t_ticket where id = ticket);
	select flightclass into flight_class from t_ticket where id = ticket;
	--select path into flight_segment from t_ticket where id = ticket;
	--select string_to_array(flight_segment, '/') into flight_segment_split;
	select array_cat(array_agg(codeorg), array_agg(codedest)) into flight_segment_split from t_pnrairsegments where pnrid = (select pnrid from t_ticket where id = ticket);
	--check flight_path
 	arrayLength := array_length(flight_segment_split, 1);
 	case
 		when flight_segment_split[1] = flight_segment_split[arrayLength] then flight_path = 'Back-and-forth';
 		else flight_path = 'Simple';
 	end case;
 	--find flight class
 	select type into flight_class_type from t_classsign where gdsprovider = gds_provider and flight_class = any(sign);
 	case
 		when (flight_class_type = 'Economic' or flight_class_type = 'Economic Premium') then
 			case
 				when flight_path = 'Back-and-forth' then select id into result from t_flightclass where flightclass = 'Back-and-forth economic class';
 				when flight_path = 'Simple' then select id into result from t_flightclass where flightclass = 'Simple economic class';
 				-- else 
 			end case;  
 		when (flight_class_type = 'Business') then
 			case
 				when flight_path = 'Back-and-forth' then select id into result from t_flightclass where flightclass = 'Back-and-forth business class';
 				when flight_path = 'Simple' then select id into result from t_flightclass where flightclass = 'Simple business class';
 			end case;  
 	end case;
 	return result;
end;
$body$
language plpgsql; 

--function to automatically find and insert service fees based on ticket
create or replace function f_findServiceFees()
returns trigger
as
$body$
declare
 	flight_type_id integer;
 	flight_class_id integer;
 	pnr_id integer;
 	value double precision;
 	ticket_status character varying(50);
begin
 	flight_type_id := f_findflightype(new.id);
 	flight_class_id := f_findflightclass(new.id);
 	select price into value from t_servicefees where flighttypeid = flight_type_id and flightclassid = flight_class_id;
 	select pnrid into pnr_id from t_ticket where id = new.id;
 	select status into ticket_status from t_ticket where id = new.id;
 	case
 		when ticket_status = 'issued' or ticket_status = 'refund' or ticket_status = 'reissued' then
 			insert into t_fee(pnrid, ticketid, type, designation, cost, tax, total) values (pnr_id, new.id, 'SERVICE FEES', ' ', value, 0, value);
 		when ticket_status = 'void' then
 			return new;
 	end case;
 	return new;
end;
$body$
language plpgsql;
 
create trigger t_result
	after insert on t_ticket
	for each row
	execute procedure f_findServiceFees();


--Doc
--Split: select string_to_array('TNR/CDG/', '/');
--Result to array: select array_agg(codeorg) from t_pnrairsegments where pnrid = 1401;
--Union of two arrays: select array_cat(array_agg(codeorg), array_agg(codedest)) from t_pnrairsegments where pnrid = 1401;