type Env = {
  SEE_STATS_DB: D1Database;
  ADMIN_KEY?: string;
  RESEND_API_KEY?: string;
  FROM_EMAIL?: string;
  ACCESS_TTL_DAYS?: string;
};

type Ctx = {request:Request;env:Env;params:{path?:string[]}};
const json=(data:any,status=200)=>new Response(JSON.stringify(data),{status,headers:{'content-type':'application/json; charset=utf-8','cache-control':'no-store','access-control-allow-origin':'*','access-control-allow-headers':'Content-Type, Authorization, X-Admin-Key','access-control-allow-methods':'GET,POST,OPTIONS'}});
const now=()=>new Date();
const iso=(d:Date)=>d.toISOString();
async function hash(value:string){const b=await crypto.subtle.digest('SHA-256',new TextEncoder().encode(value));return [...new Uint8Array(b)].map(x=>x.toString(16).padStart(2,'0')).join('');}
function randomCode(){return String(Math.floor(100000+Math.random()*900000));}
function randomToken(){const bytes=new Uint8Array(32);crypto.getRandomValues(bytes);return btoa(String.fromCharCode(...bytes)).replaceAll('+','-').replaceAll('/','_').replaceAll('=','');}
async function body(r:Request){try{return await r.json()}catch{return {}}}
async function sendEmail(env:Env,to:string,code:string){
 if(!env.RESEND_API_KEY) throw new Error('Email delivery is not configured. Add RESEND_API_KEY and FROM_EMAIL in Cloudflare.');
 const r=await fetch('https://api.resend.com/emails',{method:'POST',headers:{'Authorization':`Bearer ${env.RESEND_API_KEY}`,'Content-Type':'application/json'},body:JSON.stringify({from:env.FROM_EMAIL||'See Stats <noreply@example.com>',to:[to],subject:'Your See Stats subscriber access code',html:`<div style="font-family:Arial,sans-serif;max-width:520px"><h2>See Stats</h2><p>Your subscriber access code is:</p><div style="font-size:32px;font-weight:800;letter-spacing:8px">${code}</div><p>This is a one-time code and expires in 3 days. Once verified, your private Blue Ocean session also lasts 3 days.</p><p>If you did not request this, ignore this email.</p></div>`})});
 if(!r.ok) throw new Error('Email provider rejected the message.');
}
async function authUser(req:Request,env:Env){const h=req.headers.get('Authorization')||'';if(!h.startsWith('Bearer '))return null;const tokenHash=await hash(h.slice(7));const row=await env.SEE_STATS_DB.prepare('SELECT u.id,u.email,u.is_subscriber,u.subscriber_until,s.expires_at FROM access_sessions s JOIN users u ON u.id=s.user_id WHERE s.token_hash=?').bind(tokenHash).first<any>();if(!row)return null;if(new Date(row.expires_at)<=now())return null;if(!row.is_subscriber)return null;if(row.subscriber_until&&new Date(row.subscriber_until)<=now())return null;return row;}
async function admin(req:Request,env:Env){return !!env.ADMIN_KEY && req.headers.get('X-Admin-Key')===env.ADMIN_KEY;}
async function getFeatures(env:Env){
 const {results}=await env.SEE_STATS_DB.prepare('SELECT feature_key,label,description,enabled,subscriber_only,updated_at FROM feature_flags ORDER BY feature_key').all<any>();
 return (results||[]).reduce((acc:any,f:any)=>{acc[f.feature_key]={key:f.feature_key,label:f.label,description:f.description||'',enabled:!!f.enabled,subscriberOnly:!!f.subscriber_only,updatedAt:f.updated_at};return acc;},{});
}
function canUseFeature(features:any,key:string,isSubscriber:boolean){const f=features[key];if(!f||!f.enabled)return false;return !f.subscriberOnly||isSubscriber;}

export async function onRequest({request,env,params}:Ctx){
 if(request.method==='OPTIONS')return json({},204);
 const path='/'+(params.path||[]).join('/');
 try{
  if(path==='/auth/request-code'&&request.method==='POST'){
   const {email}=await body(request);const normalized=String(email||'').trim().toLowerCase();if(!/^\S+@\S+\.\S+$/.test(normalized))return json({error:'Enter a valid email address.'},400);
   const user=await env.SEE_STATS_DB.prepare('SELECT * FROM users WHERE email=?').bind(normalized).first<any>();
   if(!user?.is_subscriber || (user.subscriber_until&&new Date(user.subscriber_until)<=now()))return json({error:'This email is not an active subscriber. Contact See Stats to activate your subscription.'},403);
   const recent=await env.SEE_STATS_DB.prepare("SELECT COUNT(*) c FROM login_codes WHERE email=? AND created_at>datetime('now','-1 hour')").bind(normalized).first<any>();if(Number(recent?.c||0)>=5)return json({error:'Too many access-code requests. Try again later.'},429);
   const code=randomCode(), expires=new Date(now().getTime()+3*86400000), id=crypto.randomUUID(), codeHash=await hash(code);await env.SEE_STATS_DB.prepare('INSERT INTO login_codes(id,email,code_hash,expires_at) VALUES(?,?,?,?)').bind(id,normalized,codeHash,iso(expires)).run();await sendEmail(env,normalized,code);return json({ok:true,message:'Access code sent.'});
  }
  if(path==='/auth/verify-code'&&request.method==='POST'){
   const {email,code}=await body(request);const normalized=String(email||'').trim().toLowerCase();const codeHash=await hash(String(code||''));const row=await env.SEE_STATS_DB.prepare('SELECT * FROM login_codes WHERE email=? AND code_hash=? AND used_at IS NULL ORDER BY created_at DESC LIMIT 1').bind(normalized,codeHash).first<any>();if(!row)return json({error:'Invalid access code.'},401);if(new Date(row.expires_at)<=now())return json({error:'Access code has expired. Request a new one.'},401);
   const user=await env.SEE_STATS_DB.prepare('SELECT * FROM users WHERE email=?').bind(normalized).first<any>();if(!user)return json({error:'Subscriber record not found.'},403);if(!user.is_subscriber||(user.subscriber_until&&new Date(user.subscriber_until)<=now()))return json({error:'Your subscription is not active.'},403);
   await env.SEE_STATS_DB.prepare('UPDATE login_codes SET used_at=? WHERE id=?').bind(iso(now()),row.id).run();const token=randomToken(), tokenHash=await hash(token), days=Number(env.ACCESS_TTL_DAYS||3), expires=new Date(now().getTime()+days*86400000);await env.SEE_STATS_DB.prepare('INSERT INTO access_sessions(token_hash,user_id,expires_at) VALUES(?,?,?)').bind(tokenHash,user.id,iso(expires)).run();return json({token,expiresAt:iso(expires),isSubscriber:true,email:normalized});
  }
  if(path==='/config/features'&&request.method==='GET'){return json({features:await getFeatures(env)});}
  if(path==='/auth/me'&&request.method==='GET'){const u=await authUser(request,env);const features=await getFeatures(env);if(!u)return json({isSubscriber:false,features});return json({isSubscriber:true,email:u.email,expiresAt:u.expires_at,features});}
  if(path==='/premium/discoveries'&&request.method==='GET'){
   const featureKey=new URL(request.url).searchParams.get('feature')||'blue_ocean'; const features=await getFeatures(env); const feature=features[featureKey]; if(!feature||!feature.enabled)return json({error:'Feature unavailable'},404);
   const user=await authUser(request,env); if(feature.subscriberOnly&&!user)return json({error:'Subscriber access required'},403);
   const row=await env.SEE_STATS_DB.prepare("SELECT country_code,payload,updated_at FROM premium_content WHERE content_key='blue_ocean_discoveries' LIMIT 1").first<any>(); if(!row)return json({error:'Premium content is not published yet.'},404);
   return json({country:row.country_code,updatedAt:row.updated_at,discoveries:JSON.parse(row.payload)});
  }
  if(path==='/reports/latest'&&request.method==='GET'){const country=new URL(request.url).searchParams.get('country')||'GHA';const row=await env.SEE_STATS_DB.prepare('SELECT country_code,report_date,payload FROM reports WHERE country_code=? ORDER BY report_date DESC LIMIT 1').bind(country).first<any>();if(!row)return json({error:'No cloud report yet.'},404);return json({country:row.country_code,reportDate:row.report_date,analysis:JSON.parse(row.payload)});}
  if(path==='/admin/set-subscriber'&&request.method==='POST'){if(!await admin(request,env))return json({error:'Unauthorized'},401);const {email,active=true,days=30}=await body(request);const normalized=String(email||'').trim().toLowerCase();if(!normalized)return json({error:'email required'},400);const id=crypto.randomUUID();const until=active?new Date(now().getTime()+Number(days)*86400000).toISOString():null;await env.SEE_STATS_DB.prepare(`INSERT INTO users(id,email,is_subscriber,subscriber_until) VALUES(?,?,?,?) ON CONFLICT(email) DO UPDATE SET is_subscriber=excluded.is_subscriber,subscriber_until=excluded.subscriber_until,updated_at=CURRENT_TIMESTAMP`).bind(id,normalized,active?1:0,until).run();return json({ok:true,email:normalized,isSubscriber:!!active,subscriberUntil:until});}
  if(path==='/admin/features'&&request.method==='GET'){if(!await admin(request,env))return json({error:'Unauthorized'},401);return json({features:await getFeatures(env)});}
  if(path==='/admin/features'&&request.method==='POST'){
   if(!await admin(request,env))return json({error:'Unauthorized'},401);
   const data=await body(request); const updates=Array.isArray(data.features)?data.features:[data];
   if(!updates.length)return json({error:'features array required'},400);
   for(const f of updates){if(!f?.feature_key)return json({error:'feature_key required'},400);
    const existing=await env.SEE_STATS_DB.prepare('SELECT label,description FROM feature_flags WHERE feature_key=?').bind(String(f.feature_key)).first<any>();
    const label=String(f.label??existing?.label??f.feature_key); const description=String(f.description??existing?.description??'');
    await env.SEE_STATS_DB.prepare(`INSERT INTO feature_flags(feature_key,label,description,enabled,subscriber_only) VALUES(?,?,?,?,?) ON CONFLICT(feature_key) DO UPDATE SET label=excluded.label,description=excluded.description,enabled=excluded.enabled,subscriber_only=excluded.subscriber_only,updated_at=CURRENT_TIMESTAMP`).bind(String(f.feature_key),label,description,f.enabled===false?0:1,f.subscriber_only===true||f.subscriberOnly===true?1:0).run();
   }
   return json({ok:true,features:await getFeatures(env)});
  }
  if(path==='/admin/publish-premium'&&request.method==='POST'){
   if(!await admin(request,env))return json({error:'Unauthorized'},401); const {content_key='blue_ocean_discoveries',country_code='GHA',payload}=await body(request); if(!payload)return json({error:'payload required'},400);
   await env.SEE_STATS_DB.prepare(`INSERT INTO premium_content(content_key,country_code,payload) VALUES(?,?,?) ON CONFLICT(content_key) DO UPDATE SET country_code=excluded.country_code,payload=excluded.payload,updated_at=CURRENT_TIMESTAMP`).bind(String(content_key),String(country_code),JSON.stringify(payload)).run(); return json({ok:true,content_key,country_code});
  }
  if(path==='/admin/publish-report'&&request.method==='POST'){if(!await admin(request,env))return json({error:'Unauthorized'},401);const {country_code,report_date,payload}=await body(request);if(!country_code||!report_date||!payload)return json({error:'country_code, report_date and payload required'},400);const id=crypto.randomUUID();await env.SEE_STATS_DB.prepare(`INSERT INTO reports(id,country_code,report_date,payload) VALUES(?,?,?,?) ON CONFLICT(country_code,report_date) DO UPDATE SET payload=excluded.payload`).bind(id,country_code,report_date,JSON.stringify(payload)).run();return json({ok:true,country_code,report_date});}
  if(path==='/admin/countries'&&request.method==='POST'){if(!await admin(request,env))return json({error:'Unauthorized'},401);const {countries}=await body(request);if(!Array.isArray(countries))return json({error:'countries array required'},400);for(const c of countries){await env.SEE_STATS_DB.prepare(`INSERT INTO countries(code,name,enabled,source_urls) VALUES(?,?,?,?) ON CONFLICT(code) DO UPDATE SET name=excluded.name,enabled=excluded.enabled,source_urls=excluded.source_urls,updated_at=CURRENT_TIMESTAMP`).bind(c.code,c.name,c.enabled?1:0,JSON.stringify(c.sources||[])).run();}return json({ok:true,count:countries.length});}
  if(path==='/admin/countries'&&request.method==='GET'){if(!await admin(request,env))return json({error:'Unauthorized'},401);const {results}=await env.SEE_STATS_DB.prepare('SELECT code,name,enabled,source_urls FROM countries ORDER BY name').all<any>();return json({countries:(results||[]).map(c=>({...c,enabled:!!c.enabled,sources:JSON.parse(c.source_urls||'[]')}))});}
  return json({error:'Not found'},404);
 }catch(e:any){return json({error:e?.message||'Server error'},500)}
}
