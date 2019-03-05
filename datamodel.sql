USE prec_anomaly;

DROP TABLE IF EXISTS precipitation;

CREATE TABLE precipitation (
    latitude      VARCHAR(40)    NOT NULL,
    longitude  	  VARCHAR(40)    NOT NULL,
    anomaly  	  FLOAT          NOT NULL,
    month         VARCHAR(40)    NOT NULL
);

CREATE TABLE precipitation_trend (
	time_range      VARCHAR(40)    NOT NULL,
    longitude  	  	VARCHAR(40)    NOT NULL,
    latitude      	VARCHAR(40)    NOT NULL,
    precipitation  	FLOAT          NOT NULL,
    prec_smoothed   FLOAT		   NOT NULL,
    prec_trend      FLOAT		   NOT NULL
);

-- SELECT 'LOADING precipitation' as 'INFO';
-- source load_precipitation.dump ;

-- INSERT INTO `precipitation` VALUES ('88.75S','88.75S',5.4567,'0000 16 Jan 1979\r'),
-- ('88.75S','88.75S',6.4567,'0000 16 Feb 1979\r'),
-- ('88.75S','88.75S',4.4567,'0000 16 Mar 1979\r');

-- source show_elapsed.sql ;

-- ALTER TABLE precipitation_trend CHANGE COLUMN latitude longi VARCHAR(40);
-- delete from precipitation_trend where latitude = 'Latitude';

-- INSERT INTO precipitation_trend VALUES ('100W','35.025N', '1981', 52.83988);
-- INSERT INTO precipitation_trend VALUES ('100W','35.025N', '1982', 56.4168);
-- INSERT INTO precipitation_trend VALUES ('100W','35.025N', '1983', 42.34973);
-- INSERT INTO precipitation_trend VALUES ('100W','35.025N', '1984', 38.92021);
-- INSERT INTO precipitation_trend VALUES ('100W','35.025N', '1985', 63.37234);
-- INSERT INTO precipitation_trend VALUES ('100W','35.025N', '1986', 75.6129);
-- INSERT INTO precipitation_trend VALUES ('100W','35.025N', '1987', 49.92544);
-- INSERT INTO precipitation_trend VALUES ('100W','35.025N', '1988', 45.8329);
-- INSERT INTO precipitation_trend VALUES ('100W','35.025N', '1989', 50.67971);
-- INSERT INTO precipitation_trend VALUES ('100W','35.025N', '1990', 51.57405);

select longitude, latitude, count(*) from precipitation_trend group by longitude, latitude LIMIT 20;