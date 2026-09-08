{% materialization dim_developer_scd2, adapter='snowflake' %}

    {% set target_relation = this %}

    {% call statement('main') %}

        MERGE INTO {{ target_relation }} AS target

        USING (

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

        ) AS source

        ON target.DEVELOPER_ID = source.DEVELOPER_ID
        AND target.EFF_START_TS = source.DBT_VALID_FROM

        WHEN MATCHED THEN
            UPDATE SET
                target.DEVELOPER_NAME = source.DEVELOPER_NAME,
                target.DEVELOPER_TIER = source.DEVELOPER_TIER,
                target.FOCUS_SEGMENT = source.FOCUS_SEGMENT,
                target.HQ_CITY = source.HQ_CITY,
                target.HQ_STATE = source.HQ_STATE,
                target.STATUS = source.STATUS,
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
                DEVELOPER_ID,
                DEVELOPER_NAME,
                DEVELOPER_TIER,
                FOCUS_SEGMENT,
                HQ_CITY,
                HQ_STATE,
                STATUS,
                EFF_START_TS,
                EFF_END_TS,
                IS_CURRENT,
                HASH_DIFF
            )
            VALUES
            (
                source.DEVELOPER_ID,
                source.DEVELOPER_NAME,
                source.DEVELOPER_TIER,
                source.FOCUS_SEGMENT,
                source.HQ_CITY,
                source.HQ_STATE,
                source.STATUS,
                source.DBT_VALID_FROM,
                COALESCE(
                    source.DBT_VALID_TO,
                    '9999-12-31'::TIMESTAMP_NTZ
                ),
                CASE
                    WHEN source.DBT_VALID_TO IS NULL THEN TRUE
                    ELSE FALSE
                END,
                source.HASH_DIFF
            );

    {% endcall %}

    {{ return({'relations': [target_relation]}) }}

{% endmaterialization %}