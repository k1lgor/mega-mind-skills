---
name: data-analyst
description: Data visualization and insights (Python/SQL). Use for data analysis and reporting.
triggers:
  - "data analysis"
  - "data visualization"
  - "analytics"
  - "generate report"
---

# Data Analyst Skill

## Identity

You are a data analyst specialist focused on extracting insights from data through analysis and visualization.

## When to Use

- Creating data reports
- Building dashboards
- Analyzing trends
- Generating insights

## Analysis Workflow

### Step 1: Define Questions

```markdown
## Analysis Questions

1. What are the top 10 products by revenue?
2. What is the monthly trend in user signups?
3. Which marketing channels have the best conversion rate?
4. What is the churn rate by cohort?
```

### Step 2: Data Exploration

```python
import pandas as pd
import numpy as np

# Load and explore data
df = pd.read_csv('data.csv')

# Basic info
print(df.info())
print(df.describe())

# Check for missing values
print(df.isnull().sum())

# Check distributions
print(df['column'].value_counts())
```

### Step 3: Analysis

```python
# Aggregations
monthly_revenue = df.groupby(
    pd.to_datetime(df['date']).dt.to_period('M')
)['revenue'].sum()

# Metrics calculation
conversion_rate = df['converted'].sum() / len(df) * 100
avg_order_value = df['order_total'].mean()

# Cohort analysis
cohort_data = df.groupby(['cohort', 'period']).agg({
    'user_id': 'nunique',
    'revenue': 'sum'
}).reset_index()
```

### Step 4: Visualization

```python
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

# Time series
fig, ax = plt.subplots(figsize=(12, 6))
monthly_revenue.plot(kind='line', ax=ax)
ax.set_title('Monthly Revenue Trend')
ax.set_xlabel('Month')
ax.set_ylabel('Revenue ($)')
plt.tight_layout()
plt.savefig('monthly_revenue.png')

# Bar chart
fig, ax = plt.subplots(figsize=(10, 6))
top_products.plot(kind='barh', ax=ax)
ax.set_title('Top 10 Products by Revenue')
plt.tight_layout()
plt.savefig('top_products.png')
```

## SQL Analysis Queries

```sql
-- Cohort retention
WITH cohorts AS (
  SELECT
    user_id,
    DATE_TRUNC('month', created_at) as cohort_month
  FROM users
),
activity AS (
  SELECT DISTINCT
    user_id,
    DATE_TRUNC('month', activity_date) as activity_month
  FROM user_activity
)
SELECT
  c.cohort_month,
  COUNT(DISTINCT c.user_id) as cohort_size,
  COUNT(DISTINCT CASE WHEN a.activity_month = c.cohort_month + INTERVAL '1 month'
                       THEN c.user_id END) as month_1,
  COUNT(DISTINCT CASE WHEN a.activity_month = c.cohort_month + INTERVAL '2 months'
                       THEN c.user_id END) as month_2
FROM cohorts c
LEFT JOIN activity a ON c.user_id = a.user_id
GROUP BY c.cohort_month
ORDER BY c.cohort_month;

-- Funnel analysis
WITH funnel AS (
  SELECT
    COUNT(DISTINCT CASE WHEN event = 'page_view' THEN user_id END) as views,
    COUNT(DISTINCT CASE WHEN event = 'add_to_cart' THEN user_id END) as cart_adds,
    COUNT(DISTINCT CASE WHEN event = 'checkout_start' THEN user_id END) as checkouts,
    COUNT(DISTINCT CASE WHEN event = 'purchase' THEN user_id END) as purchases
  FROM events
  WHERE date >= '2024-01-01'
)
SELECT
  views,
  cart_adds,
  ROUND(cart_adds::numeric / views * 100, 2) as cart_rate,
  checkouts,
  ROUND(checkouts::numeric / cart_adds * 100, 2) as checkout_rate,
  purchases,
  ROUND(purchases::numeric / views * 100, 2) as conversion_rate
FROM funnel;
```

## Dashboard Metrics

```markdown
## Key Performance Indicators

### Revenue Metrics

| Metric              | Value      | Change |
| ------------------- | ---------- | ------ |
| Total Revenue       | $1,234,567 | +12.3% |
| Average Order Value | $85.50     | +5.2%  |
| Revenue per User    | $125.30    | +8.1%  |

### User Metrics

| Metric       | Value  | Change |
| ------------ | ------ | ------ |
| Active Users | 45,678 | +15.4% |
| New Signups  | 5,432  | +22.1% |
| Churn Rate   | 3.2%   | -0.5%  |

### Engagement Metrics

| Metric            | Value  | Change |
| ----------------- | ------ | ------ |
| Session Duration  | 8m 32s | +1.2%  |
| Pages per Session | 4.5    | +0.3%  |
| Bounce Rate       | 35.2%  | -2.1%  |
```

## Tips

- Start with clear questions
- Visualize data early
- Validate your findings
- Tell a story with data
- Make insights actionable
