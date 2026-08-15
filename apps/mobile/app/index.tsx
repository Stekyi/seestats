import React,{useEffect,useState} from 'react';
import {Pressable, Text, View, useWindowDimensions} from 'react-native';
import {useRouter} from 'expo-router';
import {analysis as seed} from '../lib/data';
import {getCountryReport} from '../lib/api';
import {AppShell, BarChart, Card, LockedCard, Pill, ScoreRing, SectionHeader, StatCard, s} from '../components/ui';
import {C} from '../lib/theme';

export default function Home(){
 const router=useRouter(); const {width}=useWindowDimensions(); const wide=width>700; const [analysis,setAnalysis]=useState(seed);
 useEffect(()=>{getCountryReport('GHA').then(r=>r.analysis&&setAnalysis(r.analysis)).catch(()=>{});},[]);
 return <AppShell active="index" title="Investment intelligence" subtitle={`Ghana · report snapshot · ${analysis.analysis_date}`}>
  <Pressable onPress={()=>router.push('/country')} style={{alignSelf:'flex-start',paddingHorizontal:11,paddingVertical:7,borderRadius:18,backgroundColor:C.panel,borderWidth:1,borderColor:C.line}}><Text style={{color:C.accent,fontSize:10,fontWeight:'900'}}>GHANA · CHANGE COUNTRY</Text></Pressable><View style={{gap:8}}><Text style={{color:C.text,fontSize:30,fontWeight:'900'}}>Where should capital go next?</Text><Text style={{color:C.muted,fontSize:13,maxWidth:720,lineHeight:20}}>See Stats turns official statistics and trade signals into ranked, investable themes — starting with Ghana and designed to expand country by country.</Text></View>
  <View style={{flexDirection:wide?'row':'column',gap:12}}><StatCard label="Import opportunities" value={analysis.summary.total_import_opps} delta="Ranked by opportunity score" icon="arrow-down-circle"/><StatCard label="Export opportunities" value={analysis.summary.total_export_opps} delta="Demand + margin + market fit" icon="arrow-up-circle"/><StatCard label="30%+ margin" value={analysis.summary.green_margin_opps} delta="Green margin signals" icon="trending-up"/><StatCard label="Budget fit" value={analysis.summary.budget_fit_opps} delta="Within GHC 100k model" icon="wallet"/></View>
  <View style={{flexDirection:wide?'row':'column',gap:16}}>
   <Card style={{flex:1}}><SectionHeader title="This week's top signals" subtitle="The opportunities with the strongest combination of market size, growth, margin and execution fit" right={<Pressable onPress={()=>router.push('/opportunities')}><Text style={{color:C.accent,fontSize:12,fontWeight:'800'}}>View all →</Text></Pressable>}/>
    <View style={{gap:10,marginTop:14}}>{analysis.top_5_overall.map((o,i)=><Pressable key={o.commodity} onPress={()=>router.push({pathname:'/opportunity',params:{id:o.commodity}})} style={{backgroundColor:C.panel2,borderRadius:13,padding:13,flexDirection:'row',alignItems:'center',gap:12}}><Text style={{color:C.muted,width:20,fontWeight:'800'}}>0{i+1}</Text><View style={{flex:1}}><Text style={{color:C.text,fontWeight:'800'}}>{o.commodity}</Text><Text style={{color:C.muted,fontSize:11,marginTop:3}}>{o.type==='export_opportunity'?'Export':'Import'} · {o.yoy_growth_pct}% YoY · {o.margin_pct}% margin</Text></View><ScoreRing score={o.score} size={54}/></Pressable>)}</View>
   </Card>
   <Card style={{flex:1,minWidth:320}}><SectionHeader title="Investor lens" subtitle="A quick read on where the signal is strongest"/><BarChart data={analysis.top_5_overall.map(o=>({label:o.commodity,value:o.score}))}/><View style={{borderTopWidth:1,borderTopColor:C.line,paddingTop:12}}><Text style={{color:C.muted,fontSize:11,lineHeight:17}}>Scores are decision-support signals, not guarantees. Validate pricing, regulation, logistics, counterparties and current source data before investing.</Text></View></Card>
  </View>
  <LockedCard onPress={()=>router.push('/blue-ocean')}/>
  <Card><SectionHeader title="How See Stats works" subtitle="One workflow from statistics to an investment decision"/><View style={{flexDirection:wide?'row':'column',gap:10,marginTop:16}}>{[['01','Observe','Collect official statistics and trade data'],['02','Score','Rank market gaps, growth, margins and access'],['03','Compare','See countries, commodities and markets side-by-side'],['04','Act','Move into diligence, contacts and a 90-day plan']].map(x=><View key={x[0]} style={{flex:1,backgroundColor:C.panel2,borderRadius:13,padding:14}}><Text style={{color:C.accent,fontWeight:'900',fontSize:11}}>{x[0]}</Text><Text style={{color:C.text,fontWeight:'800',marginTop:8}}>{x[1]}</Text><Text style={{color:C.muted,fontSize:11,lineHeight:16,marginTop:4}}>{x[2]}</Text></View>)}</View></Card>
 </AppShell>
}
