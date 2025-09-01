from fastapi import APIRouter, Depends, status, HTTPException
from src.schemas.schemas import Usuario, LoginData, UsuarioSimples, LoginSucesso
from src.infra.sqlalchemy.repositories.repositorio_usuarios import RepositorioUsuario
from sqlalchemy.orm import Session
from src.infra.sqlalchemy.config.database import get_db
from src.infra.providers import hash_provider, token_provider
from src.routers.auth_utils import obter_usuario_logado

router = APIRouter()
#|
#|
#v
@router.post('/usuarios', status_code=status.HTTP_201_CREATED, response_model=Usuario)
def signup(usuario: Usuario, session: Session = Depends(get_db)):
    usuario_localizado = RepositorioUsuario(session) .obter_por_telefone(usuario.telefone)
    if usuario_localizado:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Já existe um usuario com esse telefone')

    usuario.senha = hash_provider.gerar_hash(usuario.senha)
    usuario_criado = RepositorioUsuario(session).criar(usuario)
    return usuario_criado

@router.post('/token', response_model=LoginSucesso)
def login(login_data: LoginData, session: Session = Depends(get_db)):
    senha = login_data.senha
    telefone = login_data.telefone

    usuario = RepositorioUsuario(session).obter_por_telefone(telefone)

    if not usuario:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Telefone ou senha incorretos')
    
    senha_valida = hash_provider.verificar_hash(senha, usuario.senha)

    if not senha_valida:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Telefone ou senha incorretos')
    # Gerar Token JWT
    token = token_provider.criar_acess_token({'sub': str(usuario.telefone)})

    return LoginSucesso(usuario=usuario, acess_token=token)

@router.get('/me', response_model=UsuarioSimples)
def me(usuario: Usuario = Depends(obter_usuario_logado)):
    return usuario