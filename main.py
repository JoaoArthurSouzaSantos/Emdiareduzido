from fastapi import FastAPI
from Paciente.routers import router as paciente_router
from Pessoa.routers import router as pessoa_router
from Funcionario.routers import router as funcionario_router
from Consulta.routers import router as consulta_router
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# Incluir as rotas relacionadas ao usuário
app.include_router(funcionario_router, prefix="/funcionario", tags=["funcionarios"])
app.include_router(paciente_router, prefix="/paciente", tags=["pacientes"])
app.include_router(pessoa_router, prefix="/pessoa_router", tags=["pessoa_router"])
app.include_router(consulta_router, prefix="/consulta_router", tags=["consulta_router"])




@app.get("/openapi.json")
async def get_open_api_endpoint():
    return JSONResponse(get_openapi(title="Your Project Name", version="1.0", routes=app.routes))


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir solicitações de todas as origens
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos os métodos HTTP
    allow_headers=["*"],  # Permitir todos os cabeçalhos
)