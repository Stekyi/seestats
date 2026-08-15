import React from 'react';
import {Pressable,Text,View} from 'react-native';
import {useRouter} from 'expo-router';
import {countries} from '../lib/data';
import {AppShell,FeatureGate,Card,SectionHeader,Pill} from '../components/ui';
import {C} from '../lib/theme';
export default function Country(){const router=useRouter();return <FeatureGate featureKey="country"><AppShell active="index" title="Country intelligence" subtitle="Choose a market to inspect"><Card><SectionHeader title="Coverage map" subtitle="The platform is designed to scale from Ghana to a global country catalogue."/><View style={{gap:9,marginTop:12}}>{countries.map(c=><Pressable key={c.code} onPress={()=>c.enabled&&router.push('/')} style={{padding:14,backgroundColor:C.panel2,borderRadius:13,flexDirection:'row',alignItems:'center',gap:12,opacity:c.enabled?1:.55}}><View style={{flex:1}}><Text style={{color:C.text,fontWeight:'800'}}>{c.name}</Text><Text style={{color:C.muted,fontSize:11,marginTop:3}}>{c.code} · {c.sources.length} source connections</Text></View><Pill tone={c.enabled?'good':'neutral'}>{c.enabled?'LIVE':'COMING SOON'}</Pill></Pressable>)}</View></Card></AppShell></FeatureGate>}
