const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const sandbox = {globalThis:{}};
vm.runInNewContext(fs.readFileSync('web/metrics.js','utf8'),sandbox);
const M = sandbox.globalThis.FinanceMetrics;
const r = JSON.parse(fs.readFileSync('reports/demo/relatorio.json','utf8'));
const all = M.scope(r,'','','');
assert.deepEqual(JSON.parse(JSON.stringify(M.totals(r,all))),r.totals);
const engineering = M.scope(r,'','PRJ-01.01.01','');
assert.equal(M.totals(r,engineering).eac,22_000_000);
assert.equal(M.totals(r,engineering).matched,8_000_000);
const parent = M.scope(r,'','PRJ-01.01','');
assert.equal(M.totals(r,parent).actual,45_000_000);
assert.equal(M.totals(r,M.scope(r,'AURORA','','EQUIPAMENTOS')).eac,47_000_000);
assert.equal(M.totals(r,M.scope(r,'INEXISTENTE','','')).actual,0);
assert.equal(M.totals(r,M.scope(r,'','PRJ-01.02','SERVICOS')).eac,0);
assert.equal(M.adherence(r.totals).eacToBaseline,595/580);
assert.equal(M.adherence(r.totals).actualToPlan,315/471);
assert.equal(M.adherence({...r.totals,baseline:0}).eacToBaseline,null);
assert.equal(M.adherence({...r.totals,baseline_cut:0}).actualToPlan,null);
assert.equal(M.controls(r,'','PRJ-01.01','').length,3);
assert.equal(M.controls(r,'','','EQUIPAMENTOS')[0].delta_actual,0);
console.log('Filtros por subárvore/classe, SQL × JS, custo × caixa e EAC: OK');

for(const [project,base,actual,eac] of [['AURORA',100000000,48000000,105000000],['HORIZONTE',240000000,85000000,232000000],['ATLAS',160000000,113000000,182000000],['VERTICE',80000000,69000000,76000000]]){
 const t=M.totals(r,M.scope(r,project,'',''));assert.equal(t.baseline,base);assert.equal(t.actual,actual);assert.equal(t.eac,eac);
}
console.log('Quatro projetos: filtros independentes e totais do portfolio conferidos.');

const byPep=M.buildUp(r,all,'pep');
assert.equal(byPep.rows.length,22);
assert.equal(new Set(byPep.rows.map(p=>p.id)).size,22);
for(const key of ['baseline','actual','commitment','etc','eac']){
 assert.equal(byPep.rows.reduce((sum,p)=>sum+p[key],0),r.totals[key]);
 assert.equal(byPep.total[key],r.totals[key]);
}
assert.equal(byPep.total.remaining,280_000_000);
const byProject=M.buildUp(r,all,'project');
assert.equal(byProject.rows.length,4);
assert.equal(byProject.rows.find(p=>p.id==='ATLAS').eac,182_000_000);
for(const key of ['baseline','actual','remaining','eac'])assert.equal(byProject.rows.reduce((sum,p)=>sum+p[key],0),byProject.total[key]);
const subtree=M.buildUp(r,parent,'pep');
assert.equal(subtree.rows.length,3);
assert.equal(subtree.total.eac,92_000_000);
assert.equal(subtree.rows.some(p=>p.id==='PRJ-01.01'),false);
const equipment=M.buildUp(r,M.scope(r,'AURORA','','EQUIPAMENTOS'),'pep');
assert.equal(equipment.rows.length,1);
assert.equal(equipment.total.eac,47_000_000);
assert.equal(M.buildUp(r,[],'pep').rows.length,0);
assert.equal(M.buildUp(r,[],'pep').total.eac,0);
const creditFacts=[{...all[0],id:'credit',kind:'REALIZADO',value:-10000},{...all[0],id:'remaining',kind:'ETC',value:5000}];
const credit=M.buildUp({...r,matches:[]},creditFacts,'pep');
assert.equal(credit.total.actual,-10000);
assert.equal(credit.total.remaining,5000);
assert.equal(credit.total.eac,-5000);
console.log('Build-up por PEP/projeto: total sem duplicar pais, filtros, vazio e créditos conferidos.');
