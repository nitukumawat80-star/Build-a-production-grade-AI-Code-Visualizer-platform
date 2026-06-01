CREATE TABLE users (
  id UUID PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  full_name VARCHAR(255),
  hashed_password VARCHAR(255) NOT NULL,
  plan VARCHAR(50) NOT NULL DEFAULT ''free'',
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE analyses (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES users(id),
  language VARCHAR(32) NOT NULL,
  source_code TEXT NOT NULL,
  result_json JSONB NOT NULL,
  complexity_time VARCHAR(120),
  complexity_space VARCHAR(120),
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_analyses_user_created ON analyses(user_id, created_at DESC);
CREATE INDEX idx_analyses_language ON analyses(language);

CREATE TABLE export_jobs (
  id UUID PRIMARY KEY,
  analysis_id UUID NOT NULL REFERENCES analyses(id),
  export_type VARCHAR(16) NOT NULL,
  status VARCHAR(32) NOT NULL,
  artifact_url TEXT,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE usage_events (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES users(id),
  event_type VARCHAR(100) NOT NULL,
  metadata JSONB,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_usage_events_user_created ON usage_events(user_id, created_at DESC);
