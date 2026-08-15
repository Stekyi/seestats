import {useEffect,useMemo,useState} from 'react';
import {getFeatureFlags,getMe} from './api';

export type FeatureFlag={key:string;label:string;description:string;enabled:boolean;subscriberOnly:boolean;updatedAt?:string};
export type FeatureMap=Record<string,FeatureFlag>;

let cached:FeatureMap|null=null;
let loadingPromise:Promise<FeatureMap>|null=null;

export async function loadFeatureFlags(force=false){
  if(cached&&!force)return cached;
  if(loadingPromise&&!force)return loadingPromise;
  loadingPromise=getFeatureFlags().then((x:any)=>{cached=x.features||{};return cached!}).finally(()=>{loadingPromise=null});
  return loadingPromise;
}

export function useFeatureFlags(){
  const [features,setFeatures]=useState<FeatureMap>(cached||{});
  const [loading,setLoading]=useState(!cached);
  useEffect(()=>{let mounted=true;loadFeatureFlags().then(f=>{if(mounted)setFeatures(f)}).catch(()=>{}).finally(()=>{if(mounted)setLoading(false)});return()=>{mounted=false}},[]);
  return {features,loading,refresh:async()=>setFeatures(await loadFeatureFlags(true))};
}

export function useFeatureAccess(featureKey:string){
  const {features,loading}=useFeatureFlags();
  const [subscriber,setSubscriber]=useState(false);
  useEffect(()=>{let mounted=true;getMe().then((m:any)=>{if(mounted)setSubscriber(!!m.isSubscriber)}).catch(()=>{if(mounted)setSubscriber(false)});return()=>{mounted=false}},[]);
  const feature=features[featureKey];
  const allowed=!!feature?.enabled&&(!feature.subscriberOnly||subscriber);
  return useMemo(()=>({feature,allowed,subscriber,loading}),[feature,allowed,subscriber,loading]);
}
