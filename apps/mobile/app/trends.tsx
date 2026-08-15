import React from 'react';
import {Text,View} from 'react-native';
import {analysis,priceTrend,weeklyScores} from '../lib/data';
import {AppShell,FeatureGate,BarChart,Card,LineChart,SectionHeader} from '../components/ui';
import {C} from '../lib/theme';
export default function Trends(){return <FeatureGate featureKey="trends"><AppShell active="trends" title="Trend intelligence" subtitle="Weekly movement, price direction and signal persistence">
 <Card><SectionHeader title="Opportunity score persistence" subtitle="Composite top-signal score across weekly report runs"/><LineChart data={weeklyScores.map(x=>({label:x.week,value:x.score}))}/></Card>
 <View style={{flexDirection:'row',gap:16,flexWrap:'wrap'}}><Card style={{flex:1,minWidth:320}}><SectionHeader title="Selected price trend" subtitle="Example series from the discovery dataset"/><LineChart data={priceTrend.map(x=>({label:x.year,value:x.value}))}/></Card><Card style={{flex:1,minWidth:320}}><SectionHeader title="Current opportunity mix"/><BarChart data={[...analysis.import_opportunities,...analysis.export_opportunities].sort((a,b)=>b.score-a.score).slice(0,8).map(o=>({label:o.commodity,value:o.score}))}/></Card></View>
 <Card><SectionHeader title="How to read the trend"/><Text style={{color:C.muted,fontSize:12,lineHeight:19,marginTop:12}}>A rising score is useful when it is persistent and supported by independent indicators. See Stats should flag regime changes, but investors should still inspect the underlying time series, source revisions and methodology before committing capital.</Text></Card>
 </AppShell></FeatureGate>}
