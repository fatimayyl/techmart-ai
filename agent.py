"""
YZTA 5.0 Hackathon - AI Agent
Google GenAI SDK ile Tool-Calling Agent
"""

import os
import json
import uuid
from typing import Optional

from google import genai
from google.genai import types

from prompts import SYSTEM_PROMPT, FALLBACK_RESPONSE
from tools import TOOL_FUNCTIONS
from models import ToolAction


# ============================================================
# OTURUM YÖNETİMİ (In-memory)
# ============================================================
_sessions: dict = {}


def get_or_create_session(session_id: Optional[str] = None) -> tuple:
    """Oturum geçmişi al veya yeni oturum oluştur."""
    if session_id and session_id in _sessions:
        return session_id, _sessions[session_id]
    new_id = session_id or str(uuid.uuid4())[:8]
    _sessions[new_id] = []
    return new_id, _sessions[new_id]


def save_to_history(session_id: str, role: str, content: str):
    """Mesajı oturum geçmişine kaydet."""
    if session_id in _sessions:
        _sessions[session_id].append({"role": role, "content": content})
        if len(_sessions[session_id]) > 20:
            _sessions[session_id] = _sessions[session_id][-20:]


# ============================================================
# TOOL TANIMLARI (google-genai formatı)
# ============================================================

def _build_tool_declarations():
    """google-genai SDK için tool tanımlarını oluşturur."""
    check_order = types.FunctionDeclaration(
        name="check_order_status",
        description="Sipariş numarası ile sipariş durumunu, kargo bilgisini ve detaylarını sorgular. Sipariş numarası SP ile başlar (örnek: SP1001).",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "order_id": types.Schema(
                    type=types.Type.STRING,
                    description="Sipariş numarası (ör: SP1001)"
                )
            },
            required=["order_id"]
        )
    )

    search_order = types.FunctionDeclaration(
        name="search_order_by_customer",
        description="Müşteri adı veya telefon numarası ile siparişleri arar.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "customer_name": types.Schema(
                    type=types.Type.STRING,
                    description="Müşteri adı (ör: Ahmet Yılmaz)"
                ),
                "phone": types.Schema(
                    type=types.Type.STRING,
                    description="Telefon numarası (ör: 0532 123 4567)"
                )
            },
            required=[]
        )
    )

    check_stock_decl = types.FunctionDeclaration(
        name="check_stock",
        description="Ürün adına göre stok durumunu ve fiyat bilgisini kontrol eder.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "product_name": types.Schema(
                    type=types.Type.STRING,
                    description="Aranacak ürün adı (ör: iPhone, kulaklık, ayakkabı)"
                )
            },
            required=["product_name"]
        )
    )

    list_prods = types.FunctionDeclaration(
        name="list_products",
        description="Mağazadaki ürünleri kategoriye göre listeler. Mevcut kategoriler: Elektronik, Giyim, Ev Eşyası.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "category": types.Schema(
                    type=types.Type.STRING,
                    description="Ürün kategorisi (Elektronik, Giyim, Ev Eşyası). Boş bırakılırsa tüm ürünler."
                )
            },
            required=[]
        )
    )

    create_return = types.FunctionDeclaration(
        name="create_return_request",
        description="Teslim edilmiş bir sipariş için iade talebi oluşturur.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "order_id": types.Schema(
                    type=types.Type.STRING,
                    description="İade edilecek sipariş numarası (ör: SP1001)"
                ),
                "reason": types.Schema(
                    type=types.Type.STRING,
                    description="İade nedeni"
                )
            },
            required=["order_id", "reason"]
        )
    )

    return types.Tool(function_declarations=[
        check_order, search_order, check_stock_decl, list_prods, create_return
    ])


# ============================================================
# ANA AGENT SINIFI
# ============================================================

