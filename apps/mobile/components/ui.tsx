import React, {ReactNode} from 'react';
import {ActivityIndicator, Pressable, ScrollView, StyleSheet, Text, TextInput, useWindowDimensions, View} from 'react-native';
import {Ionicons} from '@expo/vector-icons';
import {useRouter} from 'expo-router';
import Svg, {Circle, Line, Path, Text as SvgText} from 'react-native-svg';
import {C, shadow} from '../lib/theme';
import {useFeatureFlags,useFeatureAccess} from '../lib/features';

export function Card({children, style}:{children:ReactNode;style?:any}){return <View style={[s.card,style]}>{children}</View>}
export function Pill({children,tone='neutral'}:{children:ReactNode;tone?:'good'|'warn'|'bad'|'info'|'neutral'}){
 const bg=tone==='good'?'#12392f':tone==='warn'?'#3b3016':tone==='bad'?'#3d2025':tone==='info'?'#162f51':'#1a293b';
 const color=tone==='good'?C.accent:tone==='warn'?C.gold:tone==='bad'?C.red:tone==='info'?C.accent2:C.muted;
 return <View style={[s.pill,{backgroundColor:bg}]}><Text style={[s.pillText,{color}]}>{children}</Text></View>
}
export function StatCard({label,value,delta,icon}:{label:string;value:string|number;delta?:string;icon?:keyof typeof Ionicons.glyphMap}){
 return <Card style={{flex:1,minWidth:155}}><View style={s.statTop}><Text style={s.label}>{label}</Text>{icon&&<Ionicons name={icon} size={18} color={C.accent}/>}</View><Text style={s.statValue}>{value}</Text>{delta&&<Text style={s.delta}>{delta}</Text>}</Card>
}
export function SectionHeader({title,subtitle,right}:{title:string;subtitle?:string;right?:ReactNode}){return <View style={s.sectionHead}><View style={{flex:1}}><Text style={s.sectionTitle}>{title}</Text>{subtitle&&<Text style={s.sectionSub}>{subtitle}</Text>}</View>{right}</View>}
export function SearchBox({value,onChange,placeholder='Search'}:{value:string;onChange:(v:string)=>void;placeholder?:string}){return <View style={s.search}><Ionicons name="search" size={18} color={C.muted}/><TextInput value={value} onChangeText={onChange} placeholder={placeholder} placeholderTextColor={C.muted} style={s.searchInput}/></View>}

const nav=[['index','grid-outline','Overview',''],['opportunities','trending-up-outline','Opportunities','opportunities'],['trends','analytics-outline','Trends','trends'],['blue-ocean','sparkles-outline','Blue Ocean','blue_ocean'],['account','person-circle-outline','Account','']] as const;
export function AppShell({children,title,subtitle,active}:{children:ReactNode;title:string;subtitle?:string;active:string}){
 const {width}=useWindowDimensions(); const mobile=width<800;
 return <View style={s.root}>
   {!mobile && <View style={s.sidebar}><View style={s.brand}><View style={s.logo}><Text style={s.logoText}>S</Text></View><View><Text style={s.brandText}>see stats</Text><Text style={s.brandSub}>INVESTMENT INTELLIGENCE</Text></View></View>
    <Text style={s.navCaption}>DISCOVER</Text>{nav.map(([key,icon,label,feature])=><NavItem key={key} route={key} icon={icon} label={label} active={active} featureKey={feature}/>) }
    <View style={{flex:1}}/><View style={s.sidebarFooter}><Text style={s.smallMuted}>Weekly intelligence</Text><Text style={s.smallMuted}>Data refreshed automatically</Text></View>
   </View>}
   <View style={{flex:1}}><View style={[s.topbar,mobile&&{paddingHorizontal:16}]}><View style={{flex:1}}><Text style={s.pageTitle}>{title}</Text>{subtitle&&<Text style={s.pageSub}>{subtitle}</Text>}</View><View style={s.live}><View style={s.liveDot}/><Text style={s.liveText}>DATA LIVE</Text></View></View>
   <ScrollView contentContainerStyle={[s.content,mobile&&{padding:16,paddingBottom:100}]}>{children}</ScrollView>
   {mobile&&<View style={s.bottomNav}>{nav.map(([key,icon,label,feature])=><NavItem key={key} route={key} icon={icon} label={label} active={active} compact featureKey={feature}/>)}</View>}
   </View>
 </View>
}
function NavItem({route,icon,label,active,compact,featureKey}:{route:string;icon:keyof typeof Ionicons.glyphMap;label:string;active:string;compact?:boolean;featureKey?:string}){
 const router=useRouter(); const {features}=useFeatureFlags(); const locked=!!featureKey&&!!features[featureKey]?.subscriberOnly; const disabled=!!featureKey&&features[featureKey]?.enabled===false; const go=()=>router.push((route==='index'?'/':`/${route}`) as any);
 return <Pressable onPress={go} style={[compact?s.navCompact:s.navItem,active===route&&s.navActive,disabled&&{opacity:.45}]}><View style={{position:'relative'}}><Ionicons name={icon} size={compact?21:19} color={active===route?C.accent:C.muted}/>{locked&&<View style={{position:'absolute',right:-6,top:-5,backgroundColor:C.gold,borderRadius:6,padding:1}}><Ionicons name="lock-closed" size={7} color="#07111f"/></View>}</View>{!compact&&<Text style={[s.navText,active===route&&{color:C.text}]}>{label}{locked?' · PRO':''}</Text>}{compact&&<Text style={[s.navCompactText,active===route&&{color:C.accent}]}>{label}</Text>}</Pressable>
}

