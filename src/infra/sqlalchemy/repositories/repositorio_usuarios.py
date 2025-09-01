from sqlalchemy.orm import Session
from sqlalchemy import select
from src.schemas import schemas
from src.infra.sqlalchemy.models import models

class RepositorioUsuario():
    def __init__(self, session: Session):
        self.db = session

    def criar(self, usuario: schemas.Usuario): 
        db_usuario = models.Usuario(nome=usuario.nome,
                                    senha=usuario.senha,
                                    telefone=usuario.telefone)
        self.db.add(db_usuario)
        self.db.commit()
        self.db.refresh(db_usuario)
        return db_usuario
    
    def listar(self):
        usuarios = self.db.query(models.Usuario).all()
        return usuarios
    
    def obter_por_telefone(self, telefone) -> models.Usuario:
        query = select(models.Usuario).where(models.Usuario.telefone == telefone)
        return self.db.execute(query).scalars().first()
    
    def remover(self):
        pass