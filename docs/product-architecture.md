# See Stats product architecture

## Core destination

See Stats is intended to become a destination for investors, operators and trade businesses to answer one question: **where is the data saying capital may be misallocated or demand is moving?**

The product should progressively add:

- Country scorecards
- Sector heatmaps
- Import dependency and substitution signals
- Export competitiveness
- Global demand growth
- Price / volume divergence
- Currency and macro overlays
- Regulatory / logistics risk
- Investor watchlists and saved theses
- Historical backtesting of opportunity scores
- Alerts when a score changes materially
- Source-level provenance and freshness

## Opportunity model

A country-specific adapter produces a common `Opportunity` contract. The UI never needs to know how a country was calculated. This is the key scaling mechanism.

Suggested future score dimensions:

`Opportunity = f(market_size, growth, margin, import_dependency, export_competitiveness, price_signal, capital_fit, logistics, regulation, source_confidence)`

Scores should be accompanied by a **confidence score** and a **source freshness score** so a large but stale market number cannot look identical to a current high-confidence signal.

## Premium boundary

The public tier should show enough evidence to make the product useful:

- country overview
- headline indicators
- selected opportunity rankings
- source dates
- methodology

The subscriber tier should add the expensive research:

- Blue Ocean discoveries
- first-mover playbooks
- proprietary cross-source scoring
- saved theses
- deeper market maps
- alerts
- investor-ready diligence packs

## Trust / compliance direction

The application should consistently call outputs **signals**, **rankings** or **decision-support**, not guaranteed returns or investment recommendations. Each report should expose source, retrieval date, methodology version and material assumptions.
