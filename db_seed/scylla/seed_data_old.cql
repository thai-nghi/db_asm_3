USE asm3_db;

INSERT INTO sequence_id (id, user_sequence, campaign_sequence, organization_sequence, application_sequence, requirements_sequence)
VALUES (0, 50, 44, 22, 100, 86);

INSERT INTO user (id, username, email, password) VALUES
(1, 'Alex Chen', 'alex.chen@gmail.com', '12345');
INSERT INTO user (id, username, email, password) VALUES
(2, 'Marcus Williams', 'marcus.w@hotmail.com', '12345');
INSERT INTO user (id, username, email, password) VALUES
(3, 'Raj Patel', 'raj.patel@proton.me', '12345');
INSERT INTO user (id, username, email, password) VALUES
(4, 'Diego Rodriguez', 'diego.rod@gmail.com', '12345');
INSERT INTO user (id, username, email, password) VALUES
(5, 'Kenji Nakamura', 'kenji.n@hotmail.com', '12345');
INSERT INTO user (id, username, email, password) VALUES
(6, 'Ahmed Hassan', 'ahmed.hassan@proton.me', '12345');
INSERT INTO user (id, username, email, password) VALUES
(7, 'Liam O''Connor', 'liam.oconnor@gmail.com', '12345');
INSERT INTO user (id, username, email, password) VALUES
(8, 'Vladimir Petrov', 'vlad.petrov@hotmail.com', '12345');

-- Female users from different ethnicities
INSERT INTO user (id, username, email, password) VALUES
(9, 'Sophia Martinez', 'sophia.m@gmail.com', '12345');
INSERT INTO user (id, username, email, password) VALUES
(10, 'Zara Johnson', 'zara.johnson@proton.me', '12345');
INSERT INTO user (id, username, email, password) VALUES
(11, 'Mei Lin', 'mei.lin@hotmail.com', '12345');
INSERT INTO user (id, username, email, password) VALUES
(12, 'Priya Sharma', 'priya.sharma@gmail.com', '12345');
INSERT INTO user (id, username, email, password) VALUES
(13, 'Fatima Al-Rashid', 'fatima.ar@proton.me', '12345');
INSERT INTO user (id, username, email, password) VALUES
(14, 'Emma Thompson', 'emma.t@hotmail.com', '12345');
INSERT INTO user (id, username, email, password) VALUES
(15, 'Yuki Tanaka', 'yuki.tanaka@gmail.com', '12345');
INSERT INTO user (id, username, email, password) VALUES
(16, 'Maria Gonzalez', 'maria.g@proton.me', '12345');
INSERT INTO user (id, username, email, password) VALUES
(17, 'Aisha Kone', 'aisha.kone@hotmail.com', '12345');
INSERT INTO user (id, username, email, password) VALUES
(18, 'Olivia Kim', 'olivia.kim@gmail.com', '12345');
INSERT INTO user (id, username, email, password) VALUES
(19, 'Nadia Volkov', 'nadia.volkov@proton.me', '12345');
INSERT INTO user (id, username, email, password) VALUES
(20, 'Jasmine Wright', 'jasmine.w@hotmail.com', '12345');

-- Insert 10 organizations from pop culture
INSERT INTO organization (id, name) VALUES (1, 'Stark Industries');
INSERT INTO organization (id, name) VALUES (2, 'Umbrella Corporation');
INSERT INTO organization (id, name) VALUES (3, 'Aperture Science');
INSERT INTO organization (id, name) VALUES (4, 'Wayne Enterprises');
INSERT INTO organization (id, name) VALUES (5, 'Capsule Corporation');
INSERT INTO organization (id, name) VALUES (6, 'Shinra Electric Power Company');
INSERT INTO organization (id, name) VALUES (7, 'Oscorp Industries');
INSERT INTO organization (id, name) VALUES (8, 'Vault-Tec Corporation');
INSERT INTO organization (id, name) VALUES (9, 'Tyrell Corporation');
INSERT INTO organization (id, name) VALUES (10, 'Weyland-Yutani Corporation');

