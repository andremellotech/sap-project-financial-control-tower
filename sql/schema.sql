CREATE TABLE peps(pep TEXT PRIMARY KEY, pai TEXT, projeto TEXT, descricao TEXT, responsavel TEXT, leaf INTEGER);
CREATE TABLE context(data_corte TEXT);
CREATE TABLE facts(id TEXT PRIMARY KEY, pep TEXT REFERENCES peps(pep), kind TEXT, date TEXT, classe_custo TEXT, value INTEGER, source_file TEXT, source_line INTEGER, payload TEXT);
CREATE TABLE matches(id TEXT PRIMARY KEY, custo_id TEXT REFERENCES facts(id), pagamento_id TEXT REFERENCES facts(id), pep TEXT, classe_custo TEXT, value INTEGER);
CREATE TABLE provenance(name TEXT PRIMARY KEY, sha256 TEXT, bytes INTEGER, rows INTEGER);
CREATE TABLE controls(id TEXT PRIMARY KEY, fonte TEXT, pep TEXT REFERENCES peps(pep), classe_custo TEXT, actual_ref INTEGER, commitment_ref INTEGER, budget_ref INTEGER, remaining_plan_ref INTEGER, assigned_ref INTEGER, comparable INTEGER, delta_actual INTEGER, delta_commitment INTEGER, payload TEXT);
