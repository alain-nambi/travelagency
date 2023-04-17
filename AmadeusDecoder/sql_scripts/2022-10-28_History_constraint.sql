-- constraints on t_pnr history
begin;
alter table t_pnr_history drop constraint t_pnr_history_agency_code_3759ef31_fk_t_office_code;
alter table t_pnr_history add constraint t_pnr_history_agency_code_3759ef31_fk_t_office_code foreign key (agency_code) references t_office(code) on delete set null;
alter table t_pnr_history drop constraint t_pnr_history_agent_id_294ff9dd_fk_t_user_id;
alter table t_pnr_history add constraint t_pnr_history_agent_id_294ff9dd_fk_t_user_id FOREIGN KEY (agent_id) REFERENCES t_user(id) on delete set null;
alter table t_pnr_history drop constraint t_pnr_history_currency_code_7d7ad879_fk_t_currency_code;
alter table t_pnr_history add constraint t_pnr_history_currency_code_7d7ad879_fk_t_currency_code  FOREIGN KEY (currency_code) REFERENCES t_currency(code) on delete set null;
alter table t_pnr_history drop constraint t_pnr_history_parent_pnr_id_716ff49d_fk_t_pnr_id;
alter table t_pnr_history add constraint t_pnr_history_parent_pnr_id_716ff49d_fk_t_pnr_id FOREIGN KEY (parent_pnr_id) REFERENCES t_pnr(id) on delete set null;
alter table t_pnr_history drop constraint t_pnr_history_pnr_id_f6bbf93a_fk_t_pnr_id;
alter table t_pnr_history add constraint t_pnr_history_pnr_id_f6bbf93a_fk_t_pnr_id  FOREIGN KEY (pnr_id) REFERENCES t_pnr(id) on delete set null;
commit;