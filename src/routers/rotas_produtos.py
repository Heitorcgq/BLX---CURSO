from fastapi import APIRouter, status, Depends, HTTPException
from src.schemas.schemas import Produto, ProdutoSimples
from src.infra.sqlalchemy.repositories.repositorio_produtos import RepositorioProduto
from sqlalchemy.orm import Session
from src.infra.sqlalchemy.config.database import get_db



router = APIRouter()
#|
#|
#v
@router.post('/produtos', status_code=status.HTTP_201_CREATED, response_model=Produto)
def criar_produto(produto: Produto, session: Session = Depends(get_db)):
    produto_criado = RepositorioProduto(session).criar(produto)
    return produto_criado


@router.get('/produtos')
def listar_produtos(session: Session = Depends(get_db)):
    produtos = RepositorioProduto(session).listar()
    return produtos


@router.get('/produtos/{id}')
def exibir_produto(id: int, session: Session = Depends(get_db)):
    produto_localizado = RepositorioProduto(session).buscarPorId(id)
    if not produto_localizado:
        raise HTTPException(status_code=404, detail=f"item not found id={id}")
    return produto_localizado


@router.get('/produtos/{id}')
def obter_produto(id: int, session: Session = Depends(get_db)):
    produto = RepositorioProduto(session).obter(id)
    return produto


@router.delete('/produtos/{id}')
def remover_produto(id: int, session: Session = Depends(get_db)):
    RepositorioProduto(session).remover(id)
    return {"msg": "Removido com Sucesso!"}
    

@router.put('/produtos/{id}', response_model=Produto)
def editar_produto(id: int, produto: Produto, session: Session = Depends(get_db)):
    RepositorioProduto(session).editar(id, produto)
    return produto