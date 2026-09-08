{# {{ config( #}
    -- materialized='table'
-- ) }}

-- SELECT DISTINCT

    -- TO_NUMBER(
        {# TO_CHAR(TXN_DATE, 'YYYYMMDD') #}
    -- ) AS SK_DATE,

    -- TXN_DATE AS DATE_VALUE,

    -- YEAR(TXN_DATE) AS YEAR,

    {# 'Q' || QUARTER(TXN_DATE) AS QUARTER, #}

    -- MONTH(TXN_DATE) AS MONTH,

    -- WEEKISO(TXN_DATE) AS WEEK_OF_YEAR,

    -- DAYOFWEEKISO(TXN_DATE) IN (6, 7) AS IS_WEEKEND

{# FROM {{ source('raw', 'RAW_TRANSACTIONS') }} #}

-- WHERE TXN_DATE IS NOT NULL


{{ config(
    materialized='incremental',
    unique_key='DATE_VALUE',
    incremental_strategy='merge'
) }}

SELECT DISTINCT
    TO_NUMBER(TO_CHAR(TXN_DATE, 'YYYYMMDD')) AS SK_DATE,
    TXN_DATE AS DATE_VALUE,
    YEAR(TXN_DATE) AS YEAR,
    'Q' || QUARTER(TXN_DATE) AS QUARTER,
    MONTH(TXN_DATE) AS MONTH,
    WEEKISO(TXN_DATE) AS WEEK_OF_YEAR,
    DAYOFWEEKISO(TXN_DATE) IN (6, 7) AS IS_WEEKEND
FROM {{ source('raw', 'RAW_TRANSACTIONS') }}
WHERE TXN_DATE IS NOT NULL

{% if is_incremental() %}
    AND TXN_DATE > (
        SELECT COALESCE(MAX(DATE_VALUE), '1900-01-01')
        FROM {{ this }}
    )
{% endif %}