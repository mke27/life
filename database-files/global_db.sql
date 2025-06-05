DROP DATABASE IF EXISTS global_database;
CREATE DATABASE IF NOT EXISTS global_database;

USE global_database;

CREATE TABLE IF NOT EXISTS Country
(
    country_ID   INT UNSIGNED PRIMARY KEY,
    country_name VARCHAR(30) NOT NULL
);

CREATE TABLE IF NOT EXISTS Similarity
(
    sim_ID      INT AUTO_INCREMENT PRIMARY KEY,
    country_ID  INT UNSIGNED NOT NULL,
    sim_country INT UNSIGNED NOT NULL,
    sim_score   FLOAT,
    FOREIGN KEY (country_ID) REFERENCES Country (country_ID)
);

CREATE TABLE IF NOT EXISTS Factor
(
    factor_ID   INT UNSIGNED PRIMARY KEY,
    factor_name VARCHAR(30) NOT NULL
);

CREATE TABLE IF NOT EXISTS Rate
(
    rate_ID        INT AUTO_INCREMENT PRIMARY KEY,
    factor_ID      INT UNSIGNED NOT NULL,
    country_ID     INT UNSIGNED NOT NULL,
    rate_of_change FLOAT        NOT NULL,
    FOREIGN KEY (factor_ID) REFERENCES Factor (factor_ID),
    FOREIGN KEY (country_ID) REFERENCES Country (country_ID)
);

CREATE TABLE IF NOT EXISTS User_Role
(
    role_ID INT AUTO_INCREMENT PRIMARY KEY,
    role_name   VARCHAR(30) NOT NULL 
);

CREATE TABLE IF NOT EXISTS User
(
    user_ID    INT AUTO_INCREMENT PRIMARY KEY,
    user_country INT UNSIGNED NOT NULL,
    user_age   INT UNSIGNED NOT NULL,
    user_name  VARCHAR(30)  NOT NULL,
    role_ID  INT NOT NULL,
    FOREIGN KEY (role_ID) REFERENCES User_Role (role_ID),
    FOREIGN KEY (user_country) REFERENCES Country (country_ID)
);

CREATE TABLE IF NOT EXISTS Organization
(
    org_ID      INT AUTO_INCREMENT PRIMARY KEY,
    org_name    VARCHAR(30) NOT NULL,
    org_country INT UNSIGNED NOT NULL,
    org_factor  INT UNSIGNED NOT NULL,
    org_url     VARCHAR(100),
    FOREIGN KEY (org_country) REFERENCES Country (country_ID),
    FOREIGN KEY (org_factor) REFERENCES Factor (factor_ID)
);

CREATE TABLE IF NOT EXISTS Preference
(
    pref_ID     INT AUTO_INCREMENT PRIMARY KEY,
    user_ID     INT          NOT NULL,
    pref_date   DATETIME DEFAULT CURRENT_TIMESTAMP,
    top_country INT UNSIGNED NOT NULL,
    factorID_1  INT UNSIGNED NOT NULL,
    weight1     FLOAT,
    factorID_2  INT UNSIGNED NOT NULL,
    weight2     FLOAT,
    factorID_3  INT UNSIGNED NOT NULL,
    weight3     FLOAT,
    factorID_4  INT UNSIGNED NOT NULL,
    weight4     FLOAT,
    FOREIGN KEY (user_ID) REFERENCES User (user_ID)
);

CREATE TABLE IF NOT EXISTS Predicted_Score
(
    pred_ID    INT AUTO_INCREMENT PRIMARY KEY,
    factor_ID  INT UNSIGNED NOT NULL,
    country_ID INT UNSIGNED NOT NULL,
    pred_score FLOAT,
    FOREIGN KEY (factor_ID) REFERENCES Factor (factor_ID),
    FOREIGN KEY (country_ID) REFERENCES Country (country_ID)
);

CREATE TABLE IF NOT EXISTS University
(
    university_ID       INT AUTO_INCREMENT PRIMARY KEY,
    country_ID   INT UNSIGNED NOT NULL,
    university_name VARCHAR(500),
    uni_url         VARCHAR(500),
    user_ID INT NOT NULL,
    FOREIGN KEY (user_ID) REFERENCES User (user_ID),
    FOREIGN KEY (country_ID) REFERENCES Country (country_ID)
);

CREATE TABLE IF NOT EXISTS Policy_News
(
    policy_ID  INT AUTO_INCREMENT PRIMARY KEY,
    factor_ID  INT UNSIGNED NOT NULL,
    country_ID INT UNSIGNED NOT NULL,
    urls        VARCHAR(500),
    title      VARCHAR(500),
    date_created       DATE,
    FOREIGN KEY (factor_ID) REFERENCES Factor (factor_ID),
    FOREIGN KEY (country_ID) REFERENCES Country (country_ID)
);

CREATE TABLE IF NOT EXISTS ML_Country
(
    country_ID   INT UNSIGNED PRIMARY KEY,
    country_name VARCHAR(30) NOT NULL
);

CREATE TABLE IF NOT EXISTS ML_Score
(
    score_ID  INT AUTO_INCREMENT PRIMARY KEY,
    country_ID INT UNSIGNED NOT NULL,
    country_name VARCHAR(100) NOT NULL,
    score_year       INT NOT NULL,
    health_score      FLOAT NOT NULL,
    education_score   FLOAT NOT NULL,
    safety_score     FLOAT NOT NULL,
    environment_score FLOAT NOT NULL,
    qol_score FLOAT NOT NULL,
    FOREIGN KEY (country_ID) REFERENCES ML_Country (country_ID)
);

-- INSERT INTO University
--     VALUES(1, "University of Vienna", "url"), (1, "Vienna University of Technology", "url"), (1, "University of Innsbruck", "url"),
--           (2, "KU Leuven", "url"), (2, "University of Antwerp", "url"), (2, "Ghent University", "url"),
--           (3, "Sofia University", "url"), (3, "International School of Culinary Arts and Crafts ‘Sharena Fabrika’", "url"), (3, "University of Ruse", "url"),
--           (4, "University of Zagreb", "url"), (4, "University of Split", "url"), (4, "Josip Juraj Strossmayer University of Osijek", "url"),
--           (5, "Charles University", "url"), (5, "Czech Technical University in Prague", "url"), (5, "Masaryk University", "url"),
--           (6, "University of Copenhagen", "url"), (6, "Technical University of Denmark", "url"), (6, "Aarhus University", "url"),
--           (7, "University of Tartu", "url"), (7, "Tallinn University of Technology", "url"), (7, "Tallinn University", "url"),
--           (8, "University of Helsinki", "url"), (8, "Aalto University", "url"), (8, "University of Oulu", "url"),
--           (9, "Sorbonne University", "url"), (9, "University of Paris-Saclay", "url"), (9, "Université PSL", "url"),
--           (10, "Ludwig Maximilian University of Munich", "url"), (10, "Technical University of Munich", "url"), (10, "Heidelberg University", "url"),
--           (11, "National and Kapodistrian University of Athens", "url"), (11, "Aristotle University of Thessaloniki", "url"), (11, "Aristotle University of Thessaloniki", "url"),
--           (12, "Eötvös Loránd University", "url"), (12, "Budapest University of Technology and Economics", "url"), (12, "Budapest University of Technology and Economics", "url"),
--           (13, "Trinity College Dublin", "url"), (13, "University College Dublin", "url"), (13, "University College Dublin", "url"),
--           (14, "University of Bologna", "url"), (14, "Sapienza University of Rome", "url"), (14, "Sapienza University of Rome", "url"),
--           (15, "University of Latvia", "url"), (15, "Riga Technical University", "url"), (15, "Riga Technical University", "url"),
--           (16, "Vilnius University", "url"), (16, "Vilnius Gediminas Technical University", 'https://www.vgtu.lt/'), (16, "Vilnius Gediminas Technical University", 'https://www.vgtu.lt/'),
--           (17, 'University of Luxembourg', 'https://wwwen.uni.lu/'), (17, 'University of Luxembourg', 'https://wwwen.uni.lu/'), (17, 'University of Luxembourg', 'https://wwwen.uni.lu/'),
--           (18, 'University of Warsaw', 'https://www.uw.edu.pl/en/'), (18, 'University of Warsaw', 'https://www.uw.edu.pl/en/'), (18, 'University of Warsaw', 'https://www.uw.edu.pl/en/'),
--           (19,'University of Porto', 'https://sigarra.up.pt/up/en/web_page.inicial'),  (19,'University of Porto', 'https://sigarra.up.pt/up/en/web_page.inicial'),  (19,'University of Porto', 'https://sigarra.up.pt/up/en/web_page.inicial'),
--           (20,'Bucharest University', 'https://unibuc.ro/en/'), (20,'Bucharest University', 'https://unibuc.ro/en/'), (20,'Bucharest University', 'https://unibuc.ro/en/'),
--           (21,'Comenius University', 'https'), (21,'Comenius University', 'https'), (21,'Comenius University', 'https'),
--           (22,'Comenius University', 'https'), (22,'Comenius University', 'https'), (22,'Comenius University', 'https'),
--           (23,'Comenius University', 'https'), (23,'Comenius University', 'https'), (23,'Comenius University', 'https'),
--           (24,'Comenius University', 'https'), (24,'Comenius University', 'https'), (24,'Comenius University', 'https');

        

INSERT INTO ML_Country 
    VALUES(1,"Austria"),
          (2,"Belgium"), 
          (3,"Bulgaria"), 
          (4,"Croatia"), 
          (5,"Cyprus"),
          (6,"Czechia"), 
          (7,"Denmark"), 
          (8,"Estonia"), 
          (9,"Finland"), 
          (10,"France"), 
          (11,"Germany"), 
          (12,"Greece"),
          (13,"Hungary"), 
          (14,"Ireland"), 
          (15,"Italy"), 
          (16,"Latvia"), 
          (17,"Lithuania"), 
          (18,"Luxembourg"), 
          (19,"Malta"),
          (20,"Netherlands"),
          (21,"Poland"), 
          (22,"Portugal"),
          (23,"Romania"), 
          (24,"Slovakia"), 
          (25,"Slovenia"), 
          (26,"Spain"), 
          (27,"Sweden");

INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (1,'Austria',2012,-0.0726371764091414,-1.3042268315115002,-0.44647089828964365,0.07707122909569004,1.261656080920897);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (1,'Austria',2013,-0.37893852271274214,-1.2045571211199142,-0.06115162336611681,0.18137815569136087,1.1506567675248562);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (1,'Austria',2014,-0.8712085435578153,0.20681519763501174,-0.031643198247176305,-0.07938916079781597,1.0396574541288153);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (1,'Austria',2015,-0.8055725407784728,0.313867849537086,0.028136932516285174,0.12922469239352524,0.9332557454296511);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (1,'Austria',2016,-1.0134198829130598,0.4159985404321672,0.07629993368041207,0.024917765797854863,0.7848187937876085);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (1,'Austria',2017,-1.0024805491165034,0.491058445788794,0.1749768400274537,0.18137815569136087,0.9595277722689514);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (1,'Austria',2018,-1.0462378843027311,0.5353560948517205,0.15174258082878456,0.25960835063811366,1.1000831158592048);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (1,'Austria',2019,-0.9477838801337158,0.655944139523022,0.1912805120538523,0.41606874053162013,1.163135980273523);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (1,'Austria',2020,-0.6414825338301151,0.6645575712852578,0.14575846150823377,0.024917765797854863,1.1289823453824337);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (1,'Austria',2021,-0.06169784261258484,0.7433089473971283,0.06448435114442659,0.024917765797854863,0.991054204476111);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (1,'Austria',2022,-0.16015184678159852,0.8257517942642427,0.06098852633726809,-0.027235697499980782,0.9043565159064223);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (2,'Belgium',2011,0.39775417684281705,0.5599658998866808,-0.26580239788474924,0.7550662519675497,0.9253741373778621);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (2,'Belgium',2012,0.6384195203670738,0.6854759055649736,-0.30382903366916764,0.676836057020797,0.7335883414509734);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (2,'Belgium',2013,0.47432951341871765,0.728543064376152,-0.3025314567756809,0.6507593253718789,0.7138843213214991);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (2,'Belgium',2014,0.5180868486049486,0.8651274823201779,0.3647741755182904,0.4942989354783729,0.6941803011920248);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (2,'Belgium',2015,0.5509048499946182,0.8675884628236734,0.3269917895020577,0.5986058620740438,0.6836714904563049);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (2,'Belgium',2016,0.43057217823248983,0.9377264071733088,0.37162843463800294,0.5464523987762085,0.6337546394616352);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (2,'Belgium',2017,0.4305721782324883,1.242887989606805,0.4124334115355342,0.5203756671272904,0.681044287772374);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (2,'Belgium',2018,0.3868148430462605,1.2810331874109926,0.4358203268393194,0.5203756671272904,0.6757898824045148);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (2,'Belgium',2019,0.1680281671151169,1.2982600509354643,0.4962568788547801,0.4942989354783729,0.5982874032285804);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (2,'Belgium',2020,0.46339017962215956,1.5012909424738798,0.46798496818727997,0.25960835063811366,0.5588793629696307);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (2,'Belgium',2021,0.6384195203670738,1.7781512491171738,0.38851219986384267,0.3117618139359493,0.5207849240526462);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (2,'Belgium',2022,0.4415115120290449,1.824909878683597,0.4074720881192612,0.1553014240424433,0.5917193965187557);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (3,'Bulgaria',2011,0.5071475148083889,-0.9264663242248723,-0.4332050827550553,-0.13154262409565137,-3.3096765891172453);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (3,'Bulgaria',2012,0.48526884721527574,-0.8612503408822295,-0.4316632560933828,-0.2880030139891576,-3.1888252656564666);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (3,'Bulgaria',2013,0.6165408527739606,-0.6877512153857652,-0.4302588199263147,-0.41838667223374604,-3.033163506633616);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (3,'Bulgaria',2014,0.5180868486049455,-0.5240960119032845,-0.4274041507606438,-0.3140797456380752,-2.8775017476107654);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (3,'Bulgaria',2015,0.34305750786003114,-0.48102885309210563,-0.41563436505619317,-0.1576193557445692,-2.878815348952731);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (3,'Bulgaria',2016,0.8900241976878902,-0.44657512604316263,-0.4045210006037417,-0.3140797456380752,-2.225955481996133);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (3,'Bulgaria',2017,0.6274801865705173,-0.42934826251869096,-0.4006893323653278,-0.20977281904240438,-1.9382767881058025);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (3,'Bulgaria',2018,0.9009635314844467,-0.4035079672319834,-0.3923390434154776,-0.3662332089359106,-1.8358158834325335);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (3,'Bulgaria',2019,1.0322355370431349,-0.47241542132986974,-0.39334657370924375,-0.3662332089359106,-1.7162781613137197);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (3,'Bulgaria',2020,0.8790848638913337,-0.3370614936375929,-0.40181898754318685,-0.6009237937761697,-1.5008475412314628);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (3,'Bulgaria',2021,0.3649361754531443,-0.2878418835676737,-0.4018342531536985,-0.3401564772869928,-1.362919400325139);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (3,'Bulgaria',2022,1.0978715398224772,-0.23000884173551905,-0.3950868533075672,-0.1576193557445692,-1.2381272728384658);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (4,'Croatia',2011,-0.20390918196782787,-1.4703430154974766,-0.35828146636407754,-0.7834609153185935,-1.0318918621499635);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (4,'Croatia',2012,0.2993001726738018,-1.2869999679870285,-0.3654868345255571,-0.8616911102653465,-0.981975011155295);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (4,'Croatia',2013,-0.5867858648473292,-1.0544373104066616,-0.43589183020509853,-0.9659980368610173,-0.9176085453990103);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (4,'Croatia',2014,-0.5211498620679867,-0.975685934294791,-0.4355254555528199,-0.9920747685099349,-0.8532420796427256);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (4,'Croatia',2015,-1.2322065588442035,-0.8624808311339772,-0.43346459813375265,-0.9399213052120997,-1.209228043315236);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (4,'Croatia',2016,-0.8274512083715859,-0.8329490650920265,-0.29950886589438225,-0.9138445735631819,-1.465380304998408);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (4,'Croatia',2017,-0.8821478773543734,-0.7640416109941397,-0.29654733745513007,-0.7834609153185935,-1.428599467423389);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (4,'Croatia',2018,-0.9149658787440447,-0.6176132710361311,-0.3058898910882349,-0.8877678419142643,-1.282789718465275);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (4,'Croatia',2019,-0.9259052125406012,-0.5757766024766996,-0.3059051566987465,-0.8877678419142643,-1.186896820501832);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (4,'Croatia',2020,-0.6852398690163445,-0.5523972876934883,-0.33616159673275586,-0.9138445735631819,-0.6916691145810335);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (4,'Croatia',2021,-0.6743005352197879,-0.5536277779452361,-0.3402069835183323,-0.8877678419142643,-0.3724639884835421);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (4,'Croatia',2022,-0.3133025199333997,-0.4834898335956015,-0.3366348306586157,-0.8095376469675113,-0.3724639884835421);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (5,'Cyprus',2011,-0.0835765102056995,0.8614360115649339,-0.46256085176887973,0.5725291304251261,0.00979400202826856);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (5,'Cyprus',2012,0.4415115120290464,1.0152472930334306,-0.46112588438078844,0.3639152772337845,0.0754740691265175);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (5,'Cyprus',2013,0.6493588541636335,1.122299944935505,-0.4616449151381832,0.1553014240424433,-0.4348600522268787);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (5,'Cyprus',2014,0.9337815328741165,1.267497794641765,-0.460362603855208,0.3117618139359493,-0.9451941735802748);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (5,'Cyprus',2015,0.34305750786003114,1.2047427918026186,-0.4626524454319494,0.33783854558486687,-1.133039165481267);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (5,'Cyprus',2016,1.4151122199226362,1.322869855970424,-0.4634767883995763,0.4942989354783729,-1.034519064833893);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (5,'Cyprus',2017,0.7806308597223184,1.3782419172990823,-0.4624997893268333,0.4682222038294553,-0.8493012756168317);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (5,'Cyprus',2018,0.113331498132331,1.5234397670053432,-0.45941613600348824,0.41606874053162013,-0.4762384944987754);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (5,'Cyprus',2019,0.18990683470823,1.5554325135507912,-0.46109535315976524,0.25960835063811366,-0.3278015428567329);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (5,'Cyprus',2020,0.2446035036910159,1.5960386918584741,-0.4639347567149245,0.12922469239352524,-0.24373105697097389);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (5,'Cyprus',2021,0.8681455300947771,1.785534190627662,-0.4640568815990174,0.1553014240424433,-0.24635825965490357);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (5,'Cyprus',2022,0.9447208666706761,1.989795572417826,-0.4612022124333465,0.12922469239352524,-0.3658959817737173);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (6,'Czechia',2011,0.26648217128413215,-1.4198929151758095,-0.4213589689980466,1.0419103001056442,-0.06376767312177058);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (6,'Czechia',2012,0.33211817406347305,-1.2697731044625569,-0.41862642471646855,0.9376033735099738,-0.15571976705931978);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (6,'Czechia',2013,0.36493617545314583,-1.1270362352597918,-0.3987353342198418,0.8332964469143029,-0.014507622798084152);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (6,'Czechia',2014,0.5509048499946182,-1.019983583357718,-0.3914078411742694,0.7811429836164673,0.12670452146315145);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (6,'Czechia',2015,0.2993001726738018,-0.9498456390080835,-0.39214059047882666,0.7811429836164673,0.2462422435819652);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (6,'Czechia',2016,0.36493617545314583,-0.8489454383647496,-0.3918658094896177,0.8332964469143029,0.26331906102750985);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (6,'Czechia',2017,-0.03981917501947017,-0.7628111207423915,-0.3913773099532462,0.8854499102121381,0.3973063979079386);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (6,'Czechia',2018,0.2446035036910159,-0.7394318059591799,-0.39342290176180184,0.9376033735099738,0.5825241871250012);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (6,'Czechia',2019,0.10239216433577443,-0.7665025914976356,-0.40328448615230134,0.9376033735099738,0.6600266663009343);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (6,'Czechia',2020,0.00393816016675918,-0.7049780789102369,-0.41287128955359187,0.7811429836164673,0.7309611387670438);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (6,'Czechia',2021,0.0805134967426582,-0.5204045411480408,-0.41279496150103384,0.8854499102121381,0.6718490783786196);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (6,'Czechia',2022,0.025816827759872298,-0.47487640183336566,-0.4127338990589874,0.7029127886697145,0.5733289777312456);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (7,'Denmark',2011,0.025816827759872298,0.09114911397070248,-0.1246107662628761,0.7550662519675497,1.901379934457844);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (7,'Denmark',2012,-0.0726371764091414,0.2105066683902558,-0.12358797035859828,0.5203756671272904,1.6872629157175514);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (7,'Denmark',2013,-0.2804845185437269,0.27818363223639403,-0.08327149299743848,0.5725291304251261,1.578234004334458);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (7,'Denmark',2014,-0.18203051437471476,0.3310947130615573,-0.047992667105109715,0.3639152772337845,1.4692050929513647);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (7,'Denmark',2015,-0.5867858648473292,0.44060834546712657,-0.09806386958318776,0.18137815569136087,1.4678914916093995);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (7,'Denmark',2016,-0.30236318613684315,0.551352468124444,-0.11531400946130611,0.2856850822870317,1.46263708624154);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (7,'Denmark',2017,-0.4226958578989715,0.7088552203481848,-0.05423630180435786,0.1553014240424433,1.5059859305263839);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (7,'Denmark',2018,-0.19296984817127133,0.7297735546279006,-0.016285994072497485,0.23353161898919605,1.565097990914808);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (7,'Denmark',2019,-0.6086645324404439,0.8282127747677381,0.026213465591822423,-0.0011589658510631894,1.6255236526451975);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (7,'Denmark',2020,-0.8274512083715859,0.8429786577887135,-0.0002418374247962558,-0.13154262409565137,1.5913700177541081);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (7,'Denmark',2021,-1.1337525546751883,0.9537227804460319,-0.03924547228195766,-0.1576193557445692,1.612387639225548);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (7,'Denmark',2022,-1.2759638940304312,0.9721801342222514,0.0004909118797609839,-0.2619262823402398,1.5467075721272991);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (8,'Estonia',2011,-1.2322065588442035,0.5390475656069642,-0.41851956544288726,1.3287543482437392,-1.4167770553457038);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (8,'Estonia',2012,-1.429114567182231,0.6067245294531033,-0.406383405086158,1.4591380064883275,-1.2906713265170653);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (8,'Estonia',2013,-1.352539230606332,0.6067245294531033,-0.4060475616549026,2.0589028344134346,-1.2887009245041177);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (8,'Estonia',2014,-1.429114567182231,0.6202599222223308,-0.4149932094147056,2.0589028344134346,-1.2867305224911703);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (8,'Estonia',2015,-1.4619325685719038,0.4873669750335499,-0.40079619163890906,1.563444933083998,-1.1711336043982516);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (8,'Estonia',2016,-1.0899952194889588,0.6325648247398108,-0.3905529669856193,2.0589028344134346,-1.0476550782535439);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (8,'Estonia',2017,-1.2540852264373166,0.6571746297747706,-0.3881867973563199,2.267516687604775,-0.8795141064820259);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (8,'Estonia',2018,-1.7135372458927185,0.6694795322922497,-0.40807788785294663,2.4500538091471995,-0.6772194998194185);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (8,'Estonia',2019,-1.2869032278269894,0.7999114989775352,-0.4158175523823325,1.3287543482437392,-0.5077649267059351);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (8,'Estonia',2020,-0.9040265449474881,0.8577445408096898,-0.4203514387042804,0.3117618139359493,-0.28839350259778307);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (8,'Estonia',2021,-1.1446918884717447,0.9488008194390402,-0.42158795315572073,0.4942989354783729,-0.08872609861910542);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (8,'Estonia',2022,-0.5211498620679867,1.0447790590753823,-0.4255417462782275,0.6246825937229613,0.061024454364902524);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (9,'Finland',2011,-0.8055725407784728,0.6067245294531033,-0.16552260243398864,0.1553014240424433,1.5375123627335434);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (9,'Finland',2012,-1.0790558856924024,0.6473307077607862,-0.1699801607033785,-0.20977281904240438,1.2879281077601972);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (9,'Finland',2013,-0.9313748794388803,0.7408479668936329,-0.13099179145672873,0.12922469239352524,1.2990937191668992);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (9,'Finland',2014,-0.7836938731853582,0.8749714043341615,-0.14434920065438675,-0.13154262409565137,1.3102593305736012);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (9,'Finland',2015,-0.8383905421681456,0.9660276829635109,-0.11913041208920841,-0.053312429148898374,1.319454539967357);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (9,'Finland',2016,-0.7946332069819163,1.0152472930334306,-0.09336206154561213,0.2856850822870317,1.393016215117396);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (9,'Finland',2017,-0.9477838801337174,1.058314451844609,-0.05492325427738027,0.3117618139359493,1.6071332338576874);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (9,'Finland',2018,-0.9696625477268306,1.162906123243187,-0.03146001092103699,0.8593731785632206,1.7870966177068908);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (9,'Finland',2019,-1.1884492236579742,1.3044125021942037,0.016886177569229225,0.5203756671272904,1.8396406713854903);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (9,'Finland',2020,-1.0681165518958458,1.4533018226557095,0.08987106142523263,0.20745488734027848,1.882989515670334);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (9,'Finland',2021,-0.0070011736297973795,0.9192690533970885,-0.04519906038148524,0.6507593253718789,1.8554038874890695);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (9,'Finland',2022,-0.8274512083715875,0.9820240562362349,-0.09206448465212537,0.5725291304251261,1.8330726646756654);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (10,'France',2011,0.32117884026691806,0.15390411680984847,-0.3863549240949268,-0.3401564772869928,0.4432824448767132);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (10,'France',2012,0.3321181740634746,0.288027554250378,-0.3867518299682286,-0.3662332089359106,0.4669272690320826);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (10,'France',2013,0.4305721782324883,0.4787535432713141,-0.37830994735530876,-0.3923099405848282,0.34279194221639164);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (10,'France',2014,0.46339017962215956,0.6005720781943629,-0.3715930787302007,-0.5226935988294167,0.21865661540070067);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (10,'France',2015,0.4196328444359302,0.6842454153132259,-0.36261689974937455,-0.496616867180499,0.09123728523009673);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (10,'France',2016,0.3649361754531443,0.7568443401663559,3.2157032666138594,-0.47054013553158125,0.043947636919357866);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (10,'France',2017,0.4415115120290464,0.8257517942642427,2.990627105230694,-0.44446340388266364,0.1056868999917117);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (10,'France',2018,0.49620818101183234,1.0103253320264387,3.2954508159265057,-0.5487703304783345,0.2409878382141047);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (10,'France',2019,0.5399655161980617,1.1641366134949356,3.25763789868925,-0.574847062127252,0.3355671348355836);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (10,'France',2020,0.6384195203670738,1.3683979952850998,2.8489011772409145,-0.7573841836696759,0.36972076972667406);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (10,'France',2021,0.9884782018569055,1.5062129034808724,3.9452315273531497,-0.6530772570740051,0.3657799657007789);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (10,'France',2022,0.6056015189774041,1.5701983965717665,4.58786793306036,-0.7313074520207581,0.33162633080968845);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (11,'Germany',2011,-0.7618152055922435,-0.5302484631620245,3.1331315793565655,0.8072197152653854,0.21471581137480558);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (11,'Germany',2012,-0.8930872111509315,-0.44903610654665854,3.143390069620367,0.8332964469143029,0.34607594557130344);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (11,'Germany',2013,-0.9477838801337158,-0.4108909087424711,3.3933644417479667,0.8854499102121381,0.397306397907938);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (11,'Germany',2014,-1.1446918884717447,-0.5794680732319436,3.747663996111904,0.7811429836164673,0.4485368502445725);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (11,'Germany',2015,1.0322355370431349,-0.5080996386305613,3.8372731298150495,0.7550662519675497,0.7690555776840282);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (11,'Germany',2016,1.0103568694500187,-0.42196532100820283,4.142432683942117,0.7289895203186322,0.7125707199795337);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (11,'Germany',2017,0.922842199077563,-0.3715152206865363,4.56965605972001,0.6507593253718789,0.7309611387670438);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (11,'Germany',2018,0.8790848638913306,-0.31860413986137304,4.876220050014146,0.8072197152653854,0.757233165606344);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (11,'Germany',2019,0.999417535653462,-0.21647344896629098,5.014908121512115,0.5986058620740438,0.8767708877251567);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (11,'Germany',2020,0.8900241976878902,-0.05281824548381067,5.106593378244839,0.3899920088827021,0.9805453937403912);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (11,'Germany',2021,0.8572061962982175,0.050542935663019116,5.034768680787718,0.44214547218053774,0.8215996313626276);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (11,'Germany',2022,-0.13827317918848542,0.03946852339728737,4.723792929055728,0.44214547218053774,0.6350682408036006);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (12,'Greece',2011,1.0650535384328077,-0.6717548421130417,-0.32746019874113863,0.5203756671272904,-0.3619551777478222);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (12,'Greece',2012,0.6931161893498597,-0.5708546414697078,-0.32199511017798255,0.44214547218053774,-1.278848914439381);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (12,'Greece',2013,0.7040555231464194,-0.4059689477354793,-0.3169727243196631,0.25960835063811366,-1.6584797022672608);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (12,'Greece',2014,0.6165408527739606,-0.3505968864068206,-0.31114126110422846,0.20745488734027848,-2.0381104900951406);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (12,'Greece',2015,0.5071475148083889,-0.2533881565187303,-0.3121793226190179,0.10314796074460764,-1.8069166539093036);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (12,'Greece',2016,0.5618441837911747,-0.14018305335791692,-0.3076149050760467,-0.0011589658510631894,-1.5520779935680968);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (12,'Greece',2017,0.6712375217567466,-0.02943893070059945,-0.28152597671170665,0.10314796074460764,-1.3799962177706848);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (12,'Greece',2018,0.8243881949085478,0.024702640376311123,-0.27033628420669714,-0.0011589658510631894,-1.4732619130501983);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (12,'Greece',2019,0.9447208666706761,0.04192950390078326,-0.26931348830241936,-0.1576193557445692,-1.1737608070821823);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (12,'Greece',2020,0.922842199077563,0.15636509731334525,-0.2810985396173816,-0.41838667223374604,-0.9005317279534656);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (12,'Greece',2021,0.8681455300947771,0.3815448133832238,-0.29399798049969134,-0.3401564772869928,-0.6049714260113437);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (12,'Greece',2022,1.1635075426018198,0.4541437382363547,-0.2932804968056457,-0.3140797456380752,-0.6273026488247488);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (13,'Hungary',2011,-0.7071185366094576,-1.1479545695395077,-0.38542372185371865,-0.5487703304783345,-1.925140774686153);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (13,'Hungary',2012,-0.4226958578989715,-1.0187530931059703,-0.3972698356107273,-0.6270005254250874,-2.145825800136269);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (13,'Hungary',2013,-0.46645319308520083,-0.9572285805185716,-0.39429304156096356,-0.6791539887229229,-2.1294057833617073);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (13,'Hungary',2014,-0.40081719030585683,-0.8600198506304818,-0.38337813004516297,-0.7052307203718404,-2.1129857665871454);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (13,'Hungary',2015,-0.5539678634576565,-0.7984953380430831,-0.3848283630437659,-0.6270005254250874,-1.6597933036092263);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (13,'Hungary',2016,-0.40081719030585683,-0.857558870126986,-0.38895007788190034,-0.574847062127252,-1.424658663397494);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (13,'Hungary',2017,-0.32424185372995623,-0.8255661235815384,-0.3782030880817275,-0.5226935988294167,-1.0358326661758586);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (13,'Hungary',2018,-0.12733384539192885,-0.746814747469668,-0.3544040012941288,-0.5226935988294167,-0.854555680984691);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (13,'Hungary',2019,0.014877493963315738,-0.6705243518612934,-0.37698183924079876,-0.5487703304783345,-0.536664156229165);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (13,'Hungary',2020,0.18990683470823,-0.5487058169382443,-0.3775619324402399,-0.6270005254250874,-0.5471729669648849);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (13,'Hungary',2021,0.18990683470823,-0.29645531532990954,-0.37043289233131843,-0.6009237937761697,-0.42369444082017604);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (13,'Hungary',2022,0.20084616850478657,-0.280458942057186,-0.36360916443262914,-0.7052307203718404,-0.4828065012086002);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (14,'Ireland',2011,1.207264877788046,0.9389568974250556,-0.2086021552977497,1.3809078115415743,1.1499999668538734);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (14,'Ireland',2012,1.2182042115846057,1.1050730814110323,-0.2267834974170762,1.3548310798926566,0.8767708877251567);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (14,'Ireland',2013,1.130689541212147,1.3437881902501398,-0.24288871650682387,1.3548310798926566,0.7874459964715383);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (14,'Ireland',2014,1.1416288750087067,1.4594542739144492,-0.23469108366208977,1.3548310798926566,0.6981211052179199);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (14,'Ireland',2015,1.2182042115846057,1.6194180066416852,-0.25468903343229776,1.4330612748394094,0.654772260933075);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (14,'Ireland',2016,1.4916875564985352,1.7043218340122952,-0.24313296627500963,1.4591380064883275,0.7467243548706242);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (14,'Ireland',2017,1.5135662240916483,1.8064525249073777,-0.22852377701539967,1.4852147381372451,0.7467243548706242);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (14,'Ireland',2018,1.677656231040006,1.813835466417866,-0.20612912639486902,1.3548310798926566,0.8045228139170829);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (14,'Ireland',2019,1.7214135662262353,1.8433672324598167,-0.1624389491106436,1.1983706899991506,0.9004157118805273);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (14,'Ireland',2020,0.9884782018569024,2.1042311658303876,-0.13847194060741722,1.0940637634034798,0.888593299802842);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (14,'Ireland',2021,1.207264877788049,2.491835595130999,-0.18407031920559377,1.146217226701315,0.8307948407563832);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (14,'Ireland',2022,0.9447208666706761,2.537363734445674,-0.22272284502098819,0.989756836807809,0.6600266663009343);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (15,'Italy',2011,0.2993001726738018,-1.7644301856652422,0.04270032494436032,-0.07938916079781597,0.22259741942659578);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (15,'Italy',2012,0.014877493963315738,-1.6647604752736567,0.03992198383124745,-0.10546589244673378,-0.5090785280479004);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (15,'Italy',2013,-0.017940507426355494,-1.5921615504205262,0.035739206551066535,-0.3401564772869928,-0.5570249770296221);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (15,'Italy',2014,0.15708883331855877,-1.5134101743086557,0.02261078151108266,-0.44446340388266364,-0.6049714260113437);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (15,'Italy',2015,0.21178550230134624,-1.4531161519730047,0.008383232514262921,-0.3923099405848282,-0.5668769870943592);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (15,'Italy',2016,1.2510222129742785,-1.417431934672314,0.0603321050852689,-0.41838667223374604,-0.5839538045399039);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (15,'Italy',2017,1.0103568694500218,-1.299304870504508,0.10841877819683776,-0.3662332089359106,-0.536664156229165);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (15,'Italy',2018,1.130689541212147,-1.2033266308681665,0.11508984999041096,-0.496616867180499,-0.24373105697097389);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (15,'Italy',2019,1.4588695551088624,-1.1491850597912554,0.09863352185889629,-0.5226935988294167,-0.02830043688871701);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (15,'Italy',2020,1.3713548847364068,-1.0975044692178406,0.0403341553150609,-0.6530772570740051,0.0978052919399215);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (15,'Italy',2021,1.4041728861260765,-1.060589761665401,-0.020865677225980234,-0.496616867180499,0.07678767046848176);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (15,'Italy',2022,1.2619615467708318,-1.0126006418472304,-0.031811119962804,-0.496616867180499,-0.004655612733346416);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (16,'Latvia',2011,-1.440053900978789,-0.39366404521799936,-0.44682200733141064,-1.0442282318077702,-2.162902617581815);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (16,'Latvia',2012,-1.0681165518958458,-0.24354423450474627,-0.4348690343008207,-1.226765353350194,-1.7898398364637589);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (16,'Latvia',2013,-1.9104452542307475,-0.02943893070059945,-0.4518596588002417,-1.0703049634566881,-1.7556862015726695);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (16,'Latvia',2014,-1.811991250061734,-0.044204813721574816,-0.43567811165793596,-0.5487703304783345,-1.7215325666815802);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (16,'Latvia',2015,-1.9104452542307475,0.09607107497769383,-0.42297712371227714,-0.6791539887229229,-1.1146487466937582);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (16,'Latvia',2016,-1.768233914875506,0.19820176587277588,-0.4361971424153307,-0.9138445735631819,-0.7337043575239129);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (16,'Latvia',2017,-2.2495646019240194,0.25603480770493053,-0.4312205533885461,-1.0963816951056058,-0.6246754461408192);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (16,'Latvia',2018,-2.041717259789434,0.26218725896367046,-0.4370520166039808,-0.6791539887229229,-0.6154802367470635);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (16,'Latvia',2019,-1.8666879190445183,0.376622852376232,-0.44089895045290634,-0.9138445735631819,-0.602344223327414);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (16,'Latvia',2020,-1.8010519162651757,0.6141074709635914,-0.4466998824473178,-0.6270005254250874,-0.4946289132862855);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (16,'Latvia',2021,-1.7244765796892767,0.7556138499146082,-0.45451587502926166,-0.3923099405848282,-0.3002159146754684);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (16,'Latvia',2022,-1.636961909316818,0.8368262065299741,-0.45752320030004867,0.05099449744677246,-0.25686707039062345);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (17,'Lithuania',2011,-0.47739252688175743,0.20435421713151586,-0.4424102458935556,-1.2789188166480296,-1.077867909118738);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (17,'Lithuania',2012,-0.5649071972542146,0.3064849080265979,-0.43096103800984875,-1.226765353350194,-1.2906713265170653);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (17,'Lithuania',2013,-0.5430285296610998,0.4393778552153784,-0.4409142160634179,-1.2528420849991118,-1.023353453427191);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (17,'Lithuania',2014,-0.4445745254920846,0.668249042040502,-0.43735732881421296,-1.1746118900523588,-0.756035580337317);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (17,'Lithuania',2015,-1.1446918884717447,0.868818953075422,-0.43831906227644435,-1.0442282318077702,-0.7823076071766173);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (17,'Lithuania',2016,-0.8493298759647022,0.9278824851593244,-0.4419217463571841,-0.9399213052120997,-0.6653970877417332);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (17,'Lithuania',2017,-0.7836938731853598,0.9930984685019671,-0.43682303244630666,-0.8616911102653465,-0.5997170206434843);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (17,'Lithuania',2018,-0.8712085435578153,1.1075340619145286,-0.4276941973603644,-0.7834609153185935,-0.34093755627638245);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (17,'Lithuania',2019,-0.9040265449474881,1.3720894660403429,-0.42984664844250126,-0.7834609153185935,-0.25423986770669377);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (17,'Lithuania',2020,-1.0462378843027296,1.4237700566137579,-0.43196856830361496,-0.8095376469675113,-0.2016958140280944);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (17,'Lithuania',2021,-0.8930872111509315,1.5259007475088395,-0.4288391181487351,-0.8095376469675113,0.049202042287217224);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (17,'Lithuania',2022,-0.3133025199333997,1.7498499733269708,-0.4298313828319897,-0.9659980368610173,0.4656136676901172);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (18,'Luxembourg',2011,1.0431748708396882,0.491058445788794,-0.43195330269310334,3.779967123242001,0.8439308541760328);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (18,'Luxembourg',2012,0.9665995342637892,0.6620965907817615,-0.4374183912562594,3.4670463434549887,0.8478716582019279);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (18,'Luxembourg',2013,0.3649361754531443,0.9488008194390402,-0.42766366613934115,3.0237419054233885,0.7769371857358184);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (18,'Luxembourg',2014,0.45245084582560297,1.4065431930892862,-0.4128865551641035,2.6847443939874585,0.7060027132697089);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (18,'Luxembourg',2015,0.10239216433577443,0.9180385631453407,-0.40548273406597307,2.3718236142004465,0.607482612622336);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (18,'Luxembourg',2016,-0.3351811875265144,1.0890767081383084,-0.4160770677610298,2.1371330293601867,0.5969738018866162);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (18,'Luxembourg',2017,-0.5649071972542146,0.8638969920684302,-0.43589183020509853,2.1371330293601867,0.6587130649589701);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (18,'Luxembourg',2018,-0.23672718335750068,1.3093344632011965,-0.4310068348413836,2.267516687604775,0.8951613065126667);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (18,'Luxembourg',2019,0.18990683470823,1.6834034997325804,-0.41215380585954625,2.189286492658023,1.089574305123485);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (18,'Luxembourg',2020,0.3321181740634746,1.5788118283340025,-0.4063376082546232,1.3809078115415743,1.202544020532473);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (18,'Luxembourg',2021,0.058634829149545084,2.0870043023059157,-0.4192523147474445,1.406984543190492,1.3076321278896716);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (18,'Luxembourg',2022,-0.357059855119629,2.2568119570471366,-0.42210698391311546,0.8332964469143029,1.0764382917038342);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (19,'Malta',2011,1.8855035731745962,-1.3079183022667444,-0.47413218453667944,-0.2880030139891576,-0.5892082099077643);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (19,'Malta',2012,2.224622920867865,-1.1356496670220277,-0.47375054427388924,-0.18369608739348678,-0.5839538045399039);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (19,'Malta',2013,2.290258923647211,-1.0089091710919862,-0.47367421622133116,-0.3923099405848282,-0.3619551777478222);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (19,'Malta',2014,2.56374226856114,-0.8317185748402779,-0.4739184659895169,-0.41838667223374604,-0.13995655095574056);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (19,'Malta',2015,2.6074996037473666,-0.7763465135116192,-0.47445276235742323,-0.8877678419142643,0.10437329864974745);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (19,'Malta',2016,2.202744253274752,-0.7652721012458878,-0.47353682572672673,-1.0703049634566881,0.1556037509863814);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (19,'Malta',2017,2.3996522616127822,-0.5733156219732036,-0.47211712394914707,-1.0181515001588528,0.2869638851828793);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (19,'Malta',2018,2.3996522616127822,-0.3026077665886495,-0.4715370307497059,-1.0442282318077702,0.4170104180374129);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (19,'Malta',2019,2.5199849333749107,-0.06020118699429879,-0.47442223113640003,-1.0442282318077702,0.47874968110976673);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (19,'Malta',2020,1.9183215745642659,0.07638323094972667,-0.47428484064179555,-1.0703049634566881,0.2541238516337554);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (19,'Malta',2021,1.5354448916847645,0.24126892468395514,-0.4675832376271991,-1.0703049634566881,0.05051564362918264);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (19,'Malta',2022,1.8636249055814769,0.19574078536928,-0.47362841938979633,-1.0181515001588528,-0.14258375363967024);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (20,'Netherlands',2011,-0.03981917501947017,0.21419813914549987,-0.23435524023083434,1.0679870317545623,1.4495010728218893);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (20,'Netherlands',2012,-0.10545517779881262,0.294180005509118,-0.23038618149781598,0.989756836807809,1.4495010728218893);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (20,'Netherlands',2013,-0.48833186067831397,0.3901582451454601,-0.23130211812851253,0.9636801051588914,1.361489782910236);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (20,'Netherlands',2014,-0.11639451159537074,0.45783520899159874,-0.2449190427048679,0.8332964469143029,1.2734784929985823);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (20,'Netherlands',2015,-0.5539678634576565,0.5624268803901763,-0.26580239788474924,0.9376033735099738,1.2222480406619483);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (20,'Netherlands',2016,-0.30236318613684315,0.6374867857468026,-0.28679261233821185,0.9376033735099738,1.2721648916566168);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (20,'Netherlands',2017,-0.37893852271274214,0.7974505184740388,-0.29793650801168653,0.8593731785632206,1.3562353775423759);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (20,'Netherlands',2018,-0.5539678634576565,0.913116602138349,-0.28633464402286357,0.7550662519675497,1.4179746406147309);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (20,'Netherlands',2019,-0.16015184678159852,1.1321438669494877,-0.2642758368335883,0.6507593253718789,1.3667441882780957);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (20,'Netherlands',2020,-0.14921251298504198,1.3573235830193675,-0.2814496486591486,0.3639152772337845,1.3864482084075713);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (20,'Netherlands',2021,-0.30236318613684315,1.5209787865018478,-0.29976838127307964,0.3899920088827021,1.3220817426512865);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (20,'Netherlands',2022,-0.696179202812901,1.663715655704613,-0.29740221164378017,0.18137815569136087,1.3063185265477062);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (21,'Poland',2011,-0.11639451159536919,-0.8144917113158067,0.660972816275043,0.33783854558486687,-0.7954436205962668);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (21,'Poland',2012,-0.16015184678159852,-0.6680633713577976,0.6888020242377064,0.2856850822870317,-0.770485195098932);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (21,'Poland',2013,-0.16015184678159852,-0.543783855931252,0.6213432913869056,0.23353161898919605,-0.7908460158993891);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (21,'Poland',2014,-0.09451584400225607,-0.39981649647673934,0.4971880810959883,0.20745488734027848,-0.8112068366998461);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (21,'Poland',2015,-0.0070011736297973795,-0.3382919838893406,0.363033895919967,0.25960835063811366,-0.7534083776533873);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (21,'Poland',2016,0.27742150508068714,-0.2878418835676737,0.4459414266085163,0.2856850822870317,-0.5721313924622198);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (21,'Poland',2017,0.0805134967426582,-0.18817217317608753,0.5101027875888097,0.3639152772337845,-0.37509119116747175);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (21,'Poland',2018,0.15708883331855877,-0.08604148228100635,0.44020155705615127,0.3899920088827021,-0.2975887119915375);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (21,'Poland',2019,0.17896750091167346,0.07146126994273444,0.543366552893606,0.3639152772337845,-0.2923343066236782);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (21,'Poland',2020,0.13521016572544411,0.12929431177488906,0.5390769163398438,0.2856850822870317,-0.3186063334629773);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (21,'Poland',2021,0.21178550230134469,0.08745764321545842,0.5859881374420187,0.4942989354783729,-0.37509119116747175);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (21,'Poland',2022,0.16802816711511534,0.16251754857208475,0.593361427319126,0.3117618139359493,-0.19512780731826962);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (22,'Portugal',2011,-0.4445745254920846,-1.3780562466163784,-0.4125201805118249,-0.5487703304783345,-1.420717859371599);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (22,'Portugal',2012,0.40869351063937365,-1.210709572378654,-0.4060475616549026,-0.574847062127252,-1.7175917626556851);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (22,'Portugal',2013,0.2993001726738018,-1.0716641739311332,-0.40586437432876327,-0.574847062127252,-1.7169349619847023);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (22,'Portugal',2014,-1.0462378843027311,-0.8071087698053185,-0.40432254766709075,-0.6530772570740051,-1.7162781613137197);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (22,'Portugal',2015,-1.1118738870820737,-0.6545279785885699,-0.39597225871724057,-0.496616867180499,-1.6886925331324552);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (22,'Portugal',2016,-0.6633612014232297,-0.5696241512179601,-0.38913326520803965,-0.496616867180499,-1.5941132365109763);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (22,'Portugal',2017,-0.6852398690163445,-0.5056386581270654,-0.37791304148200694,0.024917765797854863,-1.311688947988505);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (22,'Portugal',2018,-0.6633612014232297,-0.39366404521799936,-0.37701237046182196,-0.5487703304783345,-0.9399397682124154);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (22,'Portugal',2019,-0.5430285296610998,-0.2029380561970638,-0.3890874683765048,-0.6270005254250874,-0.653574675664049);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (22,'Portugal',2020,-0.4226958578989715,-0.0688146187565342,-0.41630605191870396,-0.7834609153185935,-0.6299298515086785);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (22,'Portugal',2021,-0.7289972042025739,0.19697127562102815,-0.4090548869256896,-0.8095376469675113,-0.5156465347577253);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (22,'Portugal',2022,-0.5649071972542146,0.2351164734252152,-0.3782488849132623,-0.7573841836696759,-0.5786993991720445);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (23,'Romania',2011,-0.9806018815233871,-1.7558167539030067,-0.42409151327962463,-0.8877678419142643,-1.6164444593243814);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (23,'Romania',2012,-0.8930872111509299,-1.6770653777911362,-0.4330066298184044,-0.9659980368610173,-1.8069166539093036);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (23,'Romania',2013,-0.7071185366094576,-1.6290762579729652,-0.43931132695969893,-1.0963816951056058,-1.7471477928498973);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (23,'Romania',2014,-0.5867858648473292,-1.5761651771478022,-0.44010513870630263,-1.226765353350194,-1.6873789317904908);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (23,'Romania',2015,-0.553967863457658,-1.5269455670778833,-0.3997123332925848,-1.226765353350194,-1.1566839896366377);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (23,'Romania',2016,-0.49927119447487206,-1.5318675280848753,-0.4085663873893181,-1.2789188166480296,-0.7665443910730368);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (23,'Romania',2017,-0.6524218676266716,-1.483878408266704,-0.3832865363820933,-1.226765353350194,-0.6089122300372387);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (23,'Romania',2018,-0.4992711944748705,-1.4752649765044685,-0.34730549240623054,-1.1746118900523588,-0.4447120622916158);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (23,'Romania',2019,-0.3133025199333997,-1.4100489931618259,-0.3531827524532001,-1.226765353350194,-0.3737775898255075);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (23,'Romania',2020,-0.3898778565093003,-1.3989745808960938,-0.37594377772600934,-1.304995548296947,-0.35275996835406775);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (23,'Romania',2021,-0.8602692097612588,-1.3657513440988989,-0.35748765461747384,-1.226765353350194,0.08992368388813247);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (23,'Romania',2022,-0.5867858648473292,-1.2746950654695486,-0.3357494252489424,-1.2528420849991118,0.23704703418821074);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (24,'Slovakia',2011,-2.074535261179105,-1.2746950654695486,-0.4652170679978997,-0.2358495506913222,-0.9872294165231543);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (24,'Slovakia',2012,-1.844809251451405,-1.1836387868401983,-0.4652628648294345,-0.41838667223374604,-0.5773857978300792);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (24,'Slovakia',2013,-1.5932045741305902,-1.118422803497556,-0.4473868349203402,-0.47054013553158125,-0.5603089803845345);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (24,'Slovakia',2014,-1.4509932347753471,-1.0975044692178406,-0.4522870958945667,-0.47054013553158125,-0.5432321629389898);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (24,'Slovakia',2015,-1.4728719023684602,-1.0089091710919862,-0.4501346448124299,-0.44446340388266364,-0.43420325155589595);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (24,'Slovakia',2016,-1.0899952194889588,-0.895704067931173,-0.4540579067139134,-0.41838667223374604,-0.4079312247165968);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (24,'Slovakia',2017,-1.3306605630132171,-0.7824989647703591,-0.4542563596505643,-0.3662332089359106,-0.30941112406922283);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (24,'Slovakia',2018,-1.2322065588442035,-0.6397620955675941,-0.45283665787298466,-0.3401564772869928,-0.27657109052009776);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (24,'Slovakia',2019,-1.2103278912510889,-0.5019471873718214,-0.4505468162962433,-0.47054013553158125,-0.1675421791370051);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (24,'Slovakia',2020,-1.0899952194889588,-0.42934826251869096,-0.4540579067139134,-0.7052307203718404,-0.10186211203875498);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (24,'Slovakia',2021,-1.0571772180992878,-0.34321394489633245,-0.44979880138117445,-0.5226935988294167,-0.02304603152085649);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (24,'Slovakia',2022,-0.958723213930274,-0.1697148193998681,-0.4537067976721464,-0.7052307203718404,0.0794148731524126);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (25,'Slovenia',2011,-1.702597912096162,-0.7591196499871479,-0.45387471938777413,-0.5487703304783345,-0.6391250609024342);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (25,'Slovenia',2012,-1.2322065588442035,-0.5782375829801955,-0.44998198870731376,-0.6009237937761697,-0.4578480757112665);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (25,'Slovenia',2013,-0.6852398690163445,-0.38505061345576397,-0.450714738011871,-0.496616867180499,-0.5970898179595545);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (25,'Slovenia',2014,-0.6524218676266716,-0.31122119835088535,-0.45147801853745145,0.024917765797854863,-0.7363315602078426);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (25,'Slovenia',2015,-0.7836938731853582,-0.10942079706421758,-0.45033309774908076,0.05099449744677246,-0.8414196675650414);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (25,'Slovenia',2016,-0.7399365379991304,-0.02943893070059945,-0.45491278090256354,0.18137815569136087,-0.854555680984691);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (25,'Slovenia',2017,-1.4728719023684602,0.125602841019645,-0.4520581117368926,0.20745488734027848,-0.6049714260113437);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (25,'Slovenia',2018,-1.3634785644028884,0.1588260778168407,-0.4536915320616348,0.18137815569136087,-0.3816591978772966);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (25,'Slovenia',2019,-0.14921251298504198,0.2080456878867599,-0.4559050455858181,-0.574847062127252,-0.05982686909587548);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (25,'Slovenia',2020,0.7478128583326457,0.484905994530054,-0.45401210988237856,-0.7052307203718404,0.06890606241669273);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (25,'Slovenia',2021,0.8353275287051043,1.0189387637886747,-0.45515703067074925,-0.6791539887229229,0.2909046892087744);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (25,'Slovenia',2022,1.1088108736190339,1.0029423905159507,-0.45576765509121364,-0.7313074520207581,0.3171767160480747);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (26,'Spain',2011,0.8353275287051043,0.17974441209655645,-0.24450687122105444,-0.44446340388266364,0.4629864650061875);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (26,'Spain',2012,0.7915701935188749,0.2572652979566787,-0.25536072029480855,-0.47054013553158125,-0.11368452411644028);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (26,'Spain',2013,0.5727835175877314,0.37785334262798015,-0.25861229533378133,-0.6009237937761697,-0.10908691941956306);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (26,'Spain',2014,0.7259341907395325,0.459065699243346,-0.2721223606365554,-0.6009237937761697,-0.10448931472268583);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (26,'Spain',2015,0.5071475148083889,0.5279731533412328,-0.29260880994313493,-0.574847062127252,-0.06245407177980632);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (26,'Spain',2016,0.9884782018569055,0.6387172759985503,-0.28682314355923505,-0.6270005254250874,-0.007282815417277259);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (26,'Spain',2017,1.6995348986331222,0.7211601228656648,-0.2790376821983144,-0.574847062127252,-0.12944774022002067);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (26,'Spain',2018,1.3822942185329634,0.8380566967817227,-0.2611005898471736,-0.6009237937761697,-0.07164928117356077);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (26,'Spain',2019,1.7979889028021374,0.9881765074949753,-0.22307395406275518,-0.7052307203718404,-0.009910018101206937);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (26,'Spain',2020,1.0103568694500187,1.1284523961942443,-0.21562433613308993,-0.9399213052120997,0.10831410267564139);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (26,'Spain',2021,0.2446035036910159,1.271189265397009,-0.1972903379086473,-0.8356143786164288,0.08861008254616705);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (26,'Spain',2022,-0.11639451159536919,1.3425576999983913,-0.1859327236880101,-0.8095376469675113,0.03606602886756767);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (27,'Sweden',2011,0.8243881949085446,0.3470910863342808,0.9275409070287621,-2.1655276927112306,1.2747920943405464);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (27,'Sweden',2012,0.8517365293999392,0.4787535432713141,1.0097004228022428,-2.1916044243601482,1.407465829879011);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (27,'Sweden',2013,0.8790848638913337,0.6497916882642825,1.0371174592810928,-2.243757887657984,1.3312769520450416);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (27,'Sweden',2014,2.454348930595568,0.8036029697327792,1.0225235356319944,-2.243757887657984,1.2550880742110722);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (27,'Sweden',2015,2.3996522616127822,0.9401873876768042,0.9971673565722116,-2.1916044243601482,1.1591951762476291);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (27,'Sweden',2016,2.509045599578354,1.081693766627821,0.9512026033217563,-2.1133742294133957,1.1499999668538734);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (27,'Sweden',2017,2.3777735940196694,1.1518317109774556,1.0902875806930274,-1.9829905711688072,1.1894080071128232);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (27,'Sweden',2018,2.443409596799009,1.2810331874109926,1.182293415246496,-1.8526069129242186,1.2275024460298076);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (27,'Sweden',2019,2.5309242671714673,1.3819333880543263,1.284618802505812,-1.8786836445731363,1.2406384594494573);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (27,'Sweden',2020,2.4215309292058955,1.4262310371172542,1.4503575358303529,-1.9829905711688072,1.2537744728691078);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (27,'Sweden',2021,1.4698088889054222,1.5332836890193278,1.3585806854345586,-1.8526069129242186,1.2813601010503723);
INSERT INTO ML_Score(country_ID,country_name,score_year,health_score,education_score,safety_score,environment_score,qol_score) VALUES (27,'Sweden',2022,1.0322355370431349,1.6797120289773364,1.2920531548249659,-1.8786836445731363,1.2958097158119863);
