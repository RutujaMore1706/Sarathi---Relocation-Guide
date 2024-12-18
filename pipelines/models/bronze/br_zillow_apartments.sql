{{ config(
    materialized='incremental',
    incremental_strategy='merge',
    unique_key='zpid',
    merge_update_columns=[
        'address',
        'detailurl',
        'lotid',
        'imgsrc',
        'price',
        'zip',
        'buildingname',
        'propertytype',
        'bathrooms',
        'bedrooms',
        'livingarea',
        'longitude',
        'latitude',
        'unit',
        'units',
        'apartment_added_dt',
        'updated_at'
    ],
    post_hook="TRUNCATE TABLE raw.raw_new_zillow_apartments"
) }}

WITH daily_data AS (
    SELECT
        zpid,
        address,
        detailurl,
        lotid,
        imgsrc,
        price,
        zip,
        buildingname,
        propertytype,
        bathrooms,
        bedrooms,
        livingarea,
        longitude,
        latitude,
        unit,
        units,
        apartment_added_dt,
        CURRENT_TIMESTAMP() AS updated_at
    FROM {{ source('raw', 'raw_new_zillow_apartments') }}
),

existing_data AS (
    SELECT
        zpid,
        address,
        detailurl,
        lotid,
        imgsrc,
        price,
        zip,
        buildingname,
        propertytype,
        bathrooms,
        bedrooms,
        livingarea,
        longitude,
        latitude,
        unit,
        units,
        apartment_added_dt,
        updated_at
    FROM {{ this }}
),

merged_data AS (
    SELECT
        COALESCE(daily.zpid, existing.zpid) AS zpid,
        COALESCE(daily.address, existing.address) AS address,
        COALESCE(daily.detailurl, existing.detailurl) AS detailurl,
        COALESCE(daily.lotid, existing.lotid) AS lotid,
        COALESCE(daily.imgsrc, existing.imgsrc) AS imgsrc,
        COALESCE(daily.price, existing.price) AS price,
        COALESCE(daily.zip, existing.zip) AS zip,
        COALESCE(daily.buildingname, existing.buildingname) AS buildingname,
        COALESCE(daily.propertytype, existing.propertytype) AS propertytype,
        COALESCE(daily.bathrooms, existing.bathrooms) AS bathrooms,
        COALESCE(daily.bedrooms, existing.bedrooms) AS bedrooms,
        COALESCE(daily.livingarea, existing.livingarea) AS livingarea,
        COALESCE(daily.longitude, existing.longitude) AS longitude,
        COALESCE(daily.latitude, existing.latitude) AS latitude,
        COALESCE(daily.unit, existing.unit) AS unit,
        COALESCE(daily.units, existing.units) AS units,

        CASE 
            WHEN existing.zpid IS NULL AND daily.zpid IS NOT NULL THEN daily.apartment_added_dt
            WHEN existing.zpid IS NOT NULL AND daily.zpid IS NOT NULL THEN existing.apartment_added_dt
            WHEN existing.zpid IS NOT NULL AND daily.zpid IS NULL THEN existing.apartment_added_dt
            ELSE NULL
        END AS apartment_added_dt,

        CASE
            WHEN existing.zpid IS NULL AND daily.zpid IS NOT NULL THEN daily.updated_at  -- New record
            WHEN existing.zpid IS NOT NULL AND daily.zpid IS NOT NULL THEN daily.updated_at  -- Updated record
            WHEN existing.zpid IS NOT NULL AND daily.zpid IS NULL THEN existing.updated_at  -- Unchanged record
            ELSE NULL
        END AS updated_at
    FROM existing_data existing
    FULL OUTER JOIN daily_data daily
        ON existing.zpid = daily.zpid
)

SELECT *
FROM merged_data
