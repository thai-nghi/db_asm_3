-- Seed data for PostgreSQL/DuckDB

-- Insert 20 diverse users
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
-- Stark Industries campaigns
(1, 'Iron Man Suit Beta Testers Wanted!'),
(1, 'Arc Reactor Safety Dance Challenge'),

-- Umbrella Corporation campaigns
(2, 'Zombie Apocalypse Survival Influencers'),
(2, 'T-Virus Fashion Week Extravaganza'),

-- Aperture Science campaigns
(3, 'Portal Gun Unboxing Videos'),
(3, 'Cake Recipe Testing (Definitely Not a Lie)'),

-- Wayne Enterprises campaigns  
(4, 'Gotham City Night Photography Contest'),
(4, 'Bat-Signal Yoga Challenge'),

-- Capsule Corporation campaigns
(5, 'Dragon Ball Hunt Vlog Series'),
(5, 'Gravity Chamber Workout Videos'),

-- Shinra campaigns
(6, 'Mako Energy Aesthetic TikToks'),
(6, 'Midgar Rooftop Parkour Challenge'),

-- Oscorp campaigns
(7, 'Spider Powers Before & After'),
(7, 'Web-Slinging Tutorial Series'),

-- Vault-Tec campaigns
(8, 'Post-Apocalyptic Fashion Hauls'),
(8, 'Pip-Boy Unboxing & Reviews'),

-- Tyrell Corporation campaigns
(9, 'Replicant or Human? Guessing Game'),
(9, 'Cyberpunk Street Style Showcase'),

-- Weyland-Yutani campaigns
(10, 'Alien Encounter Reaction Videos'),
(10, 'Space Mining Life Hacks');

-- Insert campaign requirements
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

-- Insert campaign applications
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

-- POSTGRESQL EXCLUSIVE DATA - Additional 20 users, 10 orgs, 20 campaigns

INSERT INTO "user" (username, email, password) VALUES
('Chen Wei', 'chen.wei@gmail.com', '12345'),
('Muhammad Ali', 'muhammad.ali@proton.me', '12345'),
('Hiroshi Sato', 'hiroshi.s@hotmail.com', '12345'),
('Carlos Santos', 'carlos.santos@gmail.com', '12345'),
('Ivan Petrov', 'ivan.petrov@proton.me', '12345'),
('Kwame Asante', 'kwame.asante@hotmail.com', '12345'),
('Sebastian Mueller', 'sebastian.m@gmail.com', '12345'),
('Ravi Kumar', 'ravi.kumar@proton.me', '12345'),
('Jean-Luc Moreau', 'jeanluc.m@hotmail.com', '12345'),
('Dmitri Volkov', 'dmitri.volkov@gmail.com', '12345'),

('Sakura Yamamoto', 'sakura.y@proton.me', '12345'),
('Isabella Silva', 'isabella.silva@hotmail.com', '12345'),
('Amara Okafor', 'amara.okafor@gmail.com', '12345'),
('Ingrid Larsson', 'ingrid.larsson@proton.me', '12345'),
('Leila Moreau', 'leila.moreau@hotmail.com', '12345'),
('Anastasia Kozlov', 'anastasia.k@gmail.com', '12345'),
('Carmen Rodriguez', 'carmen.rod@proton.me', '12345'),
('Zoe Mitchell', 'zoe.mitchell@hotmail.com', '12345'),
('Aaliyah Brooks', 'aaliyah.b@gmail.com', '12345'),
('Luna Park', 'luna.park@proton.me', '12345');

INSERT INTO organization (name) VALUES
('Black Mesa Research Facility'),
('Abstergo Industries'),
('Hyperion Corporation'),
('Cyberdyne Systems'),
('Massive Dynamic'),
('Nexus Corporation'),
('RoboCorp'),
('InGen'),
('Omni Consumer Products'),
('Globodyne Corporation');

INSERT INTO campaign (organizer_id, name) VALUES
(11, 'Resonance Cascade Survival Stories'),
(11, 'Headcrab Fashion Week 2024'),
(12, 'Genetic Memory Unboxing Videos'),
(12, 'Modern Day Templar Lifestyle'),
(13, 'Vault Hunter Recruitment Drive'),
(13, 'Pandora Planet Tour Vlogs'),
(14, 'Skynet Beta Testing Program'),
(14, 'Terminator Cosplay Challenge'),
(15, 'Parallel Universe Travel Reviews'),
(15, 'Walter Bishop Cooking Show'),
(16, 'Synthetic Human Unboxing'),
(16, 'Neo-Tokyo Street Fashion'),
(17, 'Detroit Police Recruitment'),
(17, 'Cybernetic Enhancement Tutorials'),
(18, 'Dinosaur Park Safety Training'),
(18, 'Genetic Engineering Life Hacks'),
(19, 'Corporate Dystopia Aesthetic'),
(19, 'Delta City Construction Vlogs'),
(20, 'Business Excellence Seminars'),
(20, 'Corporate Synergy Dance Challenge');

INSERT INTO campaign_requirements (campaign_id, media_type, count) VALUES
(21, 'photo', 12),
(21, 'video', 8),
(22, 'photo', 20),
(22, 'video', 5),
(23, 'video', 10),
(23, 'photo', 15),
(24, 'photo', 18),
(24, 'video', 6),
(25, 'video', 15),
(25, 'photo', 8),
(26, 'video', 20),
(26, 'photo', 25),
(27, 'video', 12),
(27, 'photo', 10),
(28, 'photo', 30),
(28, 'video', 8),
(29, 'video', 18),
(29, 'photo', 12),
(30, 'video', 25),
(30, 'photo', 5),
(31, 'video', 8),
(31, 'photo', 20),
(32, 'photo', 35),
(32, 'video', 10),
(33, 'video', 15),
(33, 'photo', 12),
(34, 'video', 20),
(34, 'photo', 15),
(35, 'video', 22),
(35, 'photo', 8),
(36, 'video', 18),
(36, 'photo', 10),
(37, 'photo', 40),
(37, 'video', 6),
(38, 'video', 16),
(38, 'photo', 20),
(39, 'video', 12),
(39, 'photo', 8),
(40, 'video', 30),
(40, 'photo', 5);

INSERT INTO campaign_application (campaign_id, user_id, status) VALUES
(27, 21, 'accept'),
(31, 21, 'pending'),
(25, 22, 'accept'),
(33, 22, 'pending'),
(23, 23, 'accept'),
(27, 23, 'declined'),
(26, 24, 'accept'),
(29, 24, 'pending'),
(30, 25, 'accept'),
(39, 25, 'pending'),
(25, 26, 'accept'),
(34, 26, 'pending'),
(39, 27, 'accept'),
(37, 27, 'pending'),
(36, 28, 'accept'),
(34, 28, 'pending'),
(24, 29, 'accept'),
(32, 29, 'pending'),
(21, 30, 'accept'),
(35, 30, 'declined'),
(22, 31, 'accept'),
(32, 31, 'accept'),
(24, 32, 'accept'),
(22, 32, 'pending'),
(26, 33, 'accept'),
(29, 33, 'pending'),
(37, 34, 'accept'),
(38, 34, 'pending'),
(30, 35, 'accept'),
(40, 35, 'pending'),
(31, 36, 'accept'),
(27, 36, 'pending'),
(28, 37, 'accept'),
(22, 37, 'declined'),


(33, 38, 'accept'),
(35, 38, 'pending'), 


(40, 39, 'accept'),
(24, 39, 'pending'), 


(36, 40, 'accept'),
(34, 40, 'declined'),


(21, 22, 'pending'),
(23, 31, 'accept'),
(25, 28, 'declined'),
(26, 33, 'accept'),
(28, 37, 'pending'),
(30, 25, 'accept'),
(32, 31, 'declined'),
(34, 40, 'accept'),
(37, 27, 'accept'),
(38, 34, 'pending'),
(39, 35, 'declined'),
(40, 39, 'accept'),
(29, 24, 'accept'),
(33, 26, 'pending'),
(35, 30, 'accept');