export function ScoreRing({score,size=74}:{score:number;size?:number}){
 return <View style={[s.ring,{width:size,height:size,borderRadius:size/2,borderColor:score>=70?C.accent:score>=50?C.gold:C.red}]}><Text style={[s.ringScore,{fontSize:size*.27}]}>{score}</Text><Text style={s.ringLabel}>/100</Text></View>
}

export function LineChart({data,height=180}:{data:{label:string,value:number}[];height?:number}){
 const {width}=useWindowDimensions(); const w=Math.max(300,Math.min(width-40,760)); const pad=28; const max=Math.max(...data.map(d=>d.value)); const min=Math.min(...data.map(d=>d.value)); const range=Math.max(1,max-min);
 const pts=data.map((d,i)=>({x:pad+(i*(w-pad*2))/Math.max(1,data.length-1),y:18+(1-(d.value-min)/range)*(height-48)}));
 const path=pts.map((p,i)=>`${i?'L':'M'} ${p.x} ${p.y}`).join(' ');
 return <View style={{height,width:'100%',overflow:'hidden'}}><Svg width="100%" height={height} viewBox={`0 0 ${w} ${height}`}><Line x1={pad} y1={height-30} x2={w-pad} y2={height-30} stroke={C.line}/><Path d={path} fill="none" stroke={C.accent} strokeWidth="3"/>{pts.map((p,i)=><React.Fragment key={i}><Circle cx={p.x} cy={p.y} r="4" fill={C.accent}/><SvgText x={p.x} y={height-10} textAnchor="middle" fill={C.muted} fontSize="10">{data[i].label}</SvgText></React.Fragment>)}</Svg></View>
}
export function BarChart({data,height=190}:{data:{label:string;value:number}[];height?:number}){
 const max=Math.max(...data.map(d=>d.value),1); return <View style={{height,justifyContent:'space-around'}}>{data.map((d,i)=><View key={i} style={{flexDirection:'row',alignItems:'center',gap:10}}><Text style={{width:88,color:C.muted,fontSize:11}} numberOfLines={1}>{d.label}</Text><View style={{flex:1,height:12,borderRadius:6,backgroundColor:C.line,overflow:'hidden'}}><View style={{height:'100%',width:`${(d.value/max)*100}%`,backgroundColor:i===0?C.accent:C.accent2,borderRadius:6}}/></View><Text style={{width:42,textAlign:'right',color:C.text,fontWeight:'700',fontSize:11}}>{d.value}</Text></View>)}</View>
}
export function LockedCard({onPress}:{onPress:()=>void}){return <Pressable onPress={onPress} style={[s.locked,shadow]}><View style={s.lockIcon}><Ionicons name="lock-closed" size={22} color={C.gold}/></View><View style={{flex:1}}><Text style={s.lockTitle}>Subscriber intelligence</Text><Text style={s.lockSub}>Blue Ocean discoveries, first-mover playbooks and private opportunity signals are protected.</Text></View><Ionicons name="chevron-forward" size={22} color={C.muted}/></Pressable>}

export function FeatureGate({featureKey,children}:{featureKey:string;children:ReactNode}){
 const router=useRouter(); const {feature,allowed,subscriber,loading}=useFeatureAccess(featureKey);
 if(loading&&!feature)return <AppShell active="account" title="Loading access" subtitle="Checking feature availability"><ActivityIndicator color={C.accent}/></AppShell>;
 if(!feature||!feature.enabled)return <AppShell active="account" title="Feature unavailable" subtitle="This feature is not currently published"><Card><SectionHeader title="Temporarily unavailable" subtitle="See Stats has disabled this feature while the product team updates its intelligence layer."/><Pressable onPress={()=>router.push('/')} style={{marginTop:14,backgroundColor:C.accent,paddingHorizontal:15,paddingVertical:11,borderRadius:11,alignSelf:'flex-start'}}><Text style={{fontWeight:'900',color:'#07111f'}}>Back to overview</Text></Pressable></Card></AppShell>;
 if(feature.subscriberOnly&&!subscriber)return <AppShell active="account" title={feature.label} subtitle="Subscriber intelligence"><LockedCard onPress={()=>router.push('/account' as any)}/><Card><SectionHeader title="Subscriber feature" subtitle={feature.description||'This feature is reserved for active subscribers.'}/><Text style={{color:C.muted,fontSize:12,lineHeight:18,marginTop:9}}>Your administrator can change which See Stats features require a subscription. If you have an active subscription, use the access code sent to your subscriber email.</Text><Pressable onPress={()=>router.push('/subscriber-access' as any)} style={{marginTop:14,backgroundColor:C.accent,paddingHorizontal:15,paddingVertical:11,borderRadius:11,alignSelf:'flex-start'}}><Text style={{fontWeight:'900',color:'#07111f'}}>Manage subscriber access</Text></Pressable></Card></AppShell>;
 return <>{children}</>;
}

