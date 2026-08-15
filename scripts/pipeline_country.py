import argparse, json, subprocess, sys
from pathlib import Path
from datetime import date, datetime
import requests

ROOT=Path(__file__).resolve().parents[1]
CONFIG=ROOT/'config'/'countries.json'
DATA=ROOT/'data'; DATA.mkdir(exist_ok=True)

def load_cfg(): return json.loads(CONFIG.read_text(encoding='utf-8'))
def fetch_url(url):
    r=requests.get(url,timeout=30,headers={'User-Agent':'SeeStats/1.0 (+weekly-data-pipeline)'})
    r.raise_for_status()
    ct=r.headers.get('content-type','').lower()
    if 'json' in ct or url.lower().endswith('.json'): return {'kind':'json','content':r.json()}
    return {'kind':'text','content':r.text[:2_000_000]}

def run_ghana():
    legacy=ROOT/'scripts'/'legacy'/'run_pipeline.py'
    subprocess.run([sys.executable,str(legacy)],cwd=ROOT/'scripts'/'legacy',check=True)
    reports=ROOT/'scripts'/'legacy'/'reports'
    latest=sorted([p for p in reports.iterdir() if p.is_dir()])[-1]
    analysis=json.loads((latest/'analysis.json').read_text(encoding='utf-8'))
    out=DATA/'ghana-analysis.json'; out.write_text(json.dumps(analysis,indent=2),encoding='utf-8')
    return analysis

def run_generic(country):
    snapshots=[]; errors=[]
    for source in country.get('sources',[]):
        try:
            result=fetch_url(source['url']); snapshots.append({'name':source['name'],'url':source['url'],'kind':result['kind'],'retrieved_at':datetime.utcnow().isoformat()+'Z','sample':result['content'] if result['kind']=='json' else result['content'][:1000]})
        except Exception as exc: errors.append({'name':source['name'],'url':source['url'],'error':str(exc)})
    report={'analysis_date':str(date.today()),'country_code':country['code'],'country_name':country['name'],'status':'source_ingestion_only','summary':{'sources_configured':len(country.get('sources',[])),'sources_retrieved':len(snapshots),'source_errors':len(errors)},'source_snapshots':snapshots,'source_errors':errors,'import_opportunities':[],'export_opportunities':[],'top_5_overall':[]}
    (DATA/f"{country['code'].lower()}-report.json").write_text(json.dumps(report,indent=2),encoding='utf-8')
    return report

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--country',required=True); ap.add_argument('--config',default=str(CONFIG)); args=ap.parse_args()
    cfg=load_cfg(); c=next((x for x in cfg['countries'] if x['code'].upper()==args.country.upper()),None)
    if not c: raise SystemExit(f'Country {args.country} not found in config.')
    if not c.get('enabled'): raise SystemExit(f'{c["name"]} is disabled.')
    report=run_ghana() if c['code']=='GHA' else run_generic(c)
    api_base = __import__('os').environ.get('SEESTATS_API_BASE'); admin=__import__('os').environ.get('ADMIN_KEY')
    if api_base and admin:
        r=requests.post(api_base.rstrip('/')+'/api/admin/publish-report',headers={'X-Admin-Key':admin,'Content-Type':'application/json'},json={'country_code':c['code'],'report_date':report['analysis_date'],'payload':report},timeout=30); r.raise_for_status(); print('Published to Cloudflare:',r.json())
    else: print('SEESTATS_API_BASE / ADMIN_KEY not set; report generated locally only.')

if __name__=='__main__': main()
