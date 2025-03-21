# Data Pipeline

This document explains the continuous data processing workflow that connects NLP processing, data source selection, SQL query execution, and data cleansing into a unified pipeline.

## Architecture Overview

The data pipeline consists of the following components:

1. **NLP Processing** (`NLPAgent`): Analyzes natural language queries to extract intent, keywords, and query structure.
2. **Data Source Selection** (`SourceRouter`): Routes requests to appropriate data sources based on NLP analysis.
3. **SQL Query Generation and Execution** (`SQLExecutor`): Generates and executes SQL queries based on the NLP output.
4. **Data Cleansing and Analysis** (`DataCleanser`): Processes query results to generate summaries and insights.
5. **Data Visualization** (`DiagramGenerator`): Creates appropriate visualizations based on the data characteristics.

## Component Details

### 1. NLP Processing

The `NLPAgent` class analyzes user queries to determine:
- **Triggers**: What kind of data sources to query (e.g., "db", "arp", "dork")
- **Keywords**: Important search terms extracted from the query
- **Raw Query**: The original user query for context preservation

Example:
```
Input: "纽约市空气质量数据分析"
Output: 
  - Triggers: ["db"]
  - Keywords: ["纽约市", "空气质量"]
  - Raw Query: "纽约市空气质量数据分析"
```

### 2. Data Source Selection

The `SourceRouter` class routes data requests to appropriate handlers based on triggers identified by NLP:
- "db" trigger routes to database queries
- "arp" trigger routes to network scanning functions
- "dork" trigger routes to web search functions

### 3. SQL Query Generation and Execution

The `SQLExecutor` class:
- Generates appropriate SQL queries based on the extracted keywords and context
- Uses LLMs to craft optimal SQL queries for the specific database schema
- Falls back to conventional query methods if LLM generation fails
- Executes the query and returns structured results

### 4. Data Cleansing and Analysis

The `DataCleanser` class processes query results to:
- Generate statistical summaries of the data
- Extract key information and patterns
- Draw initial conclusions from the data
- Prepare data for visualization

### 5. Data Visualization

The `DiagramGenerator` class:
- Automatically determines the most appropriate chart type based on data characteristics
- Generates interactive visualizations using Plotly
- Provides embeddable HTML for web integration

## Usage Example

```python
from data_pipeline import DataPipeline

# Initialize the pipeline with database schemas
db_schemas = [
    "空气质量表：城市(city), PM2.5值(pm25), 监测日期(date)",
    "电车数据表：地区(region), 车辆数(count), 充电桩(chargers)"
]

# Create the pipeline
pipeline = DataPipeline(db_schemas)

# Process a user query
result = pipeline.process_query("查询纽约市的PM2.5水平")

# Access the results
if result["status"] == "success":
    # Get cleansed data and summary
    cleansed_data = result["cleansed_data"]
    
    # Get visualization
    visualization = result["visualization"]
    
    # Get raw query results
    query_results = result["final_results"]
```

## Data Flow

The complete data flow through the pipeline is:

1. User submits a natural language query
2. NLP processing extracts intent and keywords
3. Source router determines which data sources to query
4. SQL generator creates and executes appropriate queries
5. Data cleanser processes and analyzes the results
6. Visualization generator creates appropriate charts
7. Final results are returned with all intermediate information

## Requirements

The pipeline requires the following dependencies:
- pandas
- plotly
- sqlite3
- A compatible LLM API (e.g., OpenAI, DeepSeek)

## File Structure

```
.
├── NLP.py                # Natural Language Processing component
├── choose_data.py        # Data source selection component  
├── sql_query.py          # SQL generation and execution component
├── cleansing_db.py       # Data cleansing and analysis component
├── diagram.py            # Data visualization component
└── data_pipeline.py      # Unified pipeline implementation
``` 