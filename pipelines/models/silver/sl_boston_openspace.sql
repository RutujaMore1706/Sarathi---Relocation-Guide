{{ config ( materialized = 'view')}}
with boston_openspace as (
    select site_name,
    coalesce(address, 'Address Not Available') as address,  
    acres as area,
    typelong as Type,
    left(zipcode, 5) as ZIP_CODE
    from {{ ref ('br_boston_openspace')}} 
)
select * 
from boston_openspace