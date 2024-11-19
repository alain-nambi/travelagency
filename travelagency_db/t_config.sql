INSERT INTO t_config (name,to_be_applied_on,value_name) VALUES
	 ('Company Information','Global','Name'),
	 ('Company Information','Global','Currency name'),
	 ('Company Information','Global','Currency code'),
	 ('Company Information','Global','Language code'),
	 ('Company Information','Global','Regional country'),
	 ('EMD Parser Tools','Global','Airport agency code'),
	 ('EMD Parser Tools','Global','Special EMD description'),
	 ('EMD Parser Tools','Global','Not feed'),
	 ('EMD Parser Tools','Global','EMD identifier'),
	 ('EMD Parser Tools','Global','PNR number identifier');
INSERT INTO t_config (name,to_be_applied_on,value_name) VALUES
	 ('EMD Parser Tools','Global','PNR type'),
	 ('EMD Parser Tools','Global','EMD statuses'),
	 ('EMD Parser Tools','Global','EMD description identifier'),
	 ('EMD Parser Tools','Global','EMD issuing date identifier'),
	 ('EMD Parser Tools','Global','EMD payment method identifier'),
	 ('EMD Parser Tools','Global','NO ADC identifier'),
	 ('EMD Parser Tools','Global','Cost modification identifier'),
	 ('EMD Parser Tools','Global','Cost detail identifier'),
	 ('Email Source','Global','Email PNR'),
	 ('Email Source','Global','Email PNR');
INSERT INTO t_config (name,to_be_applied_on,value_name) VALUES
	 ('Email Source','Global','Email sending error notification recipients'),
	 ('Email Source','Global','Email sending error notification'),
	 ('Email Source','Global','Anomaly email sender'),
	 ('Email Source','Global','PNR not fetched notification sender'),
	 ('Email Source','Global','Fee request sender');
INSERT INTO t_config (name,to_be_applied_on,value_name) VALUES
	 ('Email Source','Global','Fee request recipient'),
	 ('Email Source','Global','PNR parsing error notification sender'),
	 ('Email Source','Global','PNR parsing error notification recipients'),
	 ('Ticket Parser Tools','Ticket','Ticket identifier'),
	 ('Ticket Parser Tools','Ticket','Related PNR number identifier'),
	 ('Ticket Parser Tools','Ticket','Ticket issuing date identifier'),
	 ('Ticket Parser Tools','Ticket','All possible ticket statuses');
INSERT INTO t_config (name,to_be_applied_on,value_name) VALUES
	 ('Ticket Parser Tools','Ticket','IT fare identifier'),
	 ('Ticket Parser Tools','Ticket','NO ADC identifier'),
	 ('Ticket Parser Tools','Ticket','Cost modification identifier'),
	 ('Ticket Parser Tools','Ticket','Prime ticket identifier'),
	 ('Ticket Parser Tools','Ticket','Invol remote identifier'),
	 ('Ticket Parser Tools','Ticket','Credit note ticket identifier'),
	 ('Ticket Parser Tools','Ticket','GP ticket identifier'),
	 ('Ticket Parser Tools','Ticket','Cost detail identifier'),
	 ('Zenith Parser Tools','Zenith','EMD cost start'),
	 ('Zenith Parser Tools','Zenith','Main pnr start identifier');
INSERT INTO t_config (name,to_be_applied_on,value_name) VALUES
	 ('Zenith Parser Tools','Zenith','Passport identifier'),
	 ('Zenith Parser Tools','Zenith','Passenger identifier'),
	 ('Zenith Parser Tools','Zenith','Payment receipt identifier'),
	 ('Report Email','Fee','Fee history report local recipients'),
	 ('Report Email','Fee','Fee history report local recipients'),
	 ('Report Email','Fee','Fee history report customer recipients'),
	 ('Report Email','Fee','Fee history report customer recipients'),
	 ('Fee Request Tools','Fee','Fee decrease request response sender'),
	 ('Fee Request Tools','Fee','Fee request request response recipient'),
	 ('Saving File Tools','Global','File protocol');
INSERT INTO t_config (name,to_be_applied_on,value_name) VALUES
	 ('Fee Request Tools','Fee','Fee request response recipient'),
	 ('Zenith Parser Tools','Zenith','Passenger type'),
	 ('Zenith Parser Tools','Zenith','Passenger designations'),
	 ('Zenith Parser Tools','Zenith','E-ticket possible format'),
	 ('Zenith Parser Tools','Zenith','Itinerary header possible format'),
	 ('Zenith Parser Tools','Zenith','Header names'),
	 ('Zenith Parser Tools','Zenith','Service carrier'),
	 ('Zenith Parser Tools','Zenith','Airport agency code'),
	 ('Zenith Parser Tools','Zenith','Current travel agency identifier'),
	 ('Zenith Parser Tools','Zenith','Non relevant identifier for passenger');
