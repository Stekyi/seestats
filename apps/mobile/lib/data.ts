import analysisJson from '../../..//data/ghana-analysis.json';
import discoveriesJson from '../../..//data/discoveries.json';
import { Analysis, Discovery, Country } from './types';

export const analysis = analysisJson as Analysis;
export const discoveries = discoveriesJson as Discovery[];
export const countries: Country[] = [
  {code:'GHA',name:'Ghana',enabled:true,sources:[
    {name:'Ghana Statistical Service',url:'https://statsghana.gov.gh/'},
    {name:'UN Comtrade',url:'https://comtradeplus.un.org/'},
    {name:'FAOSTAT',url:'https://www.fao.org/faostat/'},
    {name:'World Bank',url:'https://data.worldbank.org/country/ghana'}
  ]},
  {code:'NGA',name:'Nigeria',enabled:false,sources:[]}, {code:'KEN',name:'Kenya',enabled:false,sources:[]},
  {code:'CIV',name:"Côte d'Ivoire",enabled:false,sources:[]}, {code:'SEN',name:'Senegal',enabled:false,sources:[]},
  {code:'RWA',name:'Rwanda',enabled:false,sources:[]}
];

export const weeklyScores = [
  {week:'May 15',score:78}, {week:'May 22',score:81}, {week:'May 29',score:80}, {week:'Jun 5',score:83},
  {week:'Jun 12',score:82}, {week:'Jun 19',score:84}, {week:'Jul 3',score:86}, {week:'Jul 17',score:84}
];
export const priceTrend = [
  {year:'2021',value:12},{year:'2022',value:15},{year:'2023',value:18},{year:'2024',value:22},{year:'2025E',value:26}
];
