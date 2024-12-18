with groups as (
select * from 
{{ ref ('sl_boston_groups')}}
),
zipcodes as (
    select * 
    from {{ ref ('zip_codes')}}
)

select * from 
groups 
