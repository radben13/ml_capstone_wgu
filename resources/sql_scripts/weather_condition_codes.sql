
-- Create a lookup table of the weather condition codes
-- https://docs.synopticdata.com/services/weather-condition-codes

create or replace transient table weather_condition_codes as
with code_obj as (
    select PARSE_JSON('{
        "0":"(no value)","1":"R (mod rain)","2":"L (mod drizzle)","3":"S (mod snow)","4":"A (mod hail)",
        "5":"T (thunder)","6":"H (haze)","7":"K (smoke)","8":"D (dust)","9":"F (fog)","10":"Q (squalls)",
        "11":"V volcanic ash)","13":"R- (lt rain)","14":"R+ (hvy rain)","15":"ZR (mod frz rain)",
        "16":"RW (mod rain shwr)","17":"L- (lt drizzle)","18":"L+ (hvy drizzle)","19":"ZL (frz drizzle)",
        "20":"S- (lt snow)","21":"S+ (hvy snow)","22":"SW (mod snow shwr)","23":"IP (mod ice pellet)",
        "24":"SG (mod snow grain)","25":"SP (mod snow pellet)","26":"A- (lt hail)","27":"A+ (hvy hail)",
        "28":"T- (lt thunder)","29":"T+ (hvy thunder)","30":"IF (ice fog)","31":"GF (ground fog)",
        "32":"BS (blowing snow)","33":"BD (blowing dust)","34":"BY (blowing spray)","35":"BN (blowing sand)",
        "36":"IC (mod ice crystals)","37":"IN (ice needles)","38":"AP (small hail)","39":"KH (smoke, haze)",
        "40":"PO (dust whirls)","41":"UP (unknown prcp)","49":"ZR- (lt frz rain)","50":"ZR+ (hvy frz rain)",
        "51":"RW- (lt rain shwr)","52":"RW+ (hvy rain shwr)","53":"ZL- (lt freezing drizzle)",
        "54":"ZL+ (hvy freezing drizzle)","55":"SW- (lt snow shwr)","56":"SW+ (hvy snow shwr)",
        "57":"IP- (lt ice pellets)","58":"IP+ (hvy ice pellets)","59":"SG- (lt snow grains)",
        "60":"SG+ (hvy snow grains)","61":"SP- (lt snow pellets)","62":"SP+ (hvy snow pellets)",
        "63":"IPW (mod ice pellet shwr)","64":"IC- (lt ice crystals)","65":"IC+ (hvy ice crystals)",
        "66":"TRW (mod thunder shwr)","67":"SPW (snow pellet shwr)","68":"BD+ (hvy blowing dust)",
        "69":"BN+ (hvy blowing sand)","70":"BS+ (hvy blowing snow)","75":"IPW- (lt ice pellet shwr)",
        "76":"IPW+ (hvy ice pellet shwr)","77":"TRW- (lt rain thunder shwr)","78":"TRW+ (hvy rain thunder shwr)",
        "-1":"Tornado","-2":"Funnel Cloud","-3":"Water Spout"}'
    ) as code_data
)

, weather_codes as (
    select
        floor(key::string) as code
        , value::string as condition
    from code_obj, lateral flatten(input => code_data)
)

select * from weather_codes
order by code
