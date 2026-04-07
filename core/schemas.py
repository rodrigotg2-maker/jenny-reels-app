from pydantic import BaseModel, Field
from typing import List


class Diagnostico(BaseModel):
    funciona: List[str] = Field(default_factory=list)
    frena: List[str] = Field(default_factory=list)


class ReelOutput(BaseModel):
    diagnostico: Diagnostico
    guion_final_optimizado: str = ""
    titulos_sugeridos: List[str] = Field(default_factory=list)
    hooks_mejorados: List[str] = Field(default_factory=list)
    hashtags: List[str] = Field(default_factory=list)
    frases_cierre: List[str] = Field(default_factory=list)