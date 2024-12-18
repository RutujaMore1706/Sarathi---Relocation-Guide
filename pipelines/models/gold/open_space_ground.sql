with grounds as (
select * from 
{{ ref ('sl_boston_openspace')}}
),
zipcodes as (
    select * 
    from {{ ref ('zip_codes')}}
)

select * from 
grounds
where ZIP_CODE in (select * from zipcodes)