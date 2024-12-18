with utilities as (
select * from 
{{ ref ('sl_boston_utilities')}}
),
zipcodes as (
    select * 
    from {{ ref ('zip_codes')}}
)

select * from 
utilities

where ZIP_CODE in (select * from zipcodes)
and electricity <> 0