{% snapshot snap_property %}

{{
    config(
        unique_key='PROPERTY_ID',
        strategy='check',
        check_cols=[
            'PROPERTY_TYPE',
            'SEGMENT',
            'BHK',
            'AREA_SQFT',
            'POSSESSION_YEAR',
            'STATUS',
            'AMENITY_TIER'
        ]
    )
}}

SELECT
    PROPERTY_ID,
    PROPERTY_TYPE,
    SEGMENT,
    BHK,
    AREA_SQFT,
    PROJECT_STATUS AS STATUS,
    AMENITY_TIER,
    POSSESSION_YEAR,

    MD5(
        COALESCE(PROPERTY_TYPE, '') || '|' ||
        COALESCE(SEGMENT, '') || '|' ||
        COALESCE(BHK::VARCHAR, '') || '|' ||
        COALESCE(AREA_SQFT::VARCHAR, '') || '|' ||
        COALESCE(POSSESSION_YEAR::VARCHAR, '') || '|' ||
        COALESCE(PROJECT_STATUS, '') || '|' ||
        COALESCE(AMENITY_TIER, '')
    ) AS HASH_DIFF,

    CURRENT_TIMESTAMP() AS LOAD_TS

FROM {{ source('raw', 'RAW_PROPERTIES') }}
WHERE PROPERTY_ID IS NOT NULL

{% endsnapshot %}