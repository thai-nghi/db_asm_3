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
  "media_type" VARCHAR CHECK (media_type IN ('photo', 'video')),
  "count" INTEGER
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

-- Create indexes for better query performance
CREATE INDEX idx_campaign_organizer ON "campaign" ("organizer_id");
CREATE INDEX idx_campaign_requirements_campaign ON "campaign_requirements" ("campaign_id");
CREATE INDEX idx_campaign_application_campaign ON "campaign_application" ("campaign_id");
CREATE INDEX idx_campaign_application_user ON "campaign_application" ("user_id");

INSERT INTO "user" (username, email, password) VALUES
('Alex Chen', 'alex.chen@gmail.com', '12345'),
('Marcus Williams', 'marcus.w@hotmail.com', '12345'),
('Raj Patel', 'raj.patel@proton.me', '12345'),
('Diego Rodriguez', 'diego.rod@gmail.com', '12345'),
('Kenji Nakamura', 'kenji.n@hotmail.com', '12345'),
('Ahmed Hassan', 'ahmed.hassan@proton.me', '12345'),
('Liam O''Connor', 'liam.oconnor@gmail.com', '12345'),
('Vladimir Petrov', 'vlad.petrov@hotmail.com', '12345'),
('Sophia Martinez', 'sophia.m@gmail.com', '12345'),
('Zara Johnson', 'zara.johnson@proton.me', '12345'),
('Mei Lin', 'mei.lin@hotmail.com', '12345'),
('Priya Sharma', 'priya.sharma@gmail.com', '12345'),
('Fatima Al-Rashid', 'fatima.ar@proton.me', '12345'),
('Emma Thompson', 'emma.t@hotmail.com', '12345'),
('Yuki Tanaka', 'yuki.tanaka@gmail.com', '12345'),
('Maria Gonzalez', 'maria.g@proton.me', '12345'),
('Aisha Kone', 'aisha.kone@hotmail.com', '12345'),
('Olivia Kim', 'olivia.kim@gmail.com', '12345'),
('Nadia Volkov', 'nadia.volkov@proton.me', '12345'),
('Jasmine Wright', 'jasmine.w@hotmail.com', '12345');

INSERT INTO organization (name) VALUES
('Stark Industries'),
('Umbrella Corporation'),
('Aperture Science'),
('Wayne Enterprises'),
('Capsule Corporation'),
('Shinra Electric Power Company'),
('Oscorp Industries'),
('Vault-Tec Corporation'),
('Tyrell Corporation'),
('Weyland-Yutani Corporation');

INSERT INTO campaign (organizer_id, name) VALUES
(1, 'Iron Man Suit Beta Testers Wanted!'),
(1, 'Arc Reactor Safety Dance Challenge'),
(2, 'Zombie Apocalypse Survival Influencers'),
(2, 'T-Virus Fashion Week Extravaganza'),
(3, 'Portal Gun Unboxing Videos'),
(3, 'Cake Recipe Testing (Definitely Not a Lie)'),
(4, 'Gotham City Night Photography Contest'),
(4, 'Bat-Signal Yoga Challenge'),
(5, 'Dragon Ball Hunt Vlog Series'),
(5, 'Gravity Chamber Workout Videos'),
(6, 'Mako Energy Aesthetic TikToks'),
(6, 'Midgar Rooftop Parkour Challenge'),
(7, 'Spider Powers Before & After'),
(7, 'Web-Slinging Tutorial Series'),
(8, 'Post-Apocalyptic Fashion Hauls'),
(8, 'Pip-Boy Unboxing & Reviews'),
(9, 'Replicant or Human? Guessing Game'),
(9, 'Cyberpunk Street Style Showcase'),
(10, 'Alien Encounter Reaction Videos'),
(10, 'Space Mining Life Hacks');

INSERT INTO campaign_requirements (campaign_id, media_type, count) VALUES
(1, 'photo', 5),
(1, 'video', 3),
(2, 'video', 8),
(2, 'photo', 2),
(3, 'photo', 10),
(3, 'video', 6),
(4, 'photo', 15),
(4, 'video', 4),
(5, 'video', 5),
(5, 'photo', 8),
(6, 'video', 7),
(6, 'photo', 3),
(7, 'photo', 20),
(8, 'video', 10),
(8, 'photo', 5),
(9, 'video', 12),
(9, 'photo', 6),
(10, 'video', 15),
(10, 'photo', 4),
(11, 'video', 25),
(12, 'video', 8),
(12, 'photo', 12),
(13, 'photo', 10),
(13, 'video', 5),
(14, 'video', 20),
(14, 'photo', 8),
(15, 'photo', 18),
(15, 'video', 6),
(16, 'video', 10),
(16, 'photo', 12),
(17, 'photo', 25),
(17, 'video', 3),
(18, 'photo', 22),
(18, 'video', 7),
(19, 'video', 15),
(19, 'photo', 5),
(20, 'video', 12),
(20, 'photo', 8);

INSERT INTO campaign_application (campaign_id, user_id, status) VALUES
(1, 1, 'pending'),
(5, 1, 'accept'),
(8, 2, 'accept'),
(12, 2, 'pending'),
(1, 3, 'declined'),
(16, 3, 'accept'),
(10, 4, 'accept'),
(8, 4, 'pending'),
(9, 5, 'accept'),
(11, 5, 'accept'),
(17, 6, 'pending'),
(19, 6, 'accept'),
(7, 7, 'accept'),
(14, 7, 'pending'),
(20, 8, 'accept'),
(5, 8, 'declined'),
(4, 9, 'accept'),
(15, 9, 'pending'),
(2, 10, 'accept'),
(8, 10, 'accept'),
(6, 11, 'accept'),
(18, 11, 'pending'),
(14, 12, 'accept'),
(20, 12, 'pending'),
(18, 13, 'accept'),
(4, 13, 'pending'),
(7, 14, 'accept'),
(13, 14, 'declined'),
(9, 15, 'pending'),
(11, 15, 'accept'),
(3, 16, 'accept'),
(15, 16, 'pending'),
(10, 17, 'accept'),
(2, 17, 'pending'),
(16, 18, 'accept'),
(5, 18, 'pending'),
(19, 19, 'accept'),
(3, 19, 'declined'),
(12, 20, 'accept'),
(14, 20, 'pending'),
(1, 5, 'declined'),
(7, 9, 'accept'),
(11, 2, 'pending'),
(17, 14, 'accept'),
(6, 20, 'declined'),
(13, 7, 'accept'),
(19, 12, 'pending'),
(4, 17, 'accept'),
(20, 10, 'declined'),
(15, 6, 'accept');

-- DUCKDB EXCLUSIVE DATA

INSERT INTO "user" (username, email, password) VALUES
('Naruto Uzumaki', 'naruto.u@gmail.com', '12345'),
('Sakura Haruno', 'sakura.h@proton.me', '12345'),
('Goku Son', 'goku.son@hotmail.com', '12345'),
('Bulma Brief', 'bulma.brief@gmail.com', '12345'),
('Edward Elric', 'edward.elric@proton.me', '12345'),
('Winry Rockbell', 'winry.r@hotmail.com', '12345'),
('Ichigo Kurosaki', 'ichigo.k@gmail.com', '12345'),
('Orihime Inoue', 'orihime.i@proton.me', '12345'),
('Link Hero', 'link.hero@hotmail.com', '12345'),
('Zelda Princess', 'zelda.p@gmail.com', '12345'),
('Cloud Strife', 'cloud.strife@proton.me', '12345'),
('Tifa Lockhart', 'tifa.lockhart@hotmail.com', '12345'),
('Geralt Rivia', 'geralt.rivia@gmail.com', '12345'),
('Ciri Cirilla', 'ciri.cirilla@proton.me', '12345'),
('Master Chief', 'master.chief@hotmail.com', '12345'),
('Neo Anderson', 'neo.anderson@gmail.com', '12345'),
('Trinity Matrix', 'trinity.matrix@proton.me', '12345'),
('Luke Skywalker', 'luke.skywalker@hotmail.com', '12345'),
('Leia Organa', 'leia.organa@gmail.com', '12345'),
('Spock Vulcan', 'spock.vulcan@proton.me', '12345'),
('Uhura Nyota', 'uhura.nyota@hotmail.com', '12345'),
('Ripley Ellen', 'ripley.ellen@gmail.com', '12345'),
('Sarah Connor', 'sarah.connor@proton.me', '12345'),
('Kyle Reese', 'kyle.reese@hotmail.com', '12345'),
('John Connor', 'john.connor@gmail.com', '12345');

INSERT INTO organization (name) VALUES
('Konoha Village'),
('Capsule Corp R&D'),
('Amestris State Military'),
('Soul Society'),
('Hyrule Royal Guard'),
('Shinra SOLDIER Program'),
('Kaer Morhen School'),
('UNSC Spartan Program'),
('Zion Resistance'),
('Rebel Alliance'),
('Galactic Empire'),
('Starfleet Academy'),
('United Federation of Planets'),
('Colonial Marines'),
('Tech-Com Resistance');

INSERT INTO campaign (organizer_id, name) VALUES
(11, 'Ninja Academy Training Videos'),
(11, 'Shadow Clone Technique Tutorials'),
(12, 'Dragon Radar Testing Program'),
(12, 'Time Machine Beta Reviews'),
(13, 'Alchemy Circle Drawing Contest'),
(13, 'Philosopher Stone Hunt'),
(14, 'Soul Reaper Training Academy'),
(14, 'Zanpakuto Weapon Reviews'),
(15, 'Triforce Adventure Vlogs'),
(15, 'Hylian Shield Combat Training'),
(16, 'Mako Enhancement Procedures'),
(16, 'Buster Sword Technique Mastery'),
(17, 'Witcher Potion Brewing Guide'),
(17, 'Monster Hunting Expeditions'),
(18, 'Mjolnir Armor Testing'),
(18, 'Covenant War Stories'),
(19, 'Red Pill vs Blue Pill Challenge'),
(19, 'Matrix Glitch Compilation'),
(20, 'Death Star Plans Recovery'),
(20, 'X-Wing Fighter Pilot Training'),
(21, 'Imperial Stormtrooper Recruitment'),
(21, 'Dark Side Force Training'),
(22, 'USS Enterprise Bridge Simulation'),
(22, 'Vulcan Logic Challenge'),
(23, 'Prime Directive Ethics Debate'),
(23, 'Diplomatic Mission Vlogs'),
(24, 'Xenomorph Combat Training'),
(24, 'Space Station Horror Stories'),
(25, 'Anti-Skynet Survival Guide'),
(25, 'Time Travel Paradox Explained');

INSERT INTO campaign_requirements (campaign_id, media_type, count) VALUES
(21, 'video', 20),
(21, 'photo', 10),
(22, 'video', 15),
(22, 'photo', 8),
(23, 'video', 12),
(23, 'photo', 15),
(24, 'video', 8),
(24, 'photo', 20),
(25, 'photo', 30),
(25, 'video', 6),
(26, 'video', 18),
(26, 'photo', 12),
(27, 'video', 25),
(27, 'photo', 15),
(28, 'photo', 35),
(28, 'video', 10),
(29, 'video', 22),
(29, 'photo', 18),
(30, 'video', 16),
(30, 'photo', 12),
(31, 'video', 14),
(31, 'photo', 25),
(32, 'video', 20),
(32, 'photo', 15),
(33, 'video', 18),
(33, 'photo', 22),
(34, 'photo', 20),
(35, 'video', 15),
(35, 'photo', 20),
(36, 'video', 28),
(36, 'photo', 12),
(37, 'video', 10),
(37, 'photo', 30),
(38, 'video', 25),
(38, 'photo', 8),
(39, 'video', 20),
(39, 'photo', 25),
(40, 'video', 22),
(40, 'photo', 18),
(41, 'video', 16),
(41, 'photo', 24),
(42, 'video', 30),
(42, 'photo', 15),
(43, 'video', 18),
(43, 'photo', 22),
(44, 'video', 12),
(44, 'photo', 28),
(45, 'video', 18),
(45, 'photo', 10),
(46, 'video', 20),
(46, 'photo', 22),
(47, 'video', 25),
(47, 'photo', 35),
(48, 'video', 30),
(48, 'photo', 15),
(49, 'video', 24),
(49, 'photo', 16),
(50, 'video', 20),
(50, 'photo', 12);

INSERT INTO campaign_application (campaign_id, user_id, status) VALUES
(21, 21, 'accept'),
(22, 21, 'accept'),
(21, 22, 'pending'),
(27, 22, 'accept'),
(23, 23, 'accept'),
(31, 23, 'pending'),
(24, 24, 'accept'),
(23, 24, 'accept'),
(25, 25, 'accept'),
(26, 25, 'pending'),
(33, 26, 'accept'),
(35, 26, 'pending'),
(27, 27, 'accept'),
(28, 27, 'accept'),


(27, 28, 'pending'),
(45, 28, 'accept'),


(29, 29, 'accept'),
(30, 29, 'accept'),


(29, 30, 'pending'),
(44, 30, 'accept'),


(31, 31, 'accept'),
(32, 31, 'accept'),


(32, 32, 'pending'),
(41, 32, 'accept'),


(33, 33, 'accept'),
(34, 33, 'accept'),


(34, 34, 'pending'),
(50, 34, 'accept'),


(35, 35, 'accept'),
(36, 35, 'accept'),


(37, 36, 'accept'),
(38, 36, 'accept'),


(37, 37, 'pending'),
(38, 37, 'accept'),


(39, 38, 'accept'),
(40, 38, 'accept'),


(39, 39, 'accept'),
(46, 39, 'pending'),


(43, 40, 'accept'),
(44, 40, 'accept'),


(43, 41, 'pending'),
(46, 41, 'accept'),


(47, 42, 'accept'),
(48, 42, 'accept'),


(49, 43, 'accept'),
(50, 43, 'pending'),


(49, 44, 'accept'),
(50, 44, 'accept'),


(49, 45, 'accept'),
(41, 45, 'declined'),


(22, 27, 'accept'),
(25, 33, 'pending'),
(28, 31, 'declined'),
(30, 29, 'accept'),
(34, 43, 'pending'),
(36, 35, 'accept'),
(42, 38, 'declined'),
(44, 36, 'accept'),
(47, 35, 'pending'),
(26, 25, 'accept');