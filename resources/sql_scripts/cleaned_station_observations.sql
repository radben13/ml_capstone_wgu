
-- Create a new table that has only the columns that will be leveraged for the project
create or replace transient table cleaned_station_observations as
with cleaned_station_observations as (
    select
        station_id
        , date_time
        , try_to_number(air_temp::string, 10, 1) air_temp
        , try_to_number(pressure::string, 10, 1) pressure
        , try_to_number(wind_speed::string, 10, 1) wind_speed
        , try_to_number(relative_humidity::string, 10, 1) relative_humidity
        , try_to_number(dew_point_temperature::string, 10, 1) dew_point_temperature
        , try_to_number(altimeter::string, 10, 1) altimeter
        , try_to_number(elevation::string, 10, 1) elevation
        , try_to_number(latitude::string, 10, 5) latitude
        , try_to_number(longitude::string, 10, 5) longitude
        , county
        , state
        , country
        , had_valid_code had_own_weather_cond_code
        , resolved_station_id
        , try_to_number(resolved_station_latitude::string, 10, 5) resolved_station_latitude
        , try_to_number(resolved_station_longitude::string, 10, 5) resolved_station_longitude
        , ifnull(meters_distance, 0) meters_distance
        , resolved_weather_cond_code
    from resolved_station_observations
)

select r.*
    , is_severe
    , iff(array_size(severe_codes) > 0, array_to_string(severe_codes, ', '), null) severe_codes
    , iff(array_size(severe_conditions) > 0, array_to_string(severe_conditions, ', '), null) severe_conditions
from cleaned_station_observations r
    join informed_weather_condition_codes
        on weather_cond_code = resolved_weather_cond_code
where 1=1
    and air_temp is not null
    and pressure is not null
    and wind_speed is not null
    and elevation is not null
    and relative_humidity is not null
    and dew_point_temperature is not null
order by date_time, state, county, station_id
