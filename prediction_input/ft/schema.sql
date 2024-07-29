

CREATE SEQUENCE id_sequence INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 3908 NO CYCLE;

CREATE TABLE prediction_input(id VARCHAR UNIQUE, articleId INTEGER UNIQUE, "timestamp" VARCHAR, "close" DOUBLE, relevance DOUBLE, sentimentPositive DOUBLE, sentimentNegative DOUBLE, sentimentNeutral DOUBLE);




