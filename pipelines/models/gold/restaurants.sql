{{ config(
    materialized='incremental',
    incremental_strategy='merge',
    unique_key=['restaurant_id'],
    on_schema_change='fail',
    schema='gold'
) }}

with restaurants as (
select * from 
{{ ref ('sl_yelp_food')}}
),
zipcodes as (
    select * 
    from {{ ref ('zip_codes')}}
)

select * from 
restaurants 
where ZIP_CODE in (select * from zipcodes)
