

-- Leveraging the Haversine Distance algorithm, grab the nearest station within the county with a weather condition code if one is not already present
-- Save as a table for further cleaning
create or replace transient table resolved_station_observations as
with valid_station_codes as (
    select distinct
        station_id, date_trunc(minute, date_time) date_time, weather_cond_code as valid_code, county, state, longitude, latitude from station_observations
        join weather_stations on station_id = stid
    where weather_cond_code in (select weather_cond_code from informed_weather_condition_codes)
)

, valid_condition_codes as (
    select distinct valid_code from valid_station_codes
)

, checked_stations as (
    select
        * exclude(date_time)
        , date_trunc(minute, date_time) date_time
        , weather_cond_code is not null
            and weather_cond_code in (select valid_code from valid_condition_codes)
        as had_valid_code
    from station_observations
)

select
    base.* exclude(weather_cond_code)
    , iff(base.had_valid_code, base.weather_cond_code, county_code.valid_code) resolved_weather_cond_code
    , base_station.* exclude (stid, name)
    , county_code.station_id resolved_station_id
    , county_code.latitude resolved_station_latitude
    , county_code.longitude resolved_station_longitude
    , iff(resolved_weather_cond_code is not null
        , round(haversine_distance(base_station.latitude, base_station.longitude, county_code.latitude, county_code.longitude))
        , null
    ) as meters_distance
from checked_stations base
    join weather_stations base_station
        on base_station.stid = base.station_id
    left join valid_station_codes county_code
        on not base.had_valid_code
        and county_code.station_id <> base.station_id
        and county_code.county = base_station.county
        and county_code.state = base_station.state
        and county_code.date_time = base.date_time
where resolved_weather_cond_code is not null
qualify row_number() over (partition by base.station_id, base.date_time order by meters_distance) = 1
order by date_time, station_id
;
