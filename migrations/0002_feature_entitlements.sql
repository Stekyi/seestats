CREATE TABLE IF NOT EXISTS feature_flags (
  feature_key TEXT PRIMARY KEY,
  label TEXT NOT NULL,
  description TEXT,
  enabled INTEGER NOT NULL DEFAULT 1,
  subscriber_only INTEGER NOT NULL DEFAULT 0,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT OR IGNORE INTO feature_flags(feature_key,label,description,enabled,subscriber_only) VALUES
 ('opportunities','Opportunity Radar','Ranked investment and trade opportunities',1,0),
 ('trends','Trend Intelligence','Historical and current trend analysis',1,0),
 ('country','Country Intelligence','Country selection, coverage and source context',1,0),
 ('checklist','Investment Diligence','Diligence checklist for an opportunity',1,0),
 ('roadmap','Business Roadmap','Step-by-step execution roadmap',1,0),
 ('customers','Buyer & Partner Directory','Buyer, supplier and partner intelligence',1,0),
 ('project_board','Project Board','Lightweight execution board',1,0),
 ('pipeline','Data Pipeline','Source freshness and pipeline status',1,0),
 ('first_mover','First-Mover Strategy','Private first-mover launch playbooks',1,1),
 ('blue_ocean','Blue Ocean','Private discovery and blue-ocean opportunities',1,1);
CREATE INDEX IF NOT EXISTS idx_feature_flags_enabled ON feature_flags(enabled);
