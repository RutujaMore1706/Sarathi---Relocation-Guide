WITH filtered_data AS (
    SELECT 
        EnergyTypeName,
        InvoiceDate,
        TotalCost,
        Zip,
        _ingest_datetime
    FROM 
        {{ref ('br_boston_utilities')}}
    WHERE 
        InvoiceDate >= '2023-01-01'
),
cost_with_bounds AS (
    SELECT 
        *,
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY TotalCost) OVER (PARTITION BY Zip, EnergyTypeName) AS Q1,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY TotalCost) OVER (PARTITION BY Zip, EnergyTypeName) AS Q3
    FROM 
        filtered_data
),
outlier_removed AS (
    SELECT 
        *
    FROM 
        cost_with_bounds
    WHERE 
        TotalCost >= (Q1 - 1.5 * (Q3 - Q1)) 
        AND TotalCost <= (Q3 + 1.5 * (Q3 - Q1))
),
monthly_cost AS (
    SELECT 
        TO_CHAR(InvoiceDate, 'YYYY-MM') AS YearMonth,
        Zip,
        EnergyTypeName,
        SUM(TotalCost) AS TotalCost
    FROM 
        outlier_removed
    GROUP BY 
        YearMonth, Zip, EnergyTypeName
),
average_monthly_cost AS (
    SELECT 
        Zip,
        EnergyTypeName,
        AVG(TotalCost) AS AverageTotalCost
    FROM 
        monthly_cost
    GROUP BY 
        Zip, EnergyTypeName
),
pivot_table AS (
    SELECT 
        Zip,
        COALESCE(SUM(CASE WHEN EnergyTypeName = 'Oil' THEN AverageTotalCost END), 0) AS Oil,
        COALESCE(SUM(CASE WHEN EnergyTypeName = 'Electric' THEN AverageTotalCost END), 0) AS Electric,
        COALESCE(SUM(CASE WHEN EnergyTypeName = 'Natural Gas' THEN AverageTotalCost END), 0) AS NaturalGas,
        COALESCE(SUM(CASE WHEN EnergyTypeName = 'Steam' THEN AverageTotalCost END), 0) AS Steam,
        COALESCE(SUM(CASE WHEN EnergyTypeName = 'Stormwater' THEN AverageTotalCost END), 0) AS Stormwater,
        COALESCE(SUM(CASE WHEN EnergyTypeName = 'Water' THEN AverageTotalCost END), 0) AS Water
    FROM 
        average_monthly_cost
    GROUP BY 
        Zip
)
SELECT 
    left(Zip,5) as ZIP_CODE,
    ROUND(Electric,2) as Electricity,
    ROUND(NaturalGas,2) as Gas,
    ROUND(Steam,2) as Heat,
    ROUND(Water,2) as Water,
    UNIFORM(200, 500, RANDOM()) AS TotalCost  
FROM 
    pivot_table