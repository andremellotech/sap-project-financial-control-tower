-- Os fatos já são posições normalizadas e validadas, não tabelas SAP brutas.
-- Agregar cada PEP folha; nunca juntar custos a pagamentos por documento/pedido.
CREATE VIEW vw_pep_finance AS
SELECT p.pep,
 COALESCE(SUM(CASE WHEN f.kind='BASELINE' THEN value ELSE 0 END),0) baseline,
 COALESCE(SUM(CASE WHEN f.kind='BASELINE' AND substr(date,1,7)<=substr(c.data_corte,1,7) THEN value ELSE 0 END),0) baseline_cut,
 COALESCE(SUM(CASE WHEN f.kind='REALIZADO' THEN value ELSE 0 END),0) actual,
 COALESCE(SUM(CASE WHEN f.kind='COMPROMISSO' THEN value ELSE 0 END),0) commitment,
 COALESCE(SUM(CASE WHEN f.kind='ETC' THEN value ELSE 0 END),0) etc,
 COALESCE(SUM(CASE WHEN f.kind='PAGAMENTO' THEN value ELSE 0 END),0) paid,
 COALESCE(SUM(CASE WHEN f.kind='COMPROMISSO_PAGAMENTO' THEN value ELSE 0 END),0) cash_commitment,
 COALESCE(SUM(CASE WHEN f.kind='LIQUIDACAO' THEN value ELSE 0 END),0) settlement,
 COALESCE(SUM(CASE WHEN f.kind='COMPROMISSO' AND date<c.data_corte THEN value ELSE 0 END),0) overdue_commitment,
 COALESCE((SELECT SUM(m.value) FROM matches m WHERE m.pep=p.pep),0) matched
FROM peps p CROSS JOIN context c LEFT JOIN facts f ON f.pep=p.pep
WHERE p.leaf=1 GROUP BY p.pep;

CREATE VIEW vw_eac AS SELECT *,
 actual+commitment+etc eac,
 actual+commitment+etc-baseline variance,
 actual-baseline_cut variance_cut,
 actual-matched actual_unmatched,
 paid-matched cash_unmatched
FROM vw_pep_finance;

CREATE VIEW vw_monthly AS
SELECT pep, substr(date,1,7) period, kind, SUM(value) value
FROM facts GROUP BY pep, substr(date,1,7), kind;
