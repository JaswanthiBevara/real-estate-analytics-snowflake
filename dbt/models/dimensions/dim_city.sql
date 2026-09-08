{{ config(
    materialized='dim_city_merge'
) }}

SELECT
    CITY_ID,
    CITY_NAME,
    STATE,
    REGION,
    CITY_CLASS,
    GEO_TYPE,
    POPULATION,
    AREA_SQKM
FROM {{ source('raw', 'RAW_CITIES') }}
WHERE CITY_ID IS NOT NULL