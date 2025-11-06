CREATE TYPE "media_type" AS ENUM (
  'photo',
  'video'
);

CREATE TYPE "application_status" AS ENUM (
  'pending',
  'accept',
  'declined'
);

CREATE TABLE "user" (
  "id" int PRIMARY KEY,
  "username" varchar,
  "email" varchar,
  "password" varchar
);

CREATE TABLE "organization" (
  "id" int PRIMARY KEY,
  "name" varchar
);

CREATE TABLE "campaign" (
  "id" int PRIMARY KEY,
  "organizer_id" int,
  "name" varchar
);

CREATE TABLE "campaign_requirements" (
  "id" int PRIMARY KEY,
  "campaign_id" int,
  "media_type" media_type
);

CREATE TABLE "campaign_application" (
  "id" int PRIMARY KEY,
  "campaign_id" int,
  "user_id" int,
  "status" application_status
);

ALTER TABLE "campaign_requirements" ADD CONSTRAINT "campaign_requirements_ref" FOREIGN KEY ("campaign_id") REFERENCES "campaign" ("id");

ALTER TABLE "campaign" ADD CONSTRAINT "campaign_organizer" FOREIGN KEY ("organizer_id") REFERENCES "organization" ("id");

ALTER TABLE "campaign_application" ADD CONSTRAINT "application_campaign" FOREIGN KEY ("campaign_id") REFERENCES "campaign" ("id");

ALTER TABLE "campaign_application" ADD CONSTRAINT "application_user" FOREIGN KEY ("user_id") REFERENCES "user" ("id");
