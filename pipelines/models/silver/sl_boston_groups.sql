{{ config ( materialized = 'view')}}
WITH events_split AS (
    SELECT
        NAME,
        DESCRIPTION,
        LINK,
        CITY,
        ZIP,
        MEMBERCOUNT,
        TOPICCATEGORY,
        TOPICS,
        PASTEVENTS,
        ADDED_DT,
        SPLIT(PASTEVENTS, ';') AS event_list
    FROM {{ ref ('br_boston_groups') }}
),
flattened_events AS (
    SELECT
        NAME,
        DESCRIPTION,
        LINK,
        CITY,
        ZIP,
        MEMBERCOUNT,
        TOPICCATEGORY,
        TOPICS,
        PASTEVENTS,
        ADDED_DT,
        TRIM(VALUE) AS event
    FROM events_split,
    LATERAL FLATTEN(INPUT => event_list)
),
extracted_events AS (
    SELECT
        NAME,
        DESCRIPTION,
        LINK,
        CITY,
        ZIP,
        MEMBERCOUNT,
        TOPICCATEGORY,
        TOPICS,
        PASTEVENTS,
        ADDED_DT,
        -- Extract event name before '(ID:'
        REGEXP_SUBSTR(event, '^(.*?)\\s*\\(ID:') AS event_name_raw,
        -- Extract date in YYYY-MM-DD format
        REGEXP_SUBSTR(event, 'Date:\\s*([\\d-]+)', 1, 1, 'e', 1) AS event_date
    FROM flattened_events
),
cleaned_events AS (
    SELECT
        NAME,
        DESCRIPTION,
        LINK,
        CITY,
        ZIP,
        MEMBERCOUNT,
        TOPICCATEGORY,
        TOPICS,
        PASTEVENTS,
        ADDED_DT,
        -- Remove duplicate parentheses
        REGEXP_REPLACE(event_name_raw, '\\s*\\([^)]*\\)\\s*', '') AS event_name_no_parentheses,
        event_date
    FROM extracted_events
),
final_events AS (
    SELECT
        NAME,
        DESCRIPTION,
        LINK,
        CITY,
        ZIP,
        MEMBERCOUNT,
        TOPICCATEGORY,
        TOPICS,
        PASTEVENTS,
        ADDED_DT,
        -- Remove emojis and special characters
        REGEXP_REPLACE(event_name_no_parentheses, '[^\\w\\s.,!?-]', '') AS cleaned_event_name,
        event_date
    FROM cleaned_events
),
aggregated_events AS (
    SELECT
        NAME,
        DESCRIPTION,
        LINK,
        CITY,
        ZIP,
        MEMBERCOUNT,
        TOPICCATEGORY,
        TOPICS,
        PASTEVENTS,
        ADDED_DT,
        -- Combine cleaned event names and dates
        LISTAGG(
            CASE 
                WHEN cleaned_event_name IS NOT NULL THEN
                    cleaned_event_name || COALESCE('(Date: ' || event_date || ')', '')
                ELSE ''
            END,
            ', '
        ) AS CLEANED_PASTEVENTS
    FROM final_events
    GROUP BY
        NAME, DESCRIPTION, LINK, CITY, ZIP, MEMBERCOUNT,
        TOPICCATEGORY, TOPICS, PASTEVENTS, ADDED_DT
)
SELECT
    NAME,
    regexp_replace(description, '<[^>]+>', '') as Group_Description,
    link as GROUP_MEETUP_URL,
    CITY,
    ZIP as ZIP_CODE,
    MEMBERCOUNT,
    TOPICS as Category,
    CLEANED_PASTEVENTS as Past_Events,
    ADDED_DT,
    
FROM aggregated_events
