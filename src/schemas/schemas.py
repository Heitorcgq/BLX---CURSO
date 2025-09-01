from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class ProdutoSimples(BaseModel):
    id: Optional[int] = None
    nome: str
    preco: float

    class Config:
        orm_mode = True


class Usuario(BaseModel):
    id: Optional[str] = None
    nome: str
    senha: str
    telefone: int
    produtos: List[ProdutoSimples] = []

    class Config:
        orm_mode = True


class UsuarioSimples(BaseModel):
    id: Optional[str] = None
    nome: str
    telefone: int

    model_config = ConfigDict(from_attributes=True)

class LoginData(BaseModel):
    senha: str
    telefone: int

class LoginSucesso(BaseModel):
    usuario: UsuarioSimples
    acess_token: str

class Produto(BaseModel):
    id: Optional[int] = None
    nome: str
    detalhes: str
    preco: float
    disponivel: bool = False
    usuario_id: Optional[str] = None

    class Config:
        orm_mode = True



class Pedido(BaseModel):
    id: Optional[int] = None
    quantidade: int
    local_entrega: Optional[str]
    tipo_entrega: str
    observacao: Optional[str] = 'Sem observações'

    usuario_id: Optional[str] = None
    produto_id: Optional[int] = None

    usuario: Optional[UsuarioSimples] = None
    produto: Optional[Produto] = None

    class Config:
        orm_mode = True


Usuario.model_rebuild()
Pedido.model_rebuild()
