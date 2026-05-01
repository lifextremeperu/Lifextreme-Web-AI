from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class Cotizacion(BaseModel):
    items: List[str] = Field(description="Lista de productos o tours seleccionados")
    precio_total: float = Field(description="Precio total de la experiencia")
    descuento_aplicado: float = Field(default=0.0, description="Monto ahorrado por membresía o comunidad")
    monto_reserva_hoy: float = Field(description="El 30% inicial para asegurar el cupo")
    monto_segundo_pago: float = Field(description="El 30% a pagar antes del tour")
    monto_pago_final: float = Field(description="El 40% a pagar el día del tour")
    link_pago_niubiz: Optional[str] = Field(None, description="URL dinámica para el pago de la reserva vía Niubiz/Yape")

class PerfilUsuario(BaseModel):
    nivel_experiencia: Literal['Principiante', 'Intermedio', 'Avanzado', 'Experto'] = Field(..., description="Nivel físico del aventurero")
    interes_principal: Literal['Expedición', 'Equipamiento', 'Membresía'] = Field(..., description="Qué es lo que más le motiva")
    es_socio_elite: bool = Field(default=False, description="Si ya tiene el pase Exclusive")
    dias_aclimatacion: int = Field(default=0, description="Días de estancia previa en altura")

class MAXResponse(BaseModel):
    mensaje: str = Field(description="Respuesta persuasiva y técnica del asistente")
    datos_cotizacion: Optional[Cotizacion] = Field(None, description="Objeto de cotización si el usuario mostró intención de compra")
    action_required: Optional[Literal['SHOW_PAYMENT', 'ASK_EXPERIENCE', 'SHOW_CATALOG']] = Field(None, description="Acción sugerida para el Frontend")
