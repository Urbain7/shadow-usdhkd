import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Charge les variables du fichier .env
load_dotenv()

# Lit l'adresse de la base de données depuis le fichier .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Crée le "moteur" de connexion SQLAlchemy
engine = create_engine(DATABASE_URL)

# Crée une "usine à sessions" pour communiquer avec la base de données
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crée une classe de base pour nos modèles de table
Base = declarative_base()