{{ config(
    materialized='incremental',
    incremental_strategy='merge',
    unique_key=['apt_zpid', 'apt_unit_number'],
    on_schema_change='fail',
    schema='gold',
    merge_update_columns=[
        'apt_zip_code',
        'apt_address',
        'apt_longitude',
        'apt_latitude',
        'apt_building_name',
        'apt_url',
        'apt_lot_id',
        'apt_image_url',
        'apt_property_type',
        'apt_bathroom_count',
        'apt_living_area',
        'apt_bedroom_count',
        'apt_rent',
        'updated_at'
    ]
) }}

WITH source_data AS (
    SELECT *
    FROM {{ ref('sl_zillow_apartments') }}
    WHERE LATITUDE IS NOT NULL
      AND LONGITUDE IS NOT NULL
      {% if is_incremental() %}
        -- Only select records updated since the last incremental run
        AND updated_at > (SELECT MAX(updated_at) FROM {{ this }})
      {% endif %}
)

SELECT 
    ZIPCODE AS apt_zip_code,
    ZPID AS apt_zpid,
    ADDRESS AS apt_address,
    LONGITUDE AS apt_longitude,
    LATITUDE AS apt_latitude,
    COALESCE(BUILDINGNAME, 'NotAvailable') AS apt_building_name,
    DETAILURL AS apt_url,
    COALESCE(LOTID, '99999999') AS apt_lot_id,
    IMGSRC AS apt_image_url,
    COALESCE(PROPERTYTYPE, 'NotAvailable') AS apt_property_type,

    COALESCE(
        BATHROOMS, 
        CASE 
            WHEN BEDS = 1 AND PRICE <= 2993.85 THEN 1
            WHEN BEDS = 1 AND PRICE > 2993.85 THEN 2
            WHEN BEDS = 2 AND PRICE <= 3514.29 THEN 1
            WHEN BEDS = 2 AND PRICE <= 4524.71 THEN 2
            WHEN BEDS = 2 AND PRICE > 4524.71 THEN 3
            WHEN BEDS = 3 AND PRICE <= 4400 THEN 1
            WHEN BEDS = 3 AND PRICE <= 6500 THEN 2
            WHEN BEDS = 3 AND PRICE > 6500 THEN 3
            WHEN BEDS = 4 THEN 2
            ELSE 1 
        END
    ) AS apt_bathroom_count,

    LIVINGAREA AS apt_living_area,
    BEDS AS apt_bedroom_count,
    PRICE AS apt_rent,
    COALESCE(UNIT, '99') AS apt_unit_number,
    apartment_added_dt,
    CURRENT_TIMESTAMP() AS updated_at
FROM source_data