-- Insert 20 campaigns (2 per organization)
INSERT INTO campaign (id, organizer_id, name) VALUES (1, 1, 'Iron Man Suit Beta Testers Wanted!');
INSERT INTO campaign (id, organizer_id, name) VALUES (2, 1, 'Arc Reactor Safety Dance Challenge');
INSERT INTO campaign (id, organizer_id, name) VALUES (3, 2, 'Zombie Apocalypse Survival Influencers');
INSERT INTO campaign (id, organizer_id, name) VALUES (4, 2, 'T-Virus Fashion Week Extravaganza');
INSERT INTO campaign (id, organizer_id, name) VALUES (5, 3, 'Portal Gun Unboxing Videos');
INSERT INTO campaign (id, organizer_id, name) VALUES (6, 3, 'Cake Recipe Testing (Definitely Not a Lie)');
INSERT INTO campaign (id, organizer_id, name) VALUES (7, 4, 'Gotham City Night Photography Contest');
INSERT INTO campaign (id, organizer_id, name) VALUES (8, 4, 'Bat-Signal Yoga Challenge');
INSERT INTO campaign (id, organizer_id, name) VALUES (9, 5, 'Dragon Ball Hunt Vlog Series');
INSERT INTO campaign (id, organizer_id, name) VALUES (10, 5, 'Gravity Chamber Workout Videos');
INSERT INTO campaign (id, organizer_id, name) VALUES (11, 6, 'Mako Energy Aesthetic TikToks');
INSERT INTO campaign (id, organizer_id, name) VALUES (12, 6, 'Midgar Rooftop Parkour Challenge');
INSERT INTO campaign (id, organizer_id, name) VALUES (13, 7, 'Spider Powers Before & After');
INSERT INTO campaign (id, organizer_id, name) VALUES (14, 7, 'Web-Slinging Tutorial Series');
INSERT INTO campaign (id, organizer_id, name) VALUES (15, 8, 'Post-Apocalyptic Fashion Hauls');
INSERT INTO campaign (id, organizer_id, name) VALUES (16, 8, 'Pip-Boy Unboxing & Reviews');
INSERT INTO campaign (id, organizer_id, name) VALUES (17, 9, 'Replicant or Human? Guessing Game');
INSERT INTO campaign (id, organizer_id, name) VALUES (18, 9, 'Cyberpunk Street Style Showcase');
INSERT INTO campaign (id, organizer_id, name) VALUES (19, 10, 'Alien Encounter Reaction Videos');
INSERT INTO campaign (id, organizer_id, name) VALUES (20, 10, 'Space Mining Life Hacks');

INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (1, 1, 'photo', 5);
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (2, 1, 'video', 3);
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (3, 2, 'video', 8);
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (4, 2, 'photo', 2);
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (5, 3, 'photo', 10);
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (6, 3, 'video', 6);

-- T-Virus Fashion Week
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (7, 4, 'photo', 15);
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (8, 4, 'video', 4);

-- Portal Gun Unboxing
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (9, 5, 'video', 5);
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (10, 5, 'photo', 8);

-- Cake Recipe Testing
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (11, 6, 'video', 7);
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (12, 6, 'photo', 3);

-- Gotham Night Photography
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (13, 7, 'photo', 20);

-- Bat-Signal Yoga
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (14, 8, 'video', 10);
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (15, 8, 'photo', 5);

-- Dragon Ball Hunt
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (16, 9, 'video', 12);
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (17, 9, 'photo', 6);

-- Gravity Chamber Workout
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (18, 10, 'video', 15);
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (19, 10, 'photo', 4);

-- Mako Energy TikToks
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (20, 11, 'video', 25);

-- Midgar Parkour
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (21, 12, 'video', 8);
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (22, 12, 'photo', 12);

