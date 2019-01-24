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

-- INSERT INTO `precipitation` VALUES ('88.75S','88.75S',5.4567,'0000 16 Jan 1979\r'),
-- ('88.75S','88.75S',6.4567,'0000 16 Feb 1979\r'),
-- ('88.75S','88.75S',4.4567,'0000 16 Mar 1979\r');

-- source show_elapsed.sql ;