export const s=StyleSheet.create({root:{flex:1,backgroundColor:C.bg,flexDirection:'row'},sidebar:{width:245,backgroundColor:'#081523',borderRightWidth:1,borderRightColor:C.line,padding:20},brand:{flexDirection:'row',alignItems:'center',gap:11,marginBottom:36},logo:{width:38,height:38,borderRadius:12,backgroundColor:C.accent,alignItems:'center',justifyContent:'center'},logoText:{fontSize:22,fontWeight:'900',color:'#06151b'},brandText:{fontSize:19,fontWeight:'800',color:C.text},brandSub:{fontSize:8,letterSpacing:1.4,color:C.muted,marginTop:2},navCaption:{fontSize:10,color:C.muted,letterSpacing:1.5,marginBottom:10},navItem:{height:46,borderRadius:12,flexDirection:'row',alignItems:'center',paddingHorizontal:12,gap:12,marginBottom:5},navActive:{backgroundColor:'#11283a'},navText:{color:C.muted,fontSize:14,fontWeight:'600'},sidebarFooter:{borderTopWidth:1,borderTopColor:C.line,paddingTop:16},smallMuted:{color:C.muted,fontSize:11,marginBottom:4},topbar:{height:82,borderBottomWidth:1,borderBottomColor:C.line,flexDirection:'row',alignItems:'center',paddingHorizontal:28},pageTitle:{color:C.text,fontSize:22,fontWeight:'800'},pageSub:{color:C.muted,fontSize:12,marginTop:3},live:{flexDirection:'row',alignItems:'center',gap:7,paddingHorizontal:10,paddingVertical:6,borderRadius:12,backgroundColor:'#10291f'},liveDot:{width:7,height:7,borderRadius:4,backgroundColor:C.accent},liveText:{fontSize:9,color:C.accent,fontWeight:'800',letterSpacing:1},content:{padding:28,maxWidth:1240,width:'100%',alignSelf:'center',gap:18},card:{backgroundColor:C.panel,borderRadius:16,borderWidth:1,borderColor:C.line,padding:18},statTop:{flexDirection:'row',justifyContent:'space-between',alignItems:'center'},label:{color:C.muted,fontSize:11,fontWeight:'700',textTransform:'uppercase',letterSpacing:.7},statValue:{color:C.text,fontSize:27,fontWeight:'800',marginTop:8},delta:{color:C.accent,fontSize:11,marginTop:4,fontWeight:'700'},sectionHead:{flexDirection:'row',alignItems:'center',marginTop:6,marginBottom:0},sectionTitle:{color:C.text,fontSize:17,fontWeight:'800'},sectionSub:{color:C.muted,fontSize:12,marginTop:4},search:{height:42,backgroundColor:C.panel,borderWidth:1,borderColor:C.line,borderRadius:12,flexDirection:'row',alignItems:'center',paddingHorizontal:12,gap:8},searchInput:{flex:1,color:C.text,fontSize:13},pill:{alignSelf:'flex-start',paddingHorizontal:9,paddingVertical:5,borderRadius:20},pillText:{fontSize:10,fontWeight:'800',textTransform:'uppercase'},ring:{borderWidth:6,alignItems:'center',justifyContent:'center'},ringScore:{color:C.text,fontWeight:'900'},ringLabel:{color:C.muted,fontSize:8,marginTop:-2},locked:{backgroundColor:'#1a1914',borderRadius:16,borderWidth:1,borderColor:'#5a4925',padding:16,flexDirection:'row',alignItems:'center',gap:14},lockIcon:{width:44,height:44,borderRadius:13,backgroundColor:'#2b2518',alignItems:'center',justifyContent:'center'},lockTitle:{color:C.text,fontWeight:'800',fontSize:14},lockSub:{color:C.muted,fontSize:11,lineHeight:17,marginTop:4},bottomNav:{position:'absolute',bottom:0,left:0,right:0,height:74,backgroundColor:'#081523',borderTopWidth:1,borderTopColor:C.line,flexDirection:'row',justifyContent:'space-around',paddingTop:7,paddingBottom:5},navCompact:{alignItems:'center',justifyContent:'center',width:72,gap:2},navCompactText:{fontSize:9,color:C.muted,fontWeight:'700'} });
