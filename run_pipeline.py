#!/usr/bin/env python3
"""
Demo script to run the complete data pipeline with a real-world example.
This script connects NLP-->choose_data-->sql_query-->cleansing_db in a continuous workflow.
"""

from data_pipeline import DataPipeline
import json
import pandas as pd
import time

def print_separator(message):
    """Print a separator with a message."""
    print(f"\n{'='*20} {message} {'='*20}")

def print_json(data):
    """Print JSON data in a formatted way."""
    print(json.dumps(data, indent=2, ensure_ascii=False))

def main():
    # Define database schemas for NLP processing
    db_schemas = [
        "空气质量表：城市(city), PM2.5值(pm25), 臭氧(ozone), 监测日期(date), 地点名称(place_name), 指标ID(indicator_id)",
        "电车数据表：地区(region), 车辆数(count), 充电桩(chargers)"
    ]
    
    # Initialize the data pipeline
    print_separator("INITIALIZING PIPELINE")
    pipeline = DataPipeline(db_schemas)
    print("Pipeline components initialized successfully!")
    
    # Define a natural language query
    query = "查询Upper East Side-Gramercy地区的臭氧(O3)水平数据"
    print_separator("USER QUERY")
    print(f"Query: {query}")
    
    # Start the timer to measure performance
    start_time = time.time()
    
    # Process the query through the entire pipeline
    print_separator("PROCESSING PIPELINE")
    print("Starting pipeline processing...")
    
    result = pipeline.process_query(query)
    
    # Calculate execution time
    execution_time = time.time() - start_time
    
    # Display results
    print_separator("PIPELINE RESULTS")
    
    if result["status"] == "success":
        print("Pipeline execution successful!")
        print(f"Execution time: {execution_time:.2f} seconds")
        
        # Display pipeline steps
        print_separator("PIPELINE STEPS")
        for step in result["pipeline_steps"]:
            step_name = step["step"]
            status = step.get("status", "completed")
            print(f"Step: {step_name} - Status: {status}")
            
            # Display step-specific details
            if step_name == "nlp_analysis":
                print(f"  Triggers: {', '.join(step['triggers'])}")
                print(f"  Keywords: {', '.join(step['keywords'])}")
                print(f"  Raw Query: {step['raw_query']}")
            elif step_name == "sql_execution" and status == "success":
                print(f"  SQL: {step.get('sql', 'N/A')}")
                print(f"  Results Count: {step.get('results_count', 0)}")
        
        # Display cleansed data if available
        if result.get("cleansed_data"):
            print_separator("DATA CLEANSING RESULTS")
            
            print("Summary:")
            print(result["cleansed_data"].get("summary", "No summary available"))
            
            print("\nKey Information:")
            key_info = result["cleansed_data"].get("key_info", {})
            if key_info:
                for field, value in zip(key_info.get("fields", []), key_info.get("values", [])):
                    print(f"  - {field}: {value}")
            
            print("\nConclusions:")
            for conclusion in result["cleansed_data"].get("conclusions", ["No conclusions available"]):
                print(f"  - {conclusion}")
        
        # Display visualization information
        if result.get("visualization"):
            print_separator("VISUALIZATION")
            print(f"Chart Type: {result['visualization']['chart_type']}")
            print("Chart data summary:")
            chart_data = result['visualization']['chart_data']
            
            # Display chart data snippet
            if isinstance(chart_data, dict):
                for key, value in chart_data.items():
                    if isinstance(value, list):
                        print(f"  {key}: {value[:3]}... ({len(value)} values)")
                    else:
                        print(f"  {key}: {value}")
            
            # Mention HTML availability
            html_embed_size = len(result['visualization']['html_embed'])
            print(f"\nHTML Embed code available ({html_embed_size} bytes)")
            
        # Display query results sample
        if result.get("final_results"):
            print_separator("QUERY RESULTS SAMPLE")
            
            results = result["final_results"]
            print(f"Total results: {len(results)}")
            
            # Convert to DataFrame for nicer display
            if results:
                df = pd.DataFrame(results[:3])  # Show first 3 rows
                print("\nSample data:")
                print(df.head(3))
                
                if len(results) > 3:
                    print(f"...and {len(results) - 3} more rows")
    else:
        print(f"Pipeline execution failed: {result.get('message', 'Unknown error')}")
    
    print_separator("END OF PIPELINE EXECUTION")

if __name__ == "__main__":
    main() 