INSERT INTO t_config (name,to_be_applied_on,value_name) VALUES
	 ('Zenith Parser Tools','Zenith','Itinerary name'),
	 ('Zenith Parser Tools','Zenith','Cost detail identifier'),
	 ('Zenith Parser Tools','Zenith','Ancillaries identifier'),
	 ('Zenith Parser Tools','Zenith','Not emitted PNR start identifier'),
	 ('Zenith Parser Tools','Zenith','Not emitted PNR start passenger'),
	 ('Zenith Parser Tools','Zenith','Not emitted PNR start booking'),
	 ('Zenith Parser Tools','Zenith','Not emitted PNR start booking cost'),
	 ('Zenith Parser Tools','Zenith','Not emitted pnr start opc'),
	 ('Zenith Parser Tools','Zenith','Not emitted pnr end opc'),
	 ('Zenith Parser Tools','Zenith','To be excluded recipient email');
INSERT INTO t_config (name,to_be_applied_on,value_name) VALUES
	 ('Zenith Parser Tools','Zenith','EMD reference start'),
	 ('Zenith Parser Tools','Zenith','EMD expiry date start'),
	 ('Zenith Parser Tools','Zenith','EMD comment start'),
	 ('Zenith Parser Tools','Zenith','Total identifier'),
	 ('Zenith Parser Tools','Zenith','Passenger word identifier'),
	 ('Zenith Parser Tools','Zenith','Payment method identifier'),
	 ('Zenith Parser Tools','Zenith','Issuing date identifier'),
	 ('Zenith Parser Tools','Zenith','Issuing office identifier'),
	 ('Zenith Parser Tools','Zenith','Cost word identifier'),
	 ('Zenith Parser Tools','Zenith','Modification identifier');
INSERT INTO t_config (name,to_be_applied_on,value_name) VALUES
	 ('Zenith Parser Tools','Zenith','Tax identifier'),
	 ('Zenith Parser Tools','Zenith','Receipt identifier'),
	 ('Zenith Parser Tools','Zenith','Customer name identifier'),
	 ('Zenith Parser Tools','Zenith','Itinerary airport iata code identifier'),
	 ('Zenith Receipt Parser Tools','Zenith','Payment option'),
	 ('Zenith Receipt Parser Tools','Zenith','Ticket number prefix'),
	 ('Zenith Receipt Parser Tools','Zenith','To be excluded keywords'),
	 ('Zenith Receipt Parser Tools','Zenith','Aiport agency code'),
	 ('Zenith Receipt Parser Tools','Zenith','Started process date'),
	 ('Zenith Receipt Parser Tools','Zenith','Current travel agency identifier');
INSERT INTO t_config (name,to_be_applied_on,value_name) VALUES
	 ('Zenith Receipt Parser Tools','Zenith','Ticket payment part'),
	 ('Zenith Receipt Parser Tools','Zenith','Adjustment part'),
	 ('Zenith Receipt Parser Tools','Zenith','EMD cancellation part'),
	 ('Zenith Receipt Parser Tools','Zenith','Ticket cancellation part'),
	 ('Zenith Receipt Parser Tools','Zenith','Penalty part'),
	 ('Zenith Receipt Parser Tools','Zenith','Agency fee part'),
	 ('Zenith Receipt Parser Tools','Zenith','EMD no number possible designation'),
	 ('Zenith Receipt Parser Tools','Zenith','Default passenger on object'),
	 ('Zenith Receipt Parser Tools','Zenith','EMD balancing statement part'),
	 ('TST Parser Tools','TST','Special agency code');
INSERT INTO t_config (name,to_be_applied_on,value_name) VALUES
	 ('TST Parser Tools','TST','Passenger designations'),
	 ('TST Parser Tools','TST','TST identifier'),
	 ('TST Parser Tools','TST','Ticket identifier'),
	 ('TST Parser Tools','TST','Cost identifier'),
	 ('TST Parser Tools','TST','Fare identifier'),
	 ('TST Parser Tools','TST','Fare equiv identifier'),
	 ('TST Parser Tools','TST','Total identifier'),
	 ('TST Parser Tools','TST','Grand Total identifier'),
	 ('PNR Parser Tools','PNR','PNR identifier'),
	 ('PNR Parser Tools','PNR','PNR type');
INSERT INTO t_config (name,to_be_applied_on,value_name) VALUES
	 ('PNR Parser Tools','PNR','Duplicate PNR identifier'),
	 ('PNR Parser Tools','PNR','Split PNR identifier'),
	 ('PNR Parser Tools','PNR','To be excluded line'),
	 ('PNR Parser Tools','PNR','Contact types'),
	 ('PNR Parser Tools','PNR','Contact type names'),
	 ('PNR Parser Tools','PNR','Ticket line identifier'),
	 ('PNR Parser Tools','PNR','Second degree ticket line identifier'),
	 ('PNR Parser Tools','PNR','Remark identifier'),
	 ('PNR Parser Tools','PNR','Passenger designations'),
	 ('PNR Parser Tools','PNR','Possible cost currency');
INSERT INTO t_config (name,to_be_applied_on,value_name) VALUES
	 ('PNR Parser Tools','PNR','AM H line identifier');
