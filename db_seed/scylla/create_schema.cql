-- Create keyspace (database equivalent in ScyllaDB)
CREATE KEYSPACE IF NOT EXISTS asm3_db
WITH REPLICATION = {
    'class': 'SimpleStrategy',
    'replication_factor': 3
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
    campaign_id int,
    media_type text -- 'photo' or 'video'
);

-- Create campaign_application table
-- Note: ScyllaDB doesn't have ENUMs, so we use text with validation in application layer
CREATE TABLE IF NOT EXISTS campaign_application (
    id int PRIMARY KEY,
    campaign_id int,
    user_id int,
    status text -- 'pending', 'accept', or 'declined'
);

-- Create secondary indexes for foreign key lookups
-- These help with queries that filter by foreign key columns
CREATE INDEX IF NOT EXISTS ON campaign (organizer_id);
CREATE INDEX IF NOT EXISTS ON campaign_requirements (campaign_id);
CREATE INDEX IF NOT EXISTS ON campaign_application (campaign_id);
CREATE INDEX IF NOT EXISTS ON campaign_application (user_id);

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