CREATE TABLE IF NOT EXISTS "user" (
  "id" INTEGER PRIMARY KEY,
  "username" VARCHAR,
  "email" VARCHAR,
  "password" VARCHAR
);

CREATE TABLE IF NOT EXISTS "organization" (
  "id" INTEGER PRIMARY KEY,
  "name" VARCHAR
);

CREATE TABLE IF NOT EXISTS "campaign" (
  "id" INTEGER PRIMARY KEY,
  "organizer_id" INTEGER,
  "name" VARCHAR
);

CREATE TABLE IF NOT EXISTS "campaign_requirements" (
  "id" INTEGER PRIMARY KEY,
  "campaign_id" INTEGER,
  "media_type" VARCHAR CHECK (media_type IN ('photo', 'video'))
);

CREATE TABLE IF NOT EXISTS "campaign_application" (
  "id" INTEGER PRIMARY KEY,
  "campaign_id" INTEGER,
  "user_id" INTEGER,
  "status" VARCHAR CHECK (status IN ('pending', 'accept', 'declined'))
);

CREATE INDEX IF NOT EXISTS idx_campaign_organizer ON "campaign" ("organizer_id");
CREATE INDEX IF NOT EXISTS idx_campaign_requirements_campaign ON "campaign_requirements" ("campaign_id");
CREATE INDEX IF NOT EXISTS idx_campaign_application_campaign ON "campaign_application" ("campaign_id");
CREATE INDEX IF NOT EXISTS idx_campaign_application_user ON "campaign_application" ("user_id");