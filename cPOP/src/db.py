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

class Measure(Base):
    __tablename__ = Columns.MEASURE
    key = Column(String, primary_key=True)
    year = Column(Integer)
    number = Column(Integer)
    fraction = Column(Float)
    year_total = Column(Integer)
    tag_total = Column(Integer)
    
def recreate_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def check_key(df, columns=[Columns.YEAR,Columns.TAG]):
    key_values = df[columns].drop_duplicates()
    if len(key_values) != len(df):
        warnings.warn("Columns are not a unique key.")
    else:
        print(f'Key check ok. Key columns are: {columns}')

def write_db(df, db_path=PATH_TO_DB):
    check_key(df)
    engine = create_engine(db_path)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Inserting data into tags table
    df[Columns.ID] = df[Columns.YEAR].astype(str) + '@@' + df[Columns.TAG]
    # tags_data = tags_data.rename(columns={Columns.TAG: Columns.TAG_GROUP})
    tags_entries = [
        Tag(key=row[Columns.ID], tag_group=row[Columns.TAG_GROUP], tag=row[Columns.TAG])
        for _, row in df.iterrows()
    ]
    session.add_all(tags_entries)

    # Inserting data into measures table
    measures_entries = [
        Measure(key=row[Columns.ID], year=row[Columns.YEAR], number=row[Columns.COUNT], fraction=row[Columns.FRACTION], tag_total=row[Columns.TAG_COUNT], year_total=row[Columns.YEAR_COUNT] )
        for _, row in df.iterrows()
    ]
    session.add_all(measures_entries)

    session.commit()
    session.close()