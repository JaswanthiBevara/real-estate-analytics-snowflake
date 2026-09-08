{{ config(
    materialized='dim_property_scd2'
) }}

SELECT
    PROPERTY_ID,
    PROPERTY_TYPE,
    SEGMENT,
    BHK,
    AREA_SQFT,
    STATUS,
    AMENITY_TIER,
    POSSESSION_YEAR,
    HASH_DIFF,
    DBT_VALID_FROM,
    DBT_VALID_TO
FROM {{ ref('snap_property') }}