import csv
import pprint
import sys

from sqlalchemy import (
    Column,
    Integer,
    MetaData,
    String,
    Table,
    UniqueConstraint,
    create_engine,
    insert,
)

# Read the CSV file qdb.csv into a list of dicts
with open("qdb.csv", mode="r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    data_list = [dict(row) for row in reader]

pprint.pprint(data_list)


# Create a SQLite database engine
engine = create_engine("sqlite:///q.db", echo=True)
metadata = MetaData()

# Define the schema
known_queries_table = Table(
    "known_queries",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("Active", Integer),
    Column("Provider", String),
    Column("Source", String),
    Column("Instrument", String),
    Column("Date_End", String),
    Column("Date_Start", String),
    UniqueConstraint(
        "Provider", "Source", "Instrument", name="uq_provider_source_instrument"
    ),
)

# Create the table in the database
metadata.create_all(engine)

# Perform the bulk insert inside a transaction block
with engine.begin() as connection:
    # Passing the list of dicts directly to values() executes a bulk insert
    connection.execute(insert(known_queries_table), data_list)

sys.exit(0)
