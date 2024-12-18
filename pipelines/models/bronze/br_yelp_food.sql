{{ config(
    materialized='incremental',
    incremental_strategy='merge',
    unique_key=['id'],
) }}

with yelp_food_bronze as (
    select
        *,
        current_timestamp() as restaurant_added_dt
    from {{ source('raw', 'raw_yelp_restaurants') }}
)

select
    *
from yelp_food_bronze

{% if is_incremental() %}
    -- Exclude records that already exist in the target table
    where id not in (select id from {{ this }})
{% endif %}
