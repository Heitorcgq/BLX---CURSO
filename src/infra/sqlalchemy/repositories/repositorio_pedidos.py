from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import List
from src.schemas import schemas
from src.infra.sqlalchemy.models import models



class RepositorioPedido():

    def __init__(self, session: Session):
        self.db = session

    
    def gravar_pedido(self, pedido: schemas.Pedido):
        
        pedido_db = models.Pedido(
            quantidade=pedido.quantidade,
            local_entrega=pedido.local_entrega,
            tipo_entrega=pedido.tipo_entrega,
            observacao=pedido.observacao,
            usuario_id=pedido.usuario_id,
            produto_id=pedido.produto_id
        )

        self.db.add(pedido_db)
        self.db.commit()
        self.db.refresh(pedido_db)
        return pedido_db


    def buscar_por_id(self, id: int):
        query = select(models.Pedido).where(models.Pedido.id == id)
        pedido = self.db.execute(query).one()
        return pedido[0]


    def listar_meus_pedidos_por_usuario_id(self, usuario_id: str):
        query = select(models.Pedido).where(models.Pedido.usuario_id == usuario_id)
        pedido = self.db.execute(query).all()
        return pedido


    def listar_minhas_vendas_por_usuario_id(self, usuario_id: str):
        query = select(models.Pedido).join_from(models.Pedido, models.Produto).where(models.Produto.usuario_id == usuario_id)
        pedido = self.db.execute(query).scalars().all()
        return pedido