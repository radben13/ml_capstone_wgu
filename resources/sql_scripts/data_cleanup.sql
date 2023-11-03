



-- Create a combination table where all of the observations are available with a station at each point in time
create or replace transient table station_observations as
with station_observation_times as (
    select distinct
        station_id
        , date_time
    from clean_observations
)

select
    base.station_id
    , base.date_time
    , heat_index.value as heat_index
    , weather_cond_code.value as weather_cond_code
    , weather_condition.value as weather_condition
    , weather_summary.value as weather_summary
    , wind_speed.value as wind_speed
    , pressure.value as pressure
    , air_temp.value as air_temp
    , dew_point_temperature.value as dew_point_temperature
    , relative_humidity.value as relative_humidity
    , altimeter.value as altimeter
    , wind_chill.value as wind_chill
from station_observation_times base
    left join clean_observations heat_index
        on base.station_id = heat_index.station_id
        and heat_index.variable = 'heat_index'
        and base.date_time = heat_index.date_time
    left join clean_observations weather_cond_code
        on base.station_id = weather_cond_code.station_id
        and weather_cond_code.variable = 'weather_cond_code'
        and base.date_time = weather_cond_code.date_time
    left join clean_observations weather_condition
        on base.station_id = weather_condition.station_id
        and weather_condition.variable = 'weather_condition'
        and base.date_time = weather_condition.date_time
    left join clean_observations weather_summary
        on base.station_id = weather_summary.station_id
        and weather_summary.variable = 'weather_summary'
        and base.date_time = weather_summary.date_time
    left join clean_observations wind_speed
        on base.station_id = wind_speed.station_id
        and wind_speed.variable = 'wind_speed'
        and base.date_time = wind_speed.date_time
    left join clean_observations pressure
        on base.station_id = pressure.station_id
        and pressure.variable = 'pressure'
        and base.date_time = pressure.date_time
    left join clean_observations air_temp
        on base.station_id = air_temp.station_id
        and air_temp.variable = 'air_temp'
        and base.date_time = air_temp.date_time
    left join clean_observations dew_point_temperature
        on base.station_id = dew_point_temperature.station_id
        and dew_point_temperature.variable = 'dew_point_temperature'
        and base.date_time = dew_point_temperature.date_time
    left join clean_observations relative_humidity
        on base.station_id = relative_humidity.station_id
        and relative_humidity.variable = 'relative_humidity'
        and base.date_time = relative_humidity.date_time
    left join clean_observations altimeter
        on base.station_id = altimeter.station_id
        and altimeter.variable = 'altimeter'
        and base.date_time = altimeter.date_time
    left join clean_observations wind_chill
        on base.station_id = wind_chill.station_id
        and wind_chill.variable = 'wind_chill'
        and base.date_time = wind_chill.date_time
order by date_time, station_id -- Order by to help Snowflake partitions
;
