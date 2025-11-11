-- DuckDB initialization script
-- Note: DuckDB doesn't support ENUMs, so we use VARCHAR with CHECK constraints

-- Create user table
CREATE SEQUENCE user_id_seq START 1;
CREATE TABLE "user" (
  "id" INTEGER PRIMARY KEY DEFAULT nextval('user_id_seq'),
  "username" VARCHAR,
  "email" VARCHAR,
  "password" VARCHAR
);


-- Create organization table
CREATE SEQUENCE organization_id_seq START 1;
CREATE TABLE "organization" (
  "id" INTEGER PRIMARY KEY DEFAULT nextval('organization_id_seq'),
  "name" VARCHAR
);

-- Create campaign table
CREATE SEQUENCE campaign_id_seq START 1;
CREATE TABLE "campaign" (
  "id" INTEGER PRIMARY KEY DEFAULT nextval('campaign_id_seq'),
  "organizer_id" INTEGER,
  "name" VARCHAR
);

-- Create campaign_requirements table
-- Using VARCHAR with CHECK constraint instead of ENUM
CREATE SEQUENCE campaign_requirements_id_seq START 1;
CREATE TABLE "campaign_requirements" (
  "id" INTEGER PRIMARY KEY DEFAULT nextval('campaign_requirements_id_seq'),
  "campaign_id" INTEGER,
  "media_type" VARCHAR CHECK (media_type IN ('photo', 'video'))
);

-- Create campaign_application table
-- Using VARCHAR with CHECK constraint instead of ENUM
CREATE SEQUENCE campaign_application_id_seq START 1;
CREATE TABLE "campaign_application" (
  "id" INTEGER PRIMARY KEY DEFAULT nextval('campaign_application_id_seq'),
  "campaign_id" INTEGER,
  "user_id" INTEGER,
  "status" VARCHAR CHECK (status IN ('pending', 'accept', 'declined'))
);

-- Note: DuckDB supports foreign key constraints but they are not enforced by default
-- Adding foreign key constraints for referential integrity documentation
-- These will be validated at query time if foreign key checking is enabled

-- Foreign key constraints (not enforced by default in DuckDB)
-- ALTER TABLE "campaign_requirements" ADD CONSTRAINT "campaign_requirements_ref" 
--   FOREIGN KEY ("campaign_id") REFERENCES "campaign" ("id");

-- ALTER TABLE "campaign" ADD CONSTRAINT "campaign_organizer" 
--   FOREIGN KEY ("organizer_id") REFERENCES "organization" ("id");

-- ALTER TABLE "campaign_application" ADD CONSTRAINT "application_campaign" 
--   FOREIGN KEY ("campaign_id") REFERENCES "campaign" ("id");

-- ALTER TABLE "campaign_application" ADD CONSTRAINT "application_user" 
--   FOREIGN KEY ("user_id") REFERENCES "user" ("id");

-- Create indexes for better query performance
CREATE INDEX idx_campaign_organizer ON "campaign" ("organizer_id");
CREATE INDEX idx_campaign_requirements_campaign ON "campaign_requirements" ("campaign_id");
CREATE INDEX idx_campaign_application_campaign ON "campaign_application" ("campaign_id");
CREATE INDEX idx_campaign_application_user ON "campaign_application" ("user_id");
