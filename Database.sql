-- ==================================================================
-- COVID-19 database for PostgreSQL
-- ==================================================================


-- ------------------------------------------------------------------
-- TABLES
-- ------------------------------------------------------------------

-- ------------------------------------------------------------------
-- Affiliation ------------------------------------------------------

DROP TABLE IF EXISTS Affiliation;
CREATE TABLE Affiliation 
  ( 
     id_affiliation    SERIAL PRIMARY KEY NOT NULL,  
     affiliation_name  VARCHAR NOT NULL, 
     affiliation_type  VARCHAR NOT NULL 
     
  ); 
-- ------------------------------------------------------------------



-- ------------------------------------------------------------------
-- Author -----------------------------------------------------------

DROP TABLE IF EXISTS Author ;
CREATE TABLE Author 
  ( 
     id_author       SERIAL PRIMARY KEY NOT NULL, 
     first_name      VARCHAR NOT NULL, 
     middle_name     VARCHAR NULL, 
     last_name       VARCHAR NOT NULL,
     suffix          VARCHAR NULL,
     id_affiliation  INT NULL, --fk--
     email           VARCHAR NULL,
     FOREIGN KEY(id_affiliation) REFERENCES Affiliation(id_affiliation)
  ); 
-- -------------------------------------------------------------------




-- -------------------------------------------------------------------
-- Studytype ---------------------------------------------------------

DROP TABLE IF EXISTS Studytype ;
CREATE TABLE Studytype 
  ( 
     id_study     SERIAL PRIMARY KEY NOT NULL,      
     study_name   VARCHAR NOT NULL
     
  ); 
-- -------------------------------------------------------------------- 



  
-- --------------------------------------------------------------------
-- Newspaper ----------------------------------------------------------

DROP TABLE IF EXISTS Newspaper ;
CREATE TABLE Newspaper
  ( 
    id_newspaper     SERIAL PRIMARY KEY NOT NULL, 
    newspaper_name   VARCHAR NOT NULL
     
  ); 
-- ---------------------------------------------------------------------





-- ---------------------------------------------------------------------
-- Theme ---------------------------------------------------------------

DROP TABLE IF EXISTS Theme;
CREATE TABLE Theme
  ( 
    id_theme     SERIAL PRIMARY KEY NOT NULL, 
    theme_name   VARCHAR NOT NULL
     
  ); 
-- ---------------------------------------------------------------------





-- ----------------------------------------------------------------------
-- Subject --------------------------------------------------------------

DROP TABLE IF EXISTS Subject ;
CREATE TABLE Subject
  ( 
    id_subject    SERIAL PRIMARY KEY NOT NULL,
    id_theme      INT NOT NULL, --fk--
    theme_name    TEXT NOT NULL,
    FOREIGN KEY(id_theme) REFERENCES Theme(id_theme)
  );
-- ---------------------------------------------------------------------- 




-- ------------------------------------------------------------------
-- Article-----------------------------------------------------------

DROP TABLE IF EXISTS Article ;
CREATE TABLE Article 
  ( 
     id_article          SERIAL PRIMARY KEY NOT NULL,     
     title               VARCHAR NOT NULL, 
     publication_date    TIMESTAMP NOT NULL,
     abstract            TEXT NULL,
     studylink           TEXT NULL,
     id_study            INT NOT NULL, --fk--
     id_newspaper        INT NOT NULL, --fk--
     FOREIGN KEY(id_study) REFERENCES Studytype(id_study),
     FOREIGN KEY(id_newspaper) REFERENCES Newspaper(id_newspaper)
     
  ); 
-- -------------------------------------------------------------------




-- -------------------------------------------------------------------
-- Subject_article ---------------------------------------------------

DROP TABLE IF EXISTS Subject_article;
CREATE TABLE Subject_article
  ( 
     id_subject      INT NOT NULL, --fk--
     id_article      INT NOT NULL, --fk--
     FOREIGN KEY(id_subject) REFERENCES Subject(id_subject),
     FOREIGN KEY(id_article) REFERENCES Article(id_article)
     
  ); 
-- -------------------------------------------------------------------- 
  



-- --------------------------------------------------------------------
-- Article_author------------------------------------------------------

DROP TABLE IF EXISTS Article_author;
CREATE TABLE Article_author
  ( 
    id_article    INT NOT NULL, --fk--
    id_author     INT NOT NULL, --fk--
    FOREIGN KEY(id_author) REFERENCES Author(id_author),
    FOREIGN KEY(id_article) REFERENCES Article(id_article)
     
  ); 
-- --------------------------------------------------------------------
