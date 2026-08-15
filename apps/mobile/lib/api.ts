import AsyncStorage from '@react-native-async-storage/async-storage';

const base = (process.env.EXPO_PUBLIC_API_BASE_URL || '').replace(/\/$/,'');
const TOKEN_KEY = 'see_stats_access_token';

async function request(path:string, options:RequestInit={}) {
  const token = await AsyncStorage.getItem(TOKEN_KEY);
  const headers = new Headers(options.headers);
  headers.set('Content-Type','application/json');
  if (token) headers.set('Authorization', `Bearer ${token}`);
  const res = await fetch(`${base}/api${path}`, {...options,headers});
  const body = await res.json().catch(()=>({}));
  if (!res.ok) throw new Error(body.error || 'Request failed');
  return body;
}
export async function requestCode(email:string) { return request('/auth/request-code',{method:'POST',body:JSON.stringify({email})}); }
export async function verifyCode(email:string,code:string) {
  const body = await request('/auth/verify-code',{method:'POST',body:JSON.stringify({email,code})});
  if (body.token) await AsyncStorage.setItem(TOKEN_KEY,body.token);
  return body;
}
export async function getMe() { return request('/auth/me'); }
export async function getFeatureFlags() { return request('/config/features'); }
export async function logout() { await AsyncStorage.removeItem(TOKEN_KEY); }
export async function getCountryReport(code:string) { return request(`/reports/latest?country=${encodeURIComponent(code)}`); }
export async function getPremiumDiscoveries(feature:string='blue_ocean') { return request(`/premium/discoveries?feature=${encodeURIComponent(feature)}`); }
export async function hasToken() { return !!(await AsyncStorage.getItem(TOKEN_KEY)); }
