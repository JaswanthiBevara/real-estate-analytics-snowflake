{{ config(
    materialized='incremental',
    unique_key=['TXN_ID', 'TXN_LINE_ID'],
    incremental_strategy='merge'
) }}

WITH latest_transactions AS (

    SELECT
        TXN_ID,
        TXN_LINE_ID,
        TXN_DATE,
        PROPERTY_ID,
        CITY_ID,
        DEVELOPER_ID,
        BUYER_SEGMENT,
        LIST_PRICE_LAKHS,
        DISCOUNT_PCT,
        SALE_PRICE_LAKHS,
        LOAN_REQUIRED,
        SALES_CHANNEL,
        TXN_STATUS,
        UPDATED_AT,
        LOAD_TS,
        SOURCE_FILE_NAME
    FROM {{ source('raw', 'RAW_TRANSACTIONS') }}
    WHERE TXN_ID IS NOT NULL
      AND TXN_LINE_ID IS NOT NULL

    QUALIFY ROW_NUMBER() OVER (
        PARTITION BY TXN_ID, TXN_LINE_ID
        ORDER BY UPDATED_AT DESC, LOAD_TS DESC, SOURCE_FILE_NAME DESC
    ) = 1
)

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
FROM latest_transactions t
LEFT JOIN {{ ref('dim_date') }} d
    ON d.DATE_VALUE = t.TXN_DATE
LEFT JOIN {{ ref('dim_city') }} c
    ON c.CITY_ID = t.CITY_ID
LEFT JOIN {{ ref('dim_developer') }} dev
    ON dev.DEVELOPER_ID = t.DEVELOPER_ID
   AND dev.IS_CURRENT = TRUE
LEFT JOIN {{ ref('dim_property') }} p
    ON p.PROPERTY_ID = t.PROPERTY_ID
   AND p.IS_CURRENT = TRUE