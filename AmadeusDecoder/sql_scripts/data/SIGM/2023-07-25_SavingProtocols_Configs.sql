--If there is a line delete that before--
delete from t_configuration where name = 'Saving File Tools';

--Insert the new value of the configuartion--
insert into t_configuration (environment, name, to_be_applied_on, value_name, single_value, dict_value, created_on, last_update, is_active) values 
('all', 'Saving File Tools', 'Global', 'File protocol', 'FTP', '"hostname"=>"51.75.181.181", "port"=>21, "username"=>"sigm", "password"=>"MGbi@261**", "repository"=>"/files/TEST", "link"=>"51.75.181.181/web/syncorders"', now(), now(), true);