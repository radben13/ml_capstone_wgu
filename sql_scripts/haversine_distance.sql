
-- SQL equivalent of the haversinie distance equation

-- APA citation: 
-- Veness, C. (2021). Calculate distance, bearing and more between Latitude/Longitude points. Movable Type Scripts.
--      Retrieved October 31, 2023, from https://www.movable-type.co.uk/scripts/latlong.html

CREATE OR REPLACE FUNCTION haversine_distance(
    lat1 FLOAT,
    lon1 FLOAT,
    lat2 FLOAT,
    lon2 FLOAT
)
RETURNS FLOAT
LANGUAGE SQL
AS '
    -- This function is based on an algorithm found at:
    -- Article Title: "Calculate distance, bearing and more between Latitude/Longitude points"
    -- Collection Title: Movable Type Scripts
    -- Author: (c) Chris Veness 2002-2021
    -- License: MIT
    -- URL: https://www.movable-type.co.uk/scripts/latlong.html
    -- Date Accessed: October 31, 2023
    6371e3 * 2 * ATAN2(SQRT(SIN(((lat2 - lat1) * PI() / 180) / 2) * SIN(((lat2 - lat1) * PI() / 180) / 2) +
              COS(lat1 * PI() / 180) * COS(lat2 * PI() / 180) *
              SIN(((lon2 - lon1) * PI() / 180) / 2) * SIN(((lon2 - lon1) * PI() / 180) / 2)), SQRT(1 - SIN(((lat2 - lat1) * PI() / 180) / 2) * SIN(((lat2 - lat1) * PI() / 180) / 2) +
              COS(lat1 * PI() / 180) * COS(lat2 * PI() / 180) *
              SIN(((lon2 - lon1) * PI() / 180) / 2) * SIN(((lon2 - lon1) * PI() / 180) / 2)))
';
