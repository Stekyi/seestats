export type Direction = 'import_opportunity' | 'export_opportunity';
export type Opportunity = {
  commodity: string; type: Direction; score: number; margin_pct: number; margin_flag: 'green'|'yellow'|'red';
  ghana_import_usd_m?: number; ghana_export_usd_m?: number; yoy_growth_pct: number;
  best_supplier?: string; best_price_usd_mt?: number; all_suppliers?: {country:string;price_usd_mt:number;distance:string}[];
  best_market?: string; market_demand_growth_pct?: number; price_premium?: string;
  all_markets?: {country:string;demand_growth_pct:number;price_premium:string}[];
  ghana_producer_price_usd_mt?: number; est_order_qty_mt:number; est_order_ghc:number; budget_fit:boolean;
  score_breakdown: Record<string,number>;
};
export type Discovery = {
  id:string; name:string; category:string; direction:string; blue_ocean_tier:string; tagline:string;
  total_score:number; market_saturation_score:number; ghana_advantage_score:number; demand_trajectory_score:number;
  entry_barrier_score:number; first_mover_score:number; ghana_producer_price_usd_kg?:number;
  estimated_export_price_usd_kg?:number; gross_margin_pct:number; starting_order_ghc:number; starting_qty_kg?:number;
  why_undiscovered:string; global_market_size_usd:string; demand_cagr_pct:number; trend_keywords:string[];
  price_trend:Record<string,number>; target_buyers:{name:string;type:string;approach:string}[];
  first_mover_actions:string[]; risks:string[];
};
export type Analysis = {
  analysis_date:string; budget_ghc:number; budget_usd:number; import_opportunities:Opportunity[];
  export_opportunities:Opportunity[]; top_5_overall:Opportunity[]; supply_demand_graph:any; summary:any;
};
export type Country = {code:string;name:string;enabled:boolean;sources:{name:string;url:string}[]};
