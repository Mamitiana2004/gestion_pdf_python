from sqlalchemy import (
    Column, Integer, String, Text, Date, ForeignKey, Numeric, Table
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Modèle pour la table `utilisateur`
class Utilisateur(Base):
    __tablename__ = 'utilisateur'
    id = Column(Integer, primary_key=True, autoincrement=True)
    identifiant = Column(String(255), nullable=False, unique=True)
    password = Column(Text, nullable=False)
    date_creation = Column(Date,nullable=False)
    date_login = Column(Date,nullable = False)

# Modèle pour la table `manifest`
class Manifest(Base):
    __tablename__ = 'manifest'
    id = Column(Integer, primary_key=True, autoincrement=True)
    vessel = Column(String(50), nullable=False)
    flag = Column(String(50), nullable=False)
    voyage = Column(String(50), nullable=False)
    date_arrive = Column(Date, nullable=False)
    cargos = relationship("Cargo", back_populates="manifest")

# Modèle pour la table `shipper`
class Shipper(Base):
    __tablename__ = 'shipper'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    adresse = Column(String(255), nullable=False)
    cargos = relationship("Cargo", back_populates="shipper")

# Modèle pour la table `consigne`
class Consigne(Base):
    __tablename__ = 'consigne'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    adresse = Column(String(2550), nullable=False)
    cargos = relationship("Cargo", back_populates="consigne")

# Modèle pour la table `port`
class Port(Base):
    __tablename__ = 'port'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)

# Modèle pour la table `cargo`
class Cargo(Base):
    __tablename__ = 'cargo'
    id = Column(Integer, primary_key=True, autoincrement=True)
    bl_no = Column(String(50), nullable=False)
    manifest_id = Column(Integer, ForeignKey('manifest.id', ondelete='CASCADE'))
    shipper_id = Column(Integer, ForeignKey('shipper.id', ondelete='SET NULL'))
    consigne_id = Column(Integer, ForeignKey('consigne.id', ondelete='SET NULL'))
    description_good = Column(Text)
    weight = Column(Numeric(10, 2))
    measurement = Column(Numeric(10, 2))
    
    manifest = relationship("Manifest", back_populates="cargos")
    shipper = relationship("Shipper", back_populates="cargos")
    consigne = relationship("Consigne", back_populates="cargos")

# Modèle pour la table `file_pdf`
class FilePDF(Base):
    __tablename__ = 'file_pdf'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(255), nullable=False)
    nom_serveur = Column(String(255),nullable=False)
    manifests = relationship("Manifest", secondary="pdf_manifest", back_populates="pdfs")
    contenus = relationship("Contenu", back_populates="pdf")

# Table d'association pour `pdf_manifest`
pdf_manifest = Table(
    'pdf_manifest', Base.metadata,
    Column('pdf_id', Integer, ForeignKey('file_pdf.id')),
    Column('manifest_id', Integer, ForeignKey('manifest.id'))
)

# Modèle pour la table `contenu`
class Contenu(Base):
    __tablename__ = 'contenu'
    pdf_id = Column(Integer, ForeignKey('file_pdf.id', ondelete='CASCADE'), primary_key=True)
    page = Column(Integer, primary_key=True)
    contenu = Column(Text, nullable=False)
    
    pdf = relationship("FilePDF", back_populates="contenus")

# Relations supplémentaires
Manifest.pdfs = relationship("FilePDF", secondary="pdf_manifest", back_populates="manifests")