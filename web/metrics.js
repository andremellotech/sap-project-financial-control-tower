'use strict';
globalThis.FinanceMetrics = (() => {
  function descendants(report, selected) {
    if (!selected) return new Set(report.peps.map(p=>p.pep));
    const found = new Set([selected]);
    let changed = true;
    while (changed) { changed=false; for (const p of report.peps) if (found.has(p.pai)&&!found.has(p.pep)) {found.add(p.pep);changed=true;} }
    return found;
  }
  function scope(report, project='', pep='', costClass='') {
    const ids = descendants(report,pep);
    return report.facts.filter(f=>ids.has(f.pep)&&(!project||f.project===project)&&(!costClass||f.classe_custo===costClass));
  }
  function totals(report, facts) {
    const t={baseline:0,baseline_cut:0,actual:0,commitment:0,etc:0,paid:0,cash_commitment:0,settlement:0,overdue_commitment:0,matched:0};
    const kind={BASELINE:'baseline',REALIZADO:'actual',COMPROMISSO:'commitment',ETC:'etc',PAGAMENTO:'paid',COMPROMISSO_PAGAMENTO:'cash_commitment',LIQUIDACAO:'settlement'};
    const ids=new Set(facts.map(f=>f.id));
    for(const f of facts) {
      t[kind[f.kind]]+=f.value;
      if(f.kind==='BASELINE'&&f.date.slice(0,7)<=report.manifest.data_corte.slice(0,7)) t.baseline_cut+=f.value;
      if(f.kind==='COMPROMISSO'&&f.date<report.manifest.data_corte) t.overdue_commitment+=f.value;
    }
    for(const m of report.matches) if(ids.has(m.custo_id)&&ids.has(m.pagamento_id)) t.matched+=m.value;
    t.eac=t.actual+t.commitment+t.etc;
    t.variance=t.eac-t.baseline;
    t.variance_cut=t.actual-t.baseline_cut;
    t.actual_unmatched=t.actual-t.matched;
    t.cash_unmatched=t.paid-t.matched;
    return t;
  }
  function adherence(t){
    const ratio=(a,b)=>b>0?a/b:null;
    return {eacToBaseline:ratio(t.eac,t.baseline),actualToPlan:ratio(t.actual,t.baseline_cut),remainingEac:t.eac-t.actual,remainingBaseline:t.baseline-t.actual,committedCoverage:ratio(t.commitment,t.eac-t.actual)};
  }
  function controls(report,project='',pep='',costClass=''){
    const ids=descendants(report,pep),projects=new Map(report.peps.map(p=>[p.pep,p.projeto]));
    return report.controls.filter(c=>ids.has(c.pep)&&(!project||projects.get(c.pep)===project)&&(!costClass||c.classe_custo===costClass));
  }
  function buildUp(report,facts,group='pep'){
    const summarize=rows=>{const t=totals(report,rows);return {...t,remaining:t.commitment+t.etc};};
    let rows;
    if(group==='project'){
      rows=[...new Set(facts.map(f=>f.project))].sort().map(id=>({id,label:id,description:report.peps.find(p=>p.projeto===id&&!p.pai)?.descricao||id,...summarize(facts.filter(f=>f.project===id))}));
    }else{
      const selected=new Set(facts.map(f=>f.pep));
      rows=report.peps.filter(p=>p.leaf&&selected.has(p.pep)).map(p=>({id:p.pep,label:p.pep,description:p.descricao,project:p.projeto,...summarize(facts.filter(f=>f.pep===p.pep))}));
    }
    return {rows,total:summarize(facts)};
  }
  return {scope,totals,descendants,adherence,controls,buildUp};
})();
