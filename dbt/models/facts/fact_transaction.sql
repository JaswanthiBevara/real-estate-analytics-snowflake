{{ config(
    materialized='incremental',
    unique_key=['TXN_ID', 'TXN_LINE_ID'],
    incremental_strategy='merge'
) }}

SELECT
    t.TXN_ID,
    t.TXN_LINE_ID,

    d.SK_DATE AS SK_TXN_DATE,
    c.SK_CITY,
    dev.SK_DEVELOPER,
    p.SK_PROPERTY,

    t.LIST_PRICE_LAKHS AS LIST_PRICE,
    t.SALE_PRICE_LAKHS AS SALE_PRICE,
    t.DISCOUNT_PCT,
    t.BUYER_SEGMENT,
    t.SALES_CHANNEL AS CHANNEL,
    t.TXN_STATUS,
    t.LOAN_REQUIRED AS LOAN_REQ

FROM {{ source('raw', 'RAW_TRANSACTIONS') }} AS t

LEFT JOIN {{ ref('dim_date') }} AS d
    ON d.DATE_VALUE = t.TXN_DATE

LEFT JOIN {{ ref('dim_city') }} AS c
    ON c.CITY_ID = t.CITY_ID

LEFT JOIN {{ ref('dim_developer') }} AS dev
    ON dev.DEVELOPER_ID = t.DEVELOPER_ID
   AND dev.IS_CURRENT = TRUE

LEFT JOIN {{ ref('dim_property') }} AS p
    ON p.PROPERTY_ID = t.PROPERTY_ID
   AND p.IS_CURRENT = TRUE

WHERE t.TXN_ID IS NOT NULL
  AND t.TXN_LINE_ID IS NOT NULL