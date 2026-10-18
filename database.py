from sqlmodel import Session, create_engine, SQLModel


DATEBASE_URL = "sqlite:///dabbawala.db"

engine = create_engine(DATEBASE_URL, echo=True)

def create_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    """
    Provides a database session

    """
    with Session(engine) as session:
        yield session