class CustomerServiceAgent:
    """TechMart AI Müşteri Temsilcisi Agent."""

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY", "")
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY ortam değişkeni ayarlanmamış. "
                "Lütfen .env dosyasına GEMINI_API_KEY=your_key ekleyin."
            )

        self.client = genai.Client(api_key=api_key)
        self.model_name = "gemini-2.0-flash"
        self.tools = _build_tool_declarations()

    async def process_message(
        self, message: str, session_id: Optional[str] = None
    ) -> dict:
        """Kullanıcı mesajını işler, gerekli tool'ları çağırır ve yanıt döner."""
        sid, history = get_or_create_session(session_id)
        tools_used: list[ToolAction] = []

        try:
            # Konuşma geçmişini SDK formatına çevir
            contents = []
            for msg in history:
                contents.append(
                    types.Content(
                        role=msg["role"],
                        parts=[types.Part.from_text(text=msg["content"])]
                    )
                )

            # Kullanıcı mesajını ekle
            contents.append(
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=message)]
                )
            )

            # Generate config
            config = types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                tools=[self.tools],
                temperature=0.7,
                max_output_tokens=2048,
            )

            # İlk istek
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=contents,
                config=config,
            )

            # Tool çağrılarını iteratif işle
            max_iterations = 5
            iteration = 0

            while iteration < max_iterations:
                iteration += 1

                # function call var mı?
                function_calls = []
                if response.candidates and response.candidates[0].content:
                    for part in response.candidates[0].content.parts:
                        if part.function_call:
                            function_calls.append(part.function_call)

                if not function_calls:
                    break

                # Model yanıtını contents'e ekle
                contents.append(response.candidates[0].content)

                # Her function call'ı çalıştır
                func_response_parts = []
                for fc in function_calls:
                    tool_name = fc.name
                    tool_args = dict(fc.args) if fc.args else {}

                    if tool_name in TOOL_FUNCTIONS:
                        try:
                            result = TOOL_FUNCTIONS[tool_name](**tool_args)
                        except Exception as e:
                            result = json.dumps(
                                {"hata": f"Tool çalıştırılırken hata: {str(e)}"},
                                ensure_ascii=False
                            )
                    else:
                        result = json.dumps(
                            {"hata": f"Bilinmeyen tool: {tool_name}"},
                            ensure_ascii=False
                        )

                    tools_used.append(ToolAction(
                        tool_name=tool_name,
                        parameters=tool_args,
                        result=result
                    ))

                    func_response_parts.append(
                        types.Part.from_function_response(
                            name=tool_name,
                            response={"result": result}
                        )
                    )

                # Tool sonuçlarını contents'e ekle
                contents.append(
                    types.Content(
                        role="user",
                        parts=func_response_parts
                    )
                )

                # Tekrar generate et
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=contents,
                    config=config,
                )

            # Final yanıtı al
            final_text = ""
            if response.candidates and response.candidates[0].content:
                for part in response.candidates[0].content.parts:
                    if part.text:
                        final_text += part.text

            if not final_text:
                final_text = FALLBACK_RESPONSE

            # Geçmişe kaydet
            save_to_history(sid, "user", message)
            save_to_history(sid, "model", final_text)

            return {
                "response": final_text,
                "session_id": sid,
                "tools_used": [t.model_dump() for t in tools_used],
                "intent": self._detect_intent(tools_used)
            }

        except Exception as e:
            error_msg = (
                f"Bir hata oluştu, lütfen tekrar deneyin. "
                f"Sorun devam ederse 0850 123 4567'yi arayabilirsiniz.\n\n"
                f"(Hata detayı: {str(e)})"
            )
            return {
                "response": error_msg,
                "session_id": sid,
                "tools_used": [],
                "intent": "error"
            }

    def _detect_intent(self, tools_used: list[ToolAction]) -> str:
        """Kullanılan tool'lara göre intent belirle."""
        if not tools_used:
            return "genel_sohbet"
        tool_names = [t.tool_name for t in tools_used]
        if "check_order_status" in tool_names:
            return "siparis_sorgulama"
        if "search_order_by_customer" in tool_names:
            return "musteri_siparis_arama"
        if "check_stock" in tool_names:
            return "stok_kontrolu"
        if "list_products" in tool_names:
            return "urun_listeleme"
        if "create_return_request" in tool_names:
            return "iade_talebi"
        return "genel"
