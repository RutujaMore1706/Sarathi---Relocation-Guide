with boston_groups as (
 select *, current_timestamp as added_dt
 from {{ source('raw', 'raw_boston_groups') }}
)
select *
from boston_groups
