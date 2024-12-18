with boston_utilities as (
 select *
 from {{ source('raw', 'raw_boston_utilities') }}
)
select *
from boston_utilities
