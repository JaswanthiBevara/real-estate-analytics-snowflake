{% materialization dim_property_scd2, adapter='snowflake' %}

    {% set target_relation = this %}

    {% call statement('main') %}

        MERGE INTO {{ target_relation }} AS target

        USING (

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

        ) AS source

        ON target.PROPERTY_ID = source.PROPERTY_ID
        AND target.EFF_START_TS = source.DBT_VALID_FROM

        WHEN MATCHED THEN
            UPDATE SET
                target.PROPERTY_TYPE = source.PROPERTY_TYPE,
                target.SEGMENT = source.SEGMENT,
                target.BHK = source.BHK,
                target.AREA_SQFT = source.AREA_SQFT,
                target.STATUS = source.STATUS,
                target.AMENITY_TIER = source.AMENITY_TIER,
                target.POSSESSION_YEAR = source.POSSESSION_YEAR,
                target.EFF_END_TS = COALESCE(
                    source.DBT_VALID_TO,
                    '9999-12-31'::TIMESTAMP_NTZ
                ),
                target.IS_CURRENT = CASE
                    WHEN source.DBT_VALID_TO IS NULL THEN TRUE
                    ELSE FALSE
                END,
                target.HASH_DIFF = source.HASH_DIFF

        WHEN NOT MATCHED THEN
            INSERT
            (
                PROPERTY_ID,
                PROPERTY_TYPE,
                SEGMENT,
                BHK,
                AREA_SQFT,
                STATUS,
                AMENITY_TIER,
                POSSESSION_YEAR,
                HASH_DIFF,
                EFF_START_TS,
                EFF_END_TS,
                IS_CURRENT
            )
            VALUES
            (
                source.PROPERTY_ID,
                source.PROPERTY_TYPE,
                source.SEGMENT,
                source.BHK,
                source.AREA_SQFT,
                source.STATUS,
                source.AMENITY_TIER,
                source.POSSESSION_YEAR,
                source.HASH_DIFF,
                source.DBT_VALID_FROM,
                COALESCE(
                    source.DBT_VALID_TO,
                    '9999-12-31'::TIMESTAMP_NTZ
                ),
                CASE
                    WHEN source.DBT_VALID_TO IS NULL THEN TRUE
                    ELSE FALSE
                END
            );

    {% endcall %}

    {{ return({'relations': [target_relation]}) }}

{% endmaterialization %}