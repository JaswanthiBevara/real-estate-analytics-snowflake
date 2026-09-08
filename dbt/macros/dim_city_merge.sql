{% materialization dim_city_merge, adapter='snowflake' %}

    {% set target_relation = this %}

    {% call statement('main') %}
        MERGE INTO {{ target_relation }} AS target
        USING (
            {{ sql }}
        ) AS source
        ON target.CITY_ID = source.CITY_ID

        WHEN MATCHED THEN
            UPDATE SET
                target.CITY_NAME  = source.CITY_NAME,
                target.STATE      = source.STATE,
                target.REGION     = source.REGION,
                target.CITY_CLASS = source.CITY_CLASS,
                target.GEO_TYPE   = source.GEO_TYPE,
                target.POPULATION = source.POPULATION,
                target.AREA_SQKM  = source.AREA_SQKM

        WHEN NOT MATCHED THEN
            INSERT
            (
                CITY_ID,
                CITY_NAME,
                STATE,
                REGION,
                CITY_CLASS,
                GEO_TYPE,
                POPULATION,
                AREA_SQKM
            )
            VALUES
            (
                source.CITY_ID,
                source.CITY_NAME,
                source.STATE,
                source.REGION,
                source.CITY_CLASS,
                source.GEO_TYPE,
                source.POPULATION,
                source.AREA_SQKM
            )
    {% endcall %}

    {{ return({'relations': [target_relation]}) }}

{% endmaterialization %}