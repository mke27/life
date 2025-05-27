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

CREATE TABLE IF NOT EXISTS Users
(
    user_ID    INT AUTO_INCREMENT PRIMARY KEY,
    persona_ID INT UNSIGNED NOT NULL,
    user_name  VARCHAR(30)  NOT NULL
);

CREATE TABLE IF NOT EXISTS Post
(
    post_ID    INT AUTO_INCREMENT PRIMARY KEY,
    user_ID    INT NOT NULL,
    text_input TEXT,
    img        BLOB,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_ID) REFERENCES Users (user_ID)
);

CREATE TABLE IF NOT EXISTS Preferences
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
    FOREIGN KEY (user_ID) REFERENCES Users (user_ID)
);

CREATE TABLE IF NOT EXISTS Pref_Factor
(
    pref_ID   INT AUTO_INCREMENT,
    factor_ID INT UNSIGNED,
    PRIMARY KEY (pref_ID, factor_ID),
    FOREIGN KEY (pref_ID) REFERENCES Preferences (pref_ID),
    FOREIGN KEY (factor_ID) REFERENCES Factor (factor_ID)
);

CREATE TABLE IF NOT EXISTS `Predicted Scores`
(
    pred_ID    INT AUTO_INCREMENT PRIMARY KEY,
    factor_ID  INT UNSIGNED NOT NULL,
    country_ID INT UNSIGNED NOT NULL,
    pred_score FLOAT,
    FOREIGN KEY (factor_ID) REFERENCES Factor (factor_ID),
    FOREIGN KEY (country_ID) REFERENCES Country (country_ID)
);

CREATE TABLE IF NOT EXISTS Recommendations
(
    rec_ID       INT AUTO_INCREMENT PRIMARY KEY,
    country_ID   INT UNSIGNED NOT NULL,
    user_ID      INT NOT NULL,
    universities VARCHAR(500),
    urls         VARCHAR(500),
    email        VARCHAR(30),
    FOREIGN KEY (user_ID) REFERENCES Users (user_ID)
);

CREATE TABLE IF NOT EXISTS Policy
(
    policy_ID  INT AUTO_INCREMENT PRIMARY KEY,
    factor_ID  INT UNSIGNED NOT NULL,
    country_ID INT UNSIGNED NOT NULL,
    url        VARCHAR(500),
    title      VARCHAR(500),
    date       DATETIME,
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

CREATE TABLE IF NOT EXISTS ML_Scores
(
    country_ID INT UNSIGNED,
    factor_ID  INT UNSIGNED,
    score      INT UNSIGNED NOT NULL,
    PRIMARY KEY (country_ID, factor_ID),
    FOREIGN KEY (country_ID) REFERENCES ML_Country (country_ID),
    FOREIGN KEY (factor_ID) REFERENCES ML_Factor (factor_ID)
);