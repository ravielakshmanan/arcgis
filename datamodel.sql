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

ALTER TABLE precipitation_trend ADD INDEX (time_range, longitude, latitude);

show index from precipitation_trend;

CREATE INDEX trend_index ON precipitation_trend(time_range, longitude, latitude);

-- SELECT 'LOADING precipitation' as 'INFO';
-- source load_precipitation.dump ;

-- INSERT INTO `precipitation` VALUES ('88.75S','88.75S',5.4567,'0000 16 Jan 1979\r'),

-- source show_elapsed.sql ;

-- ALTER TABLE precipitation_trend CHANGE COLUMN latitude longi VARCHAR(40);
-- delete from precipitation_trend where latitude = 'Latitude';