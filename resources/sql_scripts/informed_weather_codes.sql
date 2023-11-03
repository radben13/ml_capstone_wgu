
-- Create a table with informed weather codes on severity

/* Informed by the following CSV table loaded directly into Snowflake as "severe_weather_conditions"
Weather Code	Description	Reason for Being Severe
R+ (hvy rain)	Heavy Rain	Can lead to flooding, landslides
TRW+ (hvy rain thunder shwr)	Heavy Rain with Thunder	Combines flooding risk with electrical hazards
S+ (hvy snow)	Heavy Snow	Can cause road blockages, hazardous driving
BS (blowing snow)	Blowing Snow	Reduced visibility, hazardous driving
ZR (mod frz rain)	Moderate Freezing Rain	Ice accumulation on roads, power lines
ZR+ (hvy frz rain)	Heavy Freezing Rain	Significant ice buildup, more severe than ZR
A (mod hail)	Moderate Hail	Can damage property, crops, vehicles
A+ (hvy hail)	Heavy Hail	More severe damage than moderate hail
T (thunder)	Thunder	Indicative of storm conditions, electrical hazards
TRW (mod thunder shwr)	Moderate Thunder Shower	Combines moderate rain with electrical hazards
Q (squalls)	Squalls	Sudden, strong winds, often with precipitation
BD+ (hvy blowing dust)	Heavy Blowing Dust	Significantly reduced visibility
IP (mod ice pellet)	Moderate Ice Pellets	Slippery conditions, hazardous driving
IP+ (hvy ice pellets)	Heavy Ice Pellets	More severe slippery conditions than IP
SP+ (hvy snow pellets)	Heavy Snow Pellets	Slippery conditions, could cause road blockages
*/

create or replace transient table informed_weather_codes
as
select
    code
    , condition
    , severe_reason is not null is_severe
    , severe_reason
from weather_condition_codes
    left join severe_weather_conditions
        on lower(condition) = lower(weather_condition)
order by code

-- Create a lookup table of severe "Observed" weather codes
create or replace transient table informed_weather_condition_codes
as
select weather_cond_code
    , boolor_agg(is_severe) is_severe
    , array_compact(array_agg(distinct code::string)) codes
    , array_compact(array_agg(
        distinct iff(is_severe, code, null)::string
    )) severe_codes
    , array_compact(array_agg(
        distinct iff(is_severe, condition, null)::string
    )) severe_conditions
from station_observations
    join observed_codes on observed_code = weather_cond_code
    join informed_weather_codes
        on code_1 = code
        or code_2 = code
        or code_3 = code
group by 1
order by 1
