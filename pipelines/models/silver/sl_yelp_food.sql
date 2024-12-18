{{ config(
    materialized='incremental',
    incremental_strategy='merge',
    unique_key=['restaurant_id'],
    on_schema_change='fail',
    schema='silver'
) }}

with yelp_food as (
    select
        id as restaurant_id,
        name as restaurant_name,
            CASE  
                WHEN (categories ILIKE '%mexican%' OR categories ILIKE '%tacos%') THEN 'Mexican'
                WHEN categories ILIKE '%korean%' THEN 'Korean'
                WHEN (categories ILIKE '%india%' OR categories ILIKE '%pakistan%') THEN 'Indian'
                ELSE 'Other'
            END AS cuisine,

        url,
        image_url,
        price,
        rating,
        current_timestamp() as processed_dt,
        restaurant_added_dt,
        -- Parse the coordinates column to extract latitude and longitude
        try_cast(split_part(split_part(coordinates, ':', 2), ',', 1) as float) as latitude,
        try_cast(split_part(split_part(split_part(coordinates, ':', 3), '}', 1), ',', 1) as float) as longitude,
        -- Convert 'location' string to valid JSON
        try_parse_json(
            replace(
                replace(location, '''', '"'),
                'None',
                'null'
            )
        ) as json_location
    from {{ ref('br_yelp_food') }}  -- Reference the bronze model
    {% if is_incremental() %}
        -- Only process records that are new or updated since the last run
        where restaurant_added_dt > (
            select coalesce(max(restaurant_added_dt), '1970-01-01') from {{ this }}
        )
    {% endif %}
)

select
    restaurant_id,
    restaurant_name,
    cuisine,
    url,
    image_url,
    price,
    rating,
    latitude,
    longitude,
    array_to_string(
        json_location:"display_address",
        ', '
    ) as address,
    json_location:"zip_code"::string as zip_code,
    restaurant_added_dt,
    processed_dt
from yelp_food
