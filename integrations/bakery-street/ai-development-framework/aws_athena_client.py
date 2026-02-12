import os
#!/usr/bin/env python3
"""
AWS Athena Client
Simple client for running queries on AWS Athena
"""

import boto3
import time

class AthenaClient:
    def __init__(self, region='us-east-1'):
        self.client = boto3.client('athena', region_name=region)
        self.s3_output = os.getenv('AWS_S3_OUTPUT_BUCKET', 's3://your-athena-results-bucket/')
        
    def execute_query(self, query, database='default'):
        """Execute a query on Athena"""
        response = self.client.start_query_execution(
            QueryString=query,
            QueryExecutionContext={'Database': database},
            ResultConfiguration={'OutputLocation': self.s3_output}
        )
        
        query_id = response['QueryExecutionId']
        return self.wait_for_query(query_id)
    
    def wait_for_query(self, query_id):
        """Wait for query completion and return results"""
        while True:
            response = self.client.get_query_execution(QueryExecutionId=query_id)
            status = response['QueryExecution']['Status']['State']
            
            if status in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
                break
            time.sleep(1)
        
        if status == 'SUCCEEDED':
            return self.get_query_results(query_id)
        else:
            raise Exception(f"Query failed with status: {status}")
    
    def get_query_results(self, query_id):
        """Get query results"""
        response = self.client.get_query_results(QueryExecutionId=query_id)
        return response['ResultSet']['Rows']

# Example usage
if __name__ == "__main__":
    # Configure AWS credentials first: aws configure
    athena = AthenaClient()
    
    # Example query
    query = "SELECT * FROM your_table LIMIT 10"
    try:
        results = athena.execute_query(query)
        print(f"Query results: {results}")
    except Exception as e:
        print(f"Error: {e}")