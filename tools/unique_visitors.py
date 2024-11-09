from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
from typing import Dict, List
from datetime import datetime
import time
from models.analytics_models import TestPcsEvent
import os

'''
Sample questions:
1. How many people visited the website?
2. How many people visited customer_4's website in 2023?
3. How many people visited customer_3's website in 2024 in Engineering org? 
4. How many people visited customer_2's website in 2024 in Sales org? Give me a breakdown by country.
5. How many people visited Engineering org? Give me a breakdown by namespace.
'''

def get_unique_visitors(request_body: Dict) -> List[Dict]:
    """
    Returns the number of unique visitors given some filters and dimensions.
    This function constructs and executes a query to fetch customer-agnostic statistics.

    Parameters:
    (Dict): A dictionary with the following keys:
        - "from_ts" (str): Lower bound timestamp in ISO format of the date range without trailing Z. Default to 2024 Jan 1st.
        - "to_ts" (str): Upper bound timestamp in ISO format of the date range without trailing Z. Default to 2024 Dec 31st.
        - "group_ids" (List[str], optional): Customer names.
        - "business_units" (List[str], optional): Business unit names. These are essentially the organizations or departments within the company.
        - "location_countries" (List[str], optional): Country names.
        - "grouped_columns" (List[str], optional): List of column names to group by 
              when fetching breakdown data. If not provided, no grouping is applied.
              Possible values include:
                - "position_business_unit"
                - "position_location_country"
                - "group_id"
                - "namespace"
                - "event"

    Returns:
    List[Dict]: List of result dictionaries containing the groupings and unique visitor counts.

    Raises:
    Exception: If an error occurs during processing.
    """
    print(f"Actual request body is {request_body}")

    # Extract filter values from request body
    from_ts = request_body.get("from_ts")
    to_ts = request_body.get("to_ts")
    group_ids = request_body.get("group_ids") or []
    business_units = request_body.get("business_units") or []
    location_countries = request_body.get("location_countries") or []
    job_functions = request_body.get("job_functions") or []
    grouped_columns = request_body.get("grouped_columns") or []

    # Convert timestamps from ISO format if provided
    from_ts = datetime.fromisoformat(from_ts) if from_ts else None
    to_ts = datetime.fromisoformat(to_ts) if to_ts else None

    if not all([from_ts, to_ts]):
        raise Exception("Date range parameters are mandatory")

    # Build the Databricks connection URL
    url = URL.create(
        "databricks",
        host=os.getenv("DATABRICKS_SERVER_HOSTNAME"),
        port=443,
        username="njupudi@eightfold.ai",  # Replace with your actual username
        password=os.getenv("ACCESS_TOKEN"),
        database="analytics_infra_test",
        query={"http_path": os.getenv("HTTP_PATH")},
    )

    # Create SQLAlchemy engine and session
    engine = create_engine(url)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Start building the query for filtering based on request body
        query = session.query(TestPcsEvent)

        if from_ts:
            query = query.filter(TestPcsEvent.event_date >= from_ts)
        if to_ts:
            query = query.filter(TestPcsEvent.event_date <= to_ts)
        if group_ids:
            query = query.filter(TestPcsEvent.group_id.in_(group_ids))
        if business_units:
            query = query.filter(TestPcsEvent.position_business_unit.in_(business_units))
        if location_countries:
            query = query.filter(TestPcsEvent.position_location_country.in_(location_countries))
        if job_functions:
            query = query.filter(TestPcsEvent.position_job_function.in_(job_functions))

        # Dynamically build the GROUP BY clause based on grouped_columns
        if grouped_columns:
            group_by_columns = [getattr(TestPcsEvent, col) for col in grouped_columns]
            query = query.group_by(*group_by_columns)
            # Apply the aggregation: count distinct vs_cookie
            query = query.with_entities(*group_by_columns, func.count(TestPcsEvent.vs_cookie.distinct()).label('num_unique_visitors'))
        else:
             query = query.with_entities(func.count(TestPcsEvent.vs_cookie.distinct()).label('num_unique_visitors'))

        # Execute the query and fetch the results
        start_time = time.time()
        result = query.all()
        print(f"Time taken in seconds: {time.time() - start_time}")

        # Convert result into a list of dictionaries (optional)
        result_dict = [{col: getattr(row, col) for col in grouped_columns} | {'num_unique_visitors': row.num_unique_visitors} for row in result]
        return result_dict

    except Exception as e:
        raise Exception(f"Error occurred while fetching stats: {str(e)}")

    finally:
        # Close the session to release the connection
        session.close()
