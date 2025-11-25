-- Create keyspace (database equivalent in ScyllaDB)
CREATE KEYSPACE IF NOT EXISTS asm3_db
WITH REPLICATION = {
    'class': 'SimpleStrategy',
    'replication_factor': 1
};

USE asm3_db;

-- Create user table
CREATE TABLE IF NOT EXISTS user (
    id int PRIMARY KEY,
    username text,
    email text,
    password text
);

-- Create organization table
CREATE TABLE IF NOT EXISTS organization (
    id int PRIMARY KEY,
    name text
);

-- Create campaign table
CREATE TABLE IF NOT EXISTS campaign (
    id int PRIMARY KEY,
    organizer_id int,
    name text
);

-- Create campaign_requirements table
-- Note: ScyllaDB doesn't have ENUMs, so we use text with validation in application layer
CREATE TABLE IF NOT EXISTS campaign_requirements (
    id int PRIMARY KEY,
    count int,
    campaign_id int,
    media_type text -- 'photo' or 'video'
);

CREATE TABLE IF NOT EXISTS campaign_application (
    id int PRIMARY KEY,
    campaign_id int,
    user_id int,
    status text -- 'pending', 'accept', or 'declined'
);

CREATE TABLE IF NOT EXISTS account (
    id uuid PRIMARY KEY,
    username text,
    followers int
);

CREATE TABLE IF NOT EXISTS publication (
    id uuid PRIMARY KEY,
    account_id uuid,
    type text,
    insights text -- json as text
);

CREATE TABLE IF NOT EXISTS user_account (
    id uuid PRIMARY KEY,
    user_id int,
    account_id uuid
);

-- Create secondary indexes for foreign key lookups
-- These help with queries that filter by foreign key columns
CREATE INDEX IF NOT EXISTS ON campaign (organizer_id);
CREATE INDEX IF NOT EXISTS ON campaign_requirements (campaign_id);
CREATE INDEX IF NOT EXISTS ON campaign_application (campaign_id);
CREATE INDEX IF NOT EXISTS ON campaign_application (user_id);
CREATE INDEX IF NOT EXISTS ON publication (account_id);
CREATE INDEX IF NOT EXISTS ON user_account (user_id);
CREATE INDEX IF NOT EXISTS ON user_account (account_id);

-- Create materialized views for efficient querying patterns
-- View for campaigns by organizer
CREATE MATERIALIZED VIEW IF NOT EXISTS campaigns_by_organizer AS
    SELECT * FROM campaign
    WHERE organizer_id IS NOT NULL AND id IS NOT NULL
    PRIMARY KEY (organizer_id, id);

-- View for applications by campaign
CREATE MATERIALIZED VIEW IF NOT EXISTS applications_by_campaign AS
    SELECT * FROM campaign_application
    WHERE campaign_id IS NOT NULL AND id IS NOT NULL
    PRIMARY KEY (campaign_id, id);

-- View for applications by user
CREATE MATERIALIZED VIEW IF NOT EXISTS applications_by_user AS
    SELECT * FROM campaign_application
    WHERE user_id IS NOT NULL AND id IS NOT NULL
    PRIMARY KEY (user_id, id);

-- View for requirements by campaign
CREATE MATERIALIZED VIEW IF NOT EXISTS requirements_by_campaign AS
    SELECT * FROM campaign_requirements
    WHERE campaign_id IS NOT NULL AND id IS NOT NULL
    PRIMARY KEY (campaign_id, id);

-- View for requirements by media type (for filtering by media type)
CREATE MATERIALIZED VIEW IF NOT EXISTS requirements_by_media_type AS
    SELECT * FROM campaign_requirements
    WHERE media_type IS NOT NULL AND id IS NOT NULL
    PRIMARY KEY (media_type, id);

-- New materialized views for account, publication, and user_account
-- View for publications by account
CREATE MATERIALIZED VIEW IF NOT EXISTS publications_by_account AS
    SELECT * FROM publication
    WHERE account_id IS NOT NULL AND id IS NOT NULL
    PRIMARY KEY (account_id, id);

-- View for user_accounts by user_id
CREATE MATERIALIZED VIEW IF NOT EXISTS user_accounts_by_user AS
    SELECT * FROM user_account
    WHERE user_id IS NOT NULL AND id IS NOT NULL
    PRIMARY KEY (user_id, id);

-- View for user_accounts by account_id
CREATE MATERIALIZED VIEW IF NOT EXISTS user_accounts_by_account AS
    SELECT * FROM user_account
    WHERE account_id IS NOT NULL AND id IS NOT NULL
    PRIMARY KEY (account_id, id);

-- Create support key table
CREATE TABLE IF NOT EXISTS sequence_id (
    id int PRIMARY KEY,
    user_sequence int,
    campaign_sequence int,
    organization_sequence int,
    application_sequence int,
    requirements_sequence int
);

-- Insert initial sequence values
INSERT INTO sequence_id (id, user_sequence, campaign_sequence, organization_sequence, application_sequence, requirements_sequence)
VALUES (0, 1, 1, 1, 1, 1);

