create temp table temp_fee as select * from t_fee;

update t_fee set newest_cost = tef.cost from temp_fee tef where t_fee.id = tef.id;