-- Spider Powers Before/After
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (23, 13, 'photo', 10);
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (24, 13, 'video', 5);

-- Web-Slinging Tutorials
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (25, 14, 'video', 20);
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (26, 14, 'photo', 8);

-- Post-Apocalyptic Fashion
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (27, 15, 'photo', 18);
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (28, 15, 'video', 6);

-- Pip-Boy Reviews
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (29, 16, 'video', 10);
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (30, 16, 'photo', 12);

-- Replicant Guessing Game
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (31, 17, 'photo', 25);
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (32, 17, 'video', 3);

-- Cyberpunk Street Style
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (33, 18, 'photo', 22);
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (34, 18, 'video', 7);

-- Alien Encounter Reactions
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (35, 19, 'video', 15);
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (36, 19, 'photo', 5);

-- Space Mining Life Hacks
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (37, 20, 'video', 12);
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (38, 20, 'photo', 8);

-- Insert campaign applications (each user applies to at least 1 campaign)
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (1, 1, 1, 'pending');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (2, 5, 1, 'accept');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (3, 8, 2, 'accept');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (4, 12, 2, 'pending');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (5, 1, 3, 'declined');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (6, 16, 3, 'accept');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (7, 10, 4, 'accept');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (8, 8, 4, 'pending');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (9, 9, 5, 'accept');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (10, 11, 5, 'accept');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (11, 17, 6, 'pending');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (12, 19, 6, 'accept');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (13, 7, 7, 'accept');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (14, 14, 7, 'pending');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (15, 20, 8, 'accept');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (16, 5, 8, 'declined');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (17, 4, 9, 'accept');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (18, 15, 9, 'pending');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (19, 2, 10, 'accept');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (20, 8, 10, 'accept');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (21, 6, 11, 'accept');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (22, 18, 11, 'pending');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (23, 14, 12, 'accept');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (24, 20, 12, 'pending');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (25, 18, 13, 'accept');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (26, 4, 13, 'pending');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (27, 7, 14, 'accept');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (28, 13, 14, 'declined');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (29, 9, 15, 'pending');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (30, 11, 15, 'accept');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (31, 3, 16, 'accept');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (32, 15, 16, 'pending');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (33, 10, 17, 'accept');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (34, 2, 17, 'pending');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (35, 16, 18, 'accept');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (36, 5, 18, 'pending');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (37, 19, 19, 'accept');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (38, 3, 19, 'declined');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (39, 12, 20, 'accept');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (40, 14, 20, 'pending');

-- Additional applications for more engagement
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (41, 1, 5, 'declined');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (42, 7, 9, 'accept');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (43, 11, 2, 'pending');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (44, 17, 14, 'accept');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (45, 6, 20, 'declined');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (46, 13, 7, 'accept');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (47, 19, 12, 'pending');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (48, 4, 17, 'accept');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (49, 20, 10, 'declined');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (50, 15, 6, 'accept');

-- Insert 30 additional diverse users (IDs 21-50) - ScyllaDB gets the most users!
INSERT INTO user (id, username, email, password) VALUES (21, 'Monkey D. Luffy', 'luffy.monkey@gmail.com', '12345');
INSERT INTO user (id, username, email, password) VALUES (22, 'Roronoa Zoro', 'zoro.roronoa@proton.me', '12345');
INSERT INTO user (id, username, email, password) VALUES (23, 'Nami Navigator', 'nami.navigator@hotmail.com', '12345');
INSERT INTO user (id, username, email, password) VALUES (24, 'Sanji Vinsmoke', 'sanji.vinsmoke@gmail.com', '12345');
INSERT INTO user (id, username, email, password) VALUES (25, 'Tony Chopper', 'tony.chopper@proton.me', '12345');
INSERT INTO user (id, username, email, password) VALUES (26, 'Nico Robin', 'nico.robin@hotmail.com', '12345');
INSERT INTO user (id, username, email, password) VALUES (27, 'Franky Cutty', 'franky.cutty@gmail.com', '12345');
INSERT INTO user (id, username, email, password) VALUES (28, 'Brook Soul', 'brook.soul@proton.me', '12345');
INSERT INTO user (id, username, email, password) VALUES (29, 'Jinbei Fishman', 'jinbei.fishman@hotmail.com', '12345');
INSERT INTO user (id, username, email, password) VALUES (30, 'Portgas Ace', 'portgas.ace@gmail.com', '12345');

-- Marvel/DC inspired users
INSERT INTO user (id, username, email, password) VALUES (31, 'Peter Parker', 'peter.parker@proton.me', '12345');
INSERT INTO user (id, username, email, password) VALUES (32, 'Bruce Wayne', 'bruce.wayne@hotmail.com', '12345');
INSERT INTO user (id, username, email, password) VALUES (33, 'Diana Prince', 'diana.prince@gmail.com', '12345');
INSERT INTO user (id, username, email, password) VALUES (34, 'Clark Kent', 'clark.kent@proton.me', '12345');
INSERT INTO user (id, username, email, password) VALUES (35, 'Natasha Romanoff', 'natasha.romanoff@hotmail.com', '12345');
INSERT INTO user (id, username, email, password) VALUES (36, 'Steve Rogers', 'steve.rogers@gmail.com', '12345');
INSERT INTO user (id, username, email, password) VALUES (37, 'Wanda Maximoff', 'wanda.maximoff@proton.me', '12345');
INSERT INTO user (id, username, email, password) VALUES (38, 'Victor Stone', 'victor.stone@hotmail.com', '12345');
INSERT INTO user (id, username, email, password) VALUES (39, 'Barry Allen', 'barry.allen@gmail.com', '12345');
INSERT INTO user (id, username, email, password) VALUES (40, 'Arthur Curry', 'arthur.curry@proton.me', '12345');

-- Anime/Gaming mix users
INSERT INTO user (id, username, email, password) VALUES (41, 'Saitama Hero', 'saitama.hero@hotmail.com', '12345');
INSERT INTO user (id, username, email, password) VALUES (42, 'Genos Cyborg', 'genos.cyborg@gmail.com', '12345');
INSERT INTO user (id, username, email, password) VALUES (43, 'Tanjiro Kamado', 'tanjiro.kamado@proton.me', '12345');
INSERT INTO user (id, username, email, password) VALUES (44, 'Nezuko Kamado', 'nezuko.kamado@hotmail.com', '12345');
INSERT INTO user (id, username, email, password) VALUES (45, 'Senku Ishigami', 'senku.ishigami@gmail.com', '12345');
INSERT INTO user (id, username, email, password) VALUES (46, 'Yuzuriha Ogawa', 'yuzuriha.ogawa@proton.me', '12345');
INSERT INTO user (id, username, email, password) VALUES (47, 'Rimuru Tempest', 'rimuru.tempest@hotmail.com', '12345');
INSERT INTO user (id, username, email, password) VALUES (48, 'Shion Ogre', 'shion.ogre@gmail.com', '12345');
INSERT INTO user (id, username, email, password) VALUES (49, 'Kirito Kazuto', 'kirito.kazuto@proton.me', '12345');
INSERT INTO user (id, username, email, password) VALUES (50, 'Asuna Yuuki', 'asuna.yuuki@hotmail.com', '12345');

-- Insert 12 additional organizations (IDs 11-22)
INSERT INTO organization (id, name) VALUES (11, 'Straw Hat Pirates');
INSERT INTO organization (id, name) VALUES (12, 'World Government Marines');
INSERT INTO organization (id, name) VALUES (13, 'Avengers Initiative');
INSERT INTO organization (id, name) VALUES (14, 'Justice League');
INSERT INTO organization (id, name) VALUES (15, 'S.H.I.E.L.D. Agency');
INSERT INTO organization (id, name) VALUES (16, 'X-Men School');
INSERT INTO organization (id, name) VALUES (17, 'Hero Association');
INSERT INTO organization (id, name) VALUES (18, 'Demon Slayer Corps');
INSERT INTO organization (id, name) VALUES (19, 'Kingdom of Science');
INSERT INTO organization (id, name) VALUES (20, 'Tempest Federation');
INSERT INTO organization (id, name) VALUES (21, 'Sword Art Online Guild');
INSERT INTO organization (id, name) VALUES (22, 'Virtual Reality Research');

-- Insert 24 additional campaigns (2 per new organization)
INSERT INTO campaign (id, organizer_id, name) VALUES (21, 11, 'Grand Line Adventure Chronicles');
INSERT INTO campaign (id, organizer_id, name) VALUES (22, 11, 'Devil Fruit Power Showcase');

INSERT INTO campaign (id, organizer_id, name) VALUES (23, 12, 'Marine Justice Training Program');
INSERT INTO campaign (id, organizer_id, name) VALUES (24, 12, 'Pirate Bounty Hunter Challenge');

INSERT INTO campaign (id, organizer_id, name) VALUES (25, 13, 'Superhero Team-Up Videos');
INSERT INTO campaign (id, organizer_id, name) VALUES (26, 13, 'Marvel Universe Tour Guide');

INSERT INTO campaign (id, organizer_id, name) VALUES (27, 14, 'DC Multiverse Exploration');
INSERT INTO campaign (id, organizer_id, name) VALUES (28, 14, 'Superhero Ethics Discussion');

INSERT INTO campaign (id, organizer_id, name) VALUES (29, 15, 'Espionage Mission Tutorials');
INSERT INTO campaign (id, organizer_id, name) VALUES (30, 15, 'Spy Gadget Review Series');

INSERT INTO campaign (id, organizer_id, name) VALUES (31, 16, 'Mutant Powers Training Academy');
INSERT INTO campaign (id, organizer_id, name) VALUES (32, 16, 'Xavier School Daily Life Vlogs');

INSERT INTO campaign (id, organizer_id, name) VALUES (33, 17, 'Hero Ranking Battle Royale');
INSERT INTO campaign (id, organizer_id, name) VALUES (34, 17, 'Monster Disaster Alert System');

INSERT INTO campaign (id, organizer_id, name) VALUES (35, 18, 'Breathing Technique Mastery');
INSERT INTO campaign (id, organizer_id, name) VALUES (36, 18, 'Demon Hunting Night Raids');

INSERT INTO campaign (id, organizer_id, name) VALUES (37, 19, 'Stone Age Science Experiments');
INSERT INTO campaign (id, organizer_id, name) VALUES (38, 19, 'Civilization Rebuilding Project');

INSERT INTO campaign (id, organizer_id, name) VALUES (39, 20, 'Slime Nation Building Guide');
INSERT INTO campaign (id, organizer_id, name) VALUES (40, 20, 'Monster Evolution Documentaries');

INSERT INTO campaign (id, organizer_id, name) VALUES (41, 21, 'Virtual Reality Gaming Reviews');
INSERT INTO campaign (id, organizer_id, name) VALUES (42, 21, 'MMORPG Strategy Tutorials');

INSERT INTO campaign (id, organizer_id, name) VALUES (43, 22, 'Future Gaming Technology');
INSERT INTO campaign (id, organizer_id, name) VALUES (44, 22, 'VR World Development Diary');

-- Insert campaign requirements for campaigns 21-44
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (39, 21, 'video', 25);
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (40, 21, 'photo', 15);

INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (41, 22, 'video', 12);
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (42, 22, 'photo', 30);

INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (43, 23, 'video', 20);
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (44, 23, 'photo', 18);

INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (45, 24, 'video', 16);
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (46, 24, 'photo', 22);

INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (47, 25, 'video', 30);
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (48, 25, 'photo', 20);

INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (49, 26, 'video', 18);
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (50, 26, 'photo', 25);

INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (51, 27, 'video', 22);
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (52, 27, 'photo', 28);

INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (53, 28, 'video', 15);
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (54, 28, 'photo', 12);

INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (55, 29, 'video', 24);
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (56, 29, 'photo', 16);

INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (57, 30, 'video', 14);
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (58, 30, 'photo', 35);

INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (59, 31, 'video', 28);
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (60, 31, 'photo', 20);

INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (61, 32, 'video', 20);
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (62, 32, 'photo', 15);

INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (63, 33, 'video', 35);
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (64, 33, 'photo', 10);

INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (65, 34, 'video', 18);
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (66, 34, 'photo', 25);

INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (67, 35, 'video', 26);
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (68, 35, 'photo', 18);

INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (69, 36, 'video', 30);
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (70, 36, 'photo', 22);

INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (71, 37, 'video', 20);
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (72, 37, 'photo', 30);

INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (73, 38, 'video', 25);
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (74, 38, 'photo', 20);

INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (75, 39, 'video', 22);
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (76, 39, 'photo', 28);

INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (77, 40, 'video', 18);
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (78, 40, 'photo', 24);

INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (79, 41, 'video', 32);
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (80, 41, 'photo', 12);

INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (81, 42, 'video', 24);
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (82, 42, 'photo', 20);

INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (83, 43, 'video', 16);
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (84, 43, 'photo', 25);

INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (85, 44, 'video', 28);
INSERT INTO campaign_requirements (id, campaign_id, media_type, count) VALUES (86, 44, 'photo', 18);

-- Insert campaign applications for ScyllaDB users (51-100)
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (51, 21, 21, 'accept');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (52, 22, 21, 'accept');

INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (53, 21, 22, 'pending');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (54, 23, 22, 'accept');

INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (55, 21, 23, 'accept');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (56, 24, 23, 'pending');

INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (57, 22, 24, 'accept');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (58, 21, 24, 'declined');

INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (59, 25, 25, 'accept');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (60, 31, 25, 'pending');

INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (61, 26, 26, 'accept');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (62, 27, 26, 'pending');

INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (63, 25, 27, 'accept');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (64, 28, 27, 'accept');

INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (65, 29, 28, 'accept');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (66, 30, 28, 'pending');

INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (67, 21, 29, 'accept');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (68, 23, 29, 'declined');

INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (69, 22, 30, 'accept');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (70, 25, 30, 'pending');

INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (71, 25, 31, 'accept');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (72, 26, 31, 'accept');

INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (73, 27, 32, 'accept');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (74, 28, 32, 'pending');

INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (75, 27, 33, 'accept');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (76, 28, 33, 'accept');

INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (77, 27, 34, 'accept');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (78, 25, 34, 'pending');

INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (79, 29, 35, 'accept');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (80, 30, 35, 'accept');

INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (81, 25, 36, 'accept');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (82, 29, 36, 'pending');

INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (83, 31, 37, 'accept');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (84, 32, 37, 'accept');

INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (85, 27, 38, 'accept');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (86, 28, 38, 'pending');

INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (87, 27, 39, 'accept');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (88, 25, 39, 'declined');

INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (89, 27, 40, 'accept');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (90, 26, 40, 'pending');

INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (91, 33, 41, 'accept');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (92, 34, 41, 'accept');

INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (93, 33, 42, 'pending');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (94, 34, 42, 'accept');

INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (95, 35, 43, 'accept');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (96, 36, 43, 'accept');

INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (97, 35, 44, 'pending');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (98, 36, 44, 'accept');

INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (99, 37, 45, 'accept');
INSERT INTO campaign_application (id, campaign_id, user_id, status) VALUES (100, 38, 45, 'accept');