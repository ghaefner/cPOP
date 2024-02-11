from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
import warnings
from cPOP.constants import Columns, PATH_TO_DB

Base = declarative_base()

class Tag(Base):
    __tablename__ = Columns.TAG
    key = Column(String, primary_key=True)
    tag = Column(String)
    tag_group = Column(String)
    tag_total = Column(Integer)
    year_total = Column(Integer)

class Measure(Base):
    __tablename__ = Columns.MEASURE
    key = Column(String, primary_key=True)
    year = Column(Integer)
    number = Column(Integer)
    fraction = Column(Float)

def check_key(df, columns=[Columns.YEAR,Columns.TAG]):
    key_values = df[columns].drop_duplicates()
    if len(key_values) != len(df):
        warnings.warn("Columns are not a unique key.")
    else:
        print("Key check ok.")

def write_db(df, db_path=PATH_TO_DB):

    check_key(df)

    engine = create_engine(db_path)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    print(f"Writing table: {Columns.TAG} to {PATH_TO_DB}")

    # Inserting data into tags table
    columns_for_tags_table = [Columns.ID, Columns.TAG, Columns.TAG_GROUP]
    df[Columns.ID] = df[Columns.YEAR].astype(str) + '@@' + df[Columns.TAG]
    df[[columns_for_tags_table]].to_sql(Columns.TAG, con=engine, if_exists='replace', index=False)

    print(f"Writing table: {Columns.MEASURE} to {PATH_TO_DB}")

    # Inserting data into measures table
    columns_for_measure_table = [Columns.ID, Column.YEAR, Columns.COUNT, Columns.FRACTION, Columns.YEAR_COUNT, Columns.TAG_COUNT]
    df[columns_for_measure_table].to_sql(Columns.MEASURE, con=engine, if_exists='replace', index=False)


    session.commit()
    session.close()
