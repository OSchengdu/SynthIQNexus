from NLP import NLPAgent
from choose_data import SourceRouter
from sql_query import SQLExecutor
from cleansing_db import DataCleanser
from diagram import DiagramGenerator
import json
from typing import Dict, List, Any, Optional

class DataPipeline:
    """
    A unified data pipeline that connects NLP processing, data source selection,
    SQL query execution, and data cleansing into a continuous workflow.
    """
    
    def __init__(self, db_schemas: List[str], csv_path: str = "Air_Quality.csv"):
        """
        Initialize the data pipeline with required components.
        
        :param db_schemas: Database schema information for NLP module
        :param csv_path: Path to the CSV file for SQL queries
        """
        # Initialize components
        self.nlp_agent = NLPAgent(db_schemas)
        self.source_router = SourceRouter()
        self.sql_executor = SQLExecutor(csv_path)
        
    def process_query(self, user_query: str) -> Dict[str, Any]:
        """
        Process a user query through the entire pipeline.
        
        :param user_query: The natural language query from the user
        :return: Results from the entire pipeline process
        """
        results = {
            "status": "success",
            "pipeline_steps": [],
            "final_results": None,
            "visualization": None,
            "cleansed_data": None
        }
        
        try:
            # Step 1: NLP Analysis
            nlp_result = self.nlp_agent.analyze(user_query)
            if not nlp_result:
                return {"status": "error", "message": "NLP analysis failed"}
            
            triggers, keywords, raw_query = nlp_result
            results["pipeline_steps"].append({
                "step": "nlp_analysis",
                "triggers": triggers,
                "keywords": keywords,
                "raw_query": raw_query
            })
            
            # Step 2: Source Routing (choose_data)
            if not triggers:
                return {"status": "error", "message": "No data sources identified"}
            
            routing_result = self.source_router.route(triggers, keywords, raw_query)
            results["pipeline_steps"].append({
                "step": "source_routing",
                "routing_result": routing_result
            })
            
            # Step 3: SQL Query Generation and Execution
            if "db" in triggers:
                sql_result = self.sql_executor.generate_and_execute(keywords, raw_query)
                
                if not sql_result:
                    # Fallback to traditional SQL generation
                    fallback_results = self.sql_executor.fallback_execute(keywords)
                    results["pipeline_steps"].append({
                        "step": "sql_execution",
                        "status": "fallback",
                        "results_count": len(fallback_results)
                    })
                    query_results = fallback_results
                else:
                    results["pipeline_steps"].append({
                        "step": "sql_execution",
                        "status": "success",
                        "sql": sql_result.get("sql", ""),
                        "tables": sql_result.get("tables", []),
                        "fields": sql_result.get("fields", []),
                        "results_count": len(sql_result.get("results", []))
                    })
                    query_results = sql_result.get("results", [])
                
                # Step 4: Data Cleansing
                if query_results:
                    # Initialize data cleanser with query results
                    data_cleanser = DataCleanser(query_results)
                    cleansed_data = data_cleanser.cleanse()
                    
                    results["pipeline_steps"].append({
                        "step": "data_cleansing",
                        "status": "success"
                    })
                    
                    results["cleansed_data"] = cleansed_data
                    results["final_results"] = query_results
                    
                    # Step 5: Generate visualization if we have results
                    diagram_generator = DiagramGenerator(query_results)
                    chart_data = diagram_generator.generate_chart_data()
                    html_embed = diagram_generator.generate_html_embed()
                    
                    results["visualization"] = {
                        "chart_type": chart_data.get("type", ""),
                        "chart_data": chart_data.get("data", {}),
                        "html_embed": html_embed
                    }
                else:
                    results["pipeline_steps"].append({
                        "step": "data_cleansing",
                        "status": "skipped",
                        "reason": "No query results available"
                    })
            else:
                results["pipeline_steps"].append({
                    "step": "sql_execution",
                    "status": "skipped",
                    "reason": "No database trigger found"
                })
            
            return results
        
        except Exception as e:
            return {
                "status": "error",
                "message": f"Pipeline error: {str(e)}"
            }


# Example usage
if __name__ == "__main__":
    # Initialize the pipeline with database schemas
    db_schemas = [
        "空气质量表：城市(city), PM2.5值(pm25), 监测日期(date), 指标ID(indicator), 地点名称(place_name)",
        "电车数据表：地区(region), 车辆数(count), 充电桩(chargers)"
    ]
    
    # Create the pipeline
    pipeline = DataPipeline(db_schemas)
    
    # Example queries to demonstrate the pipeline
    test_queries = [
        "查询Upper East Side-Gramercy的臭氧水平",
        "纽约市空气质量数据分析",
        "比较Fordham和Upper East Side的空气质量",
        "2014年夏季的空气质量数据"
    ]
    
    # Process each query
    for idx, query in enumerate(test_queries, 1):
        print(f"\n{'='*50}")
        print(f"Query #{idx}: {query}")
        print(f"{'='*50}")
        
        # Execute the full pipeline
        result = pipeline.process_query(query)
        
        # Print summary results
        if result["status"] == "success":
            print("\nPipeline completed successfully!")
            
            # Print steps completion
            print("\nPipeline Steps:")
            for step in result["pipeline_steps"]:
                print(f"- {step['step']}: {step['status'] if 'status' in step else 'completed'}")
            
            # Print cleansed data if available
            if result.get("cleansed_data"):
                print("\nData Summary:")
                print(result["cleansed_data"].get("summary", "No summary available"))
                
                print("\nKey Information:")
                key_info = result["cleansed_data"].get("key_info", {})
                if key_info:
                    for field, value in zip(key_info.get("fields", []), key_info.get("values", [])):
                        print(f"- {field}: {value}")
                
                print("\nConclusions:")
                for conclusion in result["cleansed_data"].get("conclusions", ["No conclusions available"]):
                    print(f"- {conclusion}")
                
                # Print visualization type
                if result.get("visualization"):
                    print(f"\nVisualization: {result['visualization']['chart_type']} chart generated")
            
            # Print result count if available
            if result.get("final_results"):
                print(f"\nFound {len(result['final_results'])} results")
        else:
            print(f"\nError: {result['message']}") 