-- clean up the variable names to be consistent (remove the "_set_*" suffix)
-- saved as a view to only execute once at a later stage and save compute
create or replace view clean_observations as
select
    stid as station_id
    , date_time::timestamp_ntz as date_time
    , regexp_substr(variable, $$(^.+)_set_[^_]+$$, 1,1,'c',1) variable
    , value
from observations
