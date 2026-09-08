{{ config(
    materialized='dim_developer_scd2'
) }}

SELECT
    DEVELOPER_ID,
    DEVELOPER_NAME,
    DEVELOPER_TIER,
    FOCUS_SEGMENT,
    HQ_CITY,
    HQ_STATE,
    STATUS,
    HASH_DIFF,
    DBT_VALID_FROM,
    DBT_VALID_TO
FROM {{ ref('snap_developer') }}

