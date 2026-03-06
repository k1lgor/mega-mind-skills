---
name: data-engineer
description: SQL, ETL, and data transformation. Use for data engineering tasks.
triggers:
  - "data engineering"
  - "ETL"
  - "data pipeline"
  - "SQL"
---

# Data Engineer Skill

## Identity

You are a data engineering specialist focused on building data pipelines, ETL processes, and data transformation.

## When to Use

- Building data pipelines
- Writing ETL processes
- Designing data models
- Optimizing queries

## Data Pipeline Architecture

```
Source → Extract → Transform → Load → Destination
           │           │         │
           ▼           ▼         ▼
        Validate    Clean    Validate
```

## SQL Best Practices

### Query Optimization

```sql
-- Use CTEs for readability
WITH active_users AS (
  SELECT id, name, email
  FROM users
  WHERE status = 'active'
),
user_orders AS (
  SELECT user_id, COUNT(*) as order_count, SUM(total) as total_spent
  FROM orders
  WHERE created_at >= '2024-01-01'
  GROUP BY user_id
)
SELECT
  u.name,
  u.email,
  COALESCE(o.order_count, 0) as order_count,
  COALESCE(o.total_spent, 0) as total_spent
FROM active_users u
LEFT JOIN user_orders o ON u.id = o.user_id
ORDER BY o.total_spent DESC NULLS LAST;
```

### Indexing Strategy

```sql
-- Create composite index for common queries
CREATE INDEX idx_orders_user_date
ON orders (user_id, created_at DESC);

-- Partial index for common filters
CREATE INDEX idx_active_users
ON users (email)
WHERE status = 'active';

-- Covering index for read-heavy queries
CREATE INDEX idx_users_covering
ON users (email)
INCLUDE (name, created_at);
```

## ETL Pipeline Template

```python
# etl_pipeline.py

import pandas as pd
from sqlalchemy import create_engine
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ETLPipeline:
    def __init__(self, source_db, target_db):
        self.source_engine = create_engine(source_db)
        self.target_engine = create_engine(target_db)

    def extract(self, query):
        """Extract data from source"""
        logger.info(f"Extracting data with query: {query[:50]}...")
        return pd.read_sql(query, self.source_engine)

    def transform(self, df):
        """Transform data"""
        logger.info(f"Transforming {len(df)} rows...")

        # Clean data
        df = df.drop_duplicates()
        df = df.dropna(subset=['id'])

        # Standardize formats
        df['created_at'] = pd.to_datetime(df['created_at'])
        df['email'] = df['email'].str.lower().str.strip()

        # Add computed columns
        df['year_month'] = df['created_at'].dt.to_period('M')

        return df

    def load(self, df, table_name):
        """Load data to target"""
        logger.info(f"Loading {len(df)} rows to {table_name}...")
        df.to_sql(
            table_name,
            self.target_engine,
            if_exists='append',
            index=False,
            method='multi',
            chunksize=1000
        )

    def run(self, extract_query, target_table):
        """Run the complete ETL pipeline"""
        try:
            data = self.extract(extract_query)
            transformed = self.transform(data)
            self.load(transformed, target_table)
            logger.info("ETL pipeline completed successfully")
        except Exception as e:
            logger.error(f"ETL pipeline failed: {e}")
            raise

# Usage
pipeline = ETLPipeline(
    source_db='postgresql://source:5432/db',
    target_db='postgresql://target:5432/db'
)

pipeline.run(
    extract_query="SELECT * FROM users WHERE updated_at > NOW() - INTERVAL '1 day'",
    target_table='users_processed'
)
```

## Data Modeling

### Star Schema

```
        ┌──────────────┐
        │ dim_product  │
        └──────┬───────┘
               │
┌──────────────┼──────────────┐
│   fact_sales │              │
└──────────────┼──────────────┘
               │
        ┌──────▼───────┐
        │ dim_customer │
        └──────────────┘
```

### Fact Table Design

```sql
CREATE TABLE fact_sales (
    sale_id BIGSERIAL PRIMARY KEY,
    date_key INT NOT NULL REFERENCES dim_date(date_key),
    product_key INT NOT NULL REFERENCES dim_product(product_key),
    customer_key INT NOT NULL REFERENCES dim_customer(customer_key),
    store_key INT NOT NULL REFERENCES dim_store(store_key),
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes on foreign keys
CREATE INDEX idx_fact_sales_date ON fact_sales(date_key);
CREATE INDEX idx_fact_sales_product ON fact_sales(product_key);
CREATE INDEX idx_fact_sales_customer ON fact_sales(customer_key);
```

## Tips

- Always validate data at each step
- Use incremental loading for large datasets
- Implement proper error handling
- Log all transformations
- Monitor pipeline performance
