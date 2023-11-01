
-- Create a function to parse the weather condition codes
create or replace function parse_condition_codes(code number)
returns array
as
$$
    case
        when code < 80
            then [floor(code)]
        when code < 6400
            then [floor(code / 80), code - 80*floor(code/80)]
        else
            [
                floor(code / 6400),
                floor((code - 6400*floor(code/6400))/80),
                code - 80*floor((code - 6400*floor(code/6400))/80) - 6400*floor(code/6400)
            ]
    end
$$
;

-- Create a table of the observed codes
create or replace transient table observed_codes as
with parsed_codes as (
    select distinct
        weather_cond_code
        , parse_condition_codes(try_to_number(weather_cond_code)) code_values
    from station_observations
    where try_to_number(weather_cond_code) is not null
)

select
    weather_cond_code observed_code
    , first_code.code code_1
    , first_code.condition condition_1
    , second_code.code code_2
    , second_code.condition condition_2
    , third_code.code code_3
    , third_code.condition condition_3
from parsed_codes
    join weather_condition_codes first_code
        on first_code.code = code_values[0]
    left join weather_condition_codes second_code
        on second_code.code = code_values[1]
    left join weather_condition_codes third_code
        on third_code.code = code_values[2]
