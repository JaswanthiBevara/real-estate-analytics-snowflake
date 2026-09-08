{% snapshot snap_developer %}

{{
    config(
        unique_key='DEVELOPER_ID',
        strategy='check',
        check_cols=[
            'DEVELOPER_TIER',
            'FOCUS_SEGMENT',
            'HQ_CITY',
            'HQ_STATE',
            'STATUS'
        ]
    )
}}

SELECT
    DEVELOPER_ID,
    DEVELOPER_NAME,
    DEVELOPER_TIER,
    FOCUS_SEGMENT,
    HQ_CITY,
    HQ_STATE,
    STATUS,
    MD5(
        COALESCE(DEVELOPER_TIER, '') || '|' ||
        COALESCE(FOCUS_SEGMENT, '') || '|' ||
        COALESCE(HQ_CITY, '') || '|' ||
        COALESCE(HQ_STATE, '') || '|' ||
        COALESCE(STATUS, '')
    ) AS HASH_DIFF,
    CURRENT_TIMESTAMP() AS LOAD_TS
FROM {{ source('raw', 'RAW_DEVELOPERS') }}
WHERE DEVELOPER_ID IS NOT NULL

{% endsnapshot %}