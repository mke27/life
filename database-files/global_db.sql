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
    role_name   VARCHAR(30) NOT NULL, 
);

CREATE TABLE IF NOT EXISTS User
(
    user_ID    INT AUTO_INCREMENT PRIMARY KEY,
    user_country INT UNSIGNED NOT NULL,
    user_age   INT UNSIGNED NOT NULL,
    user_name  VARCHAR(30)  NOT NULL
    role_ID  INT UNSIGNED NOT NULL,
    FOREIGN KEY (role_ID) REFERENCES User_Role (role_ID)
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
    factorID_5  INT UNSIGNED NOT NULL,
    weight5     FLOAT,
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

CREATE TABLE IF NOT EXISTS Recommendation
(
    rec_ID       INT AUTO_INCREMENT PRIMARY KEY,
    country_ID   INT UNSIGNED NOT NULL,
    user_ID      INT          NOT NULL,
    universities VARCHAR(500),
    urls         VARCHAR(500),
    email        VARCHAR(30),
    FOREIGN KEY (user_ID) REFERENCES User (user_ID)
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

CREATE TABLE IF NOT EXISTS ML_Factor
(
    factor_ID   INT UNSIGNED PRIMARY KEY,
    factor_name VARCHAR(30) NOT NULL
);

CREATE TABLE IF NOT EXISTS ML_Score
(
    country_ID INT UNSIGNED,
    factor_ID  INT UNSIGNED,
    score      INT UNSIGNED NOT NULL,
    PRIMARY KEY (country_ID, factor_ID),
    FOREIGN KEY (country_ID) REFERENCES ML_Country (country_ID),
    FOREIGN KEY (factor_ID) REFERENCES ML_Factor (factor_ID)
);

INSERT INTO Country (country_ID, country_name)
VALUES (13, 'Belgium'),
       (15, 'Greece');

INSERT INTO Similarity (country_ID, sim_country, sim_score)
VALUES (13, 15, 0.876),
       (15, 13, 0.876);

INSERT INTO Factor (factor_ID, factor_name)
VALUES (1, 'Safety'),
       (2, 'Education');

INSERT INTO Rate (factor_ID, country_ID, rate_of_change)
VALUES (1, 13, 1.159),
       (1, 15, 1.0789);

INSERT INTO User (persona_ID, user_name)
VALUES (372, 'mfontenot'),
       (254, 'egerber');

INSERT INTO Preference (user_ID, top_country, factorID_1, weight1, factorID_2, weight2, factorID_3, weight3,
                         factorID_4, weight4, factorID_5, weight5)
VALUES (1, 13, 1, 0.234, 2, 0.3333, 3, 0.78, 4, 0.99, 5, 0.324),
       (2, 14, 2, 0.34, 1, 0.67, 3, 0.98, 4, 0.9, 5, 0.34);

INSERT INTO Predicted_Score (factor_ID, country_ID, pred_score)
VALUES (1, 13, 1.455),
       (2, 15, 0.978);

INSERT INTO Recommendation (country_ID, user_ID, universities, urls, email)
VALUES (13, 1, 'KU Leuven, Ghent, Antwerp', 'https://www.kuleuven.be/kuleuven', 'kuleuven@edu.com'),
       (15, 2, 'Patras, Thessaly, Athens', 'https://www.upatras.gr/en/', 'patras@edu.com');

INSERT INTO Policy_News (factor_ID, country_ID, url, title, date)
VALUES (1, 13, 'euupdate/parliament.com', 'Changes in EU Parliament', '2025-05-23'),
       (2, 15, 'greecegov/education.com', 'Changes in Greece Education', '2025-05-26');

INSERT INTO ML_Country (country_ID, country_name)
VALUES (13, 'Beligum'),
       (15, 'Greece');

INSERT INTO ML_Factor (factor_ID, factor_name)
VALUES (1, 'Safety'),
       (2, 'Education');

INSERT INTO ML_Score (country_ID, factor_ID, score)
VALUES (13, 1, 78),
       (15, 2, 65);
