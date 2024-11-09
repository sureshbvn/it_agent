from sqlalchemy import Column, String, BigInteger, DateTime
from sqlalchemy.orm import declarative_base

# Define the SQLAlchemy Base class and the model
Base = declarative_base()

class TestPcsEvent(Base):
    __tablename__ = 'test_pcs_events'
    __table_args__ = {'schema': 'analytics_data'}  # Explicitly set schema

    event_date = Column(DateTime)
    group_id = Column(String)
    namespace = Column(String)
    event = Column(String)
    utm_source = Column(String)
    vs_cookie = Column(String)
    position_id = Column(BigInteger)
    vs_cookie_position_id = Column(String)
    position_location_country = Column(String)
    position_business_unit = Column(String)
    position_job_function = Column(String)

    # This tells SQLAlchemy to skip primary key requirement for SELECT queries
    __mapper_args__ = {
        'primary_key': [group_id, event_date, namespace, event]  # Use any unique column here
    }