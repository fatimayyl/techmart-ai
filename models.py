"""
YZTA 5.0 Hackathon - Pydantic Modelleri
"""

from pydantic import BaseModel, Field
from typing import Optional, List


class ChatRequest(BaseModel):
    """Kullanıcıdan gelen chat mesajı."""
    message: str = Field(..., description="Kullanıcının mesajı", min_length=1)
    session_id: Optional[str] = Field(None, description="Oturum ID'si (konuşma geçmişi için)")


class ToolAction(BaseModel):
    """Agent'ın çağırdığı tool bilgisi."""
    tool_name: str = Field(..., description="Çağrılan tool adı")
    parameters: dict = Field(default_factory=dict, description="Tool parametreleri")
    result: Optional[str] = Field(None, description="Tool sonucu")


class ChatResponse(BaseModel):
    """Agent'ın yanıtı."""
    response: str = Field(..., description="Agent'ın yanıt mesajı")
    session_id: str = Field(..., description="Oturum ID'si")
    tools_used: List[ToolAction] = Field(default_factory=list, description="Kullanılan tool'lar")
    intent: Optional[str] = Field(None, description="Algılanan kullanıcı niyeti")


class OrderStatusRequest(BaseModel):
    """Sipariş durumu sorgusu."""
    order_id: str = Field(..., description="Sipariş numarası (ör: SP1001)")


class OrderStatusResponse(BaseModel):
    """Sipariş durumu yanıtı."""
    found: bool
    order_id: str
    status: Optional[str] = None
    details: Optional[dict] = None
    message: str
