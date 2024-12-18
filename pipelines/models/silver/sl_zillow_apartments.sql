{{ config(
    materialized='incremental',
    incremental_strategy='merge',
    unique_key=['zpid', 'unit'],
    on_schema_change='fail',
    schema='silver',
    merge_update_columns=[
        'zipcode',
        'zpid',
        'address',
        'longitude',
        'latitude',
        'buildingname',
        'detailurl',
        'lotid',
        'imgsrc',
        'propertytype',
        'bathrooms',
        'livingarea',
        'beds',
        'price',
        'updated_at'  
    ]
) }}

WITH parsed_data AS (
    SELECT
        LPAD(ZIP, 5, '0') AS ZIPCODE,
        ZPID,
        PARSE_JSON(UNITS) AS units_json,
        ADDRESS,
        LONGITUDE,
        LATITUDE,
        BUILDINGNAME,
        CONCAT('https://www.zillow.com/', DETAILURL) AS DETAILURL,
        LOTID,
        IMGSRC,
        PROPERTYTYPE,
        BATHROOMS,
        LIVINGAREA,
        BEDROOMS,
        PRICE,
        apartment_added_dt,
        updated_at
    FROM {{ ref('br_zillow_apartments') }}
    -- Incremental filter: only select rows that have updated_at greater than the max in this table
    {% if is_incremental() %}
    WHERE updated_at > (SELECT MAX(updated_at) FROM {{ this }})
      AND UNITS IS NOT NULL AND UNITS != '[]'
    {% else %}
    WHERE UNITS IS NOT NULL AND UNITS != '[]'
    {% endif %}
),

flattened_data AS (
    SELECT
        pd.ZIPCODE,
        pd.ZPID,
        u.value AS unit_json,
        pd.ADDRESS,
        pd.LONGITUDE,
        pd.LATITUDE,
        pd.BUILDINGNAME,
        pd.DETAILURL,
        pd.LOTID,
        pd.IMGSRC,
        pd.PROPERTYTYPE,
        pd.BATHROOMS,
        pd.LIVINGAREA,
        pd.BEDROOMS,
        pd.PRICE,
        pd.apartment_added_dt,
        pd.updated_at,
        ROW_NUMBER() OVER (PARTITION BY pd.ADDRESS ORDER BY pd.ZPID) AS UNIT
    FROM parsed_data pd,
    LATERAL FLATTEN(input => pd.units_json) u
),

units_not_null AS (
    SELECT
        ZIPCODE,
        ZPID,
        ADDRESS,
        LONGITUDE,
        LATITUDE,
        BUILDINGNAME,
        DETAILURL,
        LOTID,
        IMGSRC,
        PROPERTYTYPE,
        BATHROOMS,
        LIVINGAREA,
        TO_NUMBER(unit_json:beds::STRING)::INT AS BEDS,
        TO_NUMBER(REGEXP_REPLACE(unit_json:price::STRING, '[^0-9]', ''))::INT AS PRICE,
        COALESCE(UNIT, 99) AS UNIT,
        apartment_added_dt,
        updated_at
    FROM flattened_data
),

units_null AS (
    SELECT
        LPAD(ZIP, 5, '0') AS ZIPCODE,
        ZPID,
        ADDRESS,
        LONGITUDE,
        LATITUDE,
        BUILDINGNAME,
        CONCAT('https://www.zillow.com/', DETAILURL) AS DETAILURL,
        LOTID,
        IMGSRC,
        PROPERTYTYPE,
        BATHROOMS,
        LIVINGAREA,
        TO_NUMBER(BEDROOMS)::INT AS BEDS,
        TO_NUMBER(PRICE)::INT AS PRICE,
        COALESCE(
            TO_NUMBER(REGEXP_REPLACE(UNITS, '[^0-9]', '')), 99
        )::INT AS UNIT,
        apartment_added_dt,
        updated_at
    FROM {{ ref('br_zillow_apartments') }}
    {% if is_incremental() %}
    WHERE updated_at > (SELECT MAX(updated_at) FROM {{ this }})
      AND (UNITS IS NULL OR UNITS = '[]')
    {% else %}
    WHERE UNITS IS NULL OR UNITS = '[]'
    {% endif %}
)

SELECT * FROM units_not_null
UNION ALL
SELECT * FROM units_null
