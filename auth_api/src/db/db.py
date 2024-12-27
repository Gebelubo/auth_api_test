from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect
from ..config import DATABASE_URL
from src.entities.models import Base

class Database:
    def __init__(self):
        self.engine = create_engine(DATABASE_URL, echo=True)  # 'echo=True' para log de SQL
        self.Session = sessionmaker(bind=self.engine)
    
    def get_session(self):
        return self.Session()

    def create_tables(self):
        try:
            with self.engine.begin() as conn:
                print("Criando tabelas...")
                Base.metadata.create_all(bind=conn)
                print("Tabelas criadas com sucesso.")
                conn.commit()  # Commit explícito após a criação
        except Exception as e:
            print(f"Erro ao criar tabelas: {e}")
        self.test_connection()

    def test_connection(self):
        try:
            with self.engine.connect() as conn:
                print(f"Conectado ao banco: {conn.engine.url.database}")
                inspector = inspect(self.engine)
                print(f"Tabelas existentes: {inspector.get_table_names()}")
                schemas = inspector.get_schema_names()
                print(f"Schemas disponíveis: {schemas}")
                tabelas = inspector.get_table_names(schema="public")
                print(f"Tabelas no schema 'public': {tabelas}")
        except Exception as e:
            print(f"Erro ao conectar no banco: {e}")
