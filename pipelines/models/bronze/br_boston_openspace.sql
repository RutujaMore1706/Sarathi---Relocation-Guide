with boston_openspace as (
 select *
 from {{ source('raw', 'raw_boston_openspace') }}
)
select *
from boston_openspace
