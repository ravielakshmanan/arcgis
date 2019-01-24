USE prec_anomaly;

DROP TABLE IF EXISTS precipitation;

CREATE TABLE precipitation (
    latitude      VARCHAR(40)    NOT NULL,
    longitude  	  VARCHAR(40)    NOT NULL,
    anomaly  	  FLOAT          NOT NULL,
    month         VARCHAR(40)    NOT NULL
);

-- SELECT 'LOADING precipitation' as 'INFO';
-- source load_precipitation.dump ;

-- source show_elapsed.sql ;