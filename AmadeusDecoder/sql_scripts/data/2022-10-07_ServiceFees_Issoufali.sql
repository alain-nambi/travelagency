-- Service Fees for Issoufaly only
delete from t_servicefees_amount_based;
-- Update 1
insert into t_servicefees_amount_based(min_interval, max_interval, fee, last_update) values
(1, 250, 30, current_timestamp),
(251, 350, 35, current_timestamp),
(351, 550, 40, current_timestamp),
(551, 960, 45, current_timestamp),
(961, 1250, 75, current_timestamp),
(1251, 1760, 85, current_timestamp),
(1761, 0, 95, current_timestamp);
delete from t_servicefees_amount_based;
-- Update 2
insert into t_servicefees_amount_based(min_interval, max_interval, fee, last_update) values
(0, 250, 35, current_timestamp),
(251, 350, 40, current_timestamp),
(351, 550, 45, current_timestamp),
(551, 960, 50, current_timestamp),
(961, 1250, 80, current_timestamp),
(1251, 1760, 90, current_timestamp),
(1761, 2150, 100, current_timestamp),
(2151, 2951, 120, current_timestamp),
(2952, 0, 190, current_timestamp);
delete from t_servicefees_amount_based;
-- Update 3
insert into t_servicefees_amount_based(min_interval, max_interval, fee, last_update, effective_date) values
(0, 250, 35, current_timestamp, current_timestamp),
(251, 550, 40, current_timestamp, current_timestamp),
(551, 960, 50, current_timestamp, current_timestamp),
(961, 1250, 80, current_timestamp, current_timestamp),
(1251, 1760, 90, current_timestamp, current_timestamp),
(1761, 2150, 100, current_timestamp, current_timestamp),
(2151, 2951, 120, current_timestamp, current_timestamp),
(2952, 0, 190, current_timestamp, current_timestamp);