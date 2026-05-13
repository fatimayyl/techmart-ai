"""
YZTA 5.0 Hackathon - FastAPI Ana Uygulama
TechMart AI Müşteri İletişim Otomasyonu
"""

import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from models import ChatRequest, ChatResponse, OrderStatusRequest, OrderStatusResponse
from agent import CustomerServiceAgent
from tools import check_order_status, list_products, check_stock
from mock_db import PRODUCTS

import json

# ============================================================
# UYGULAMA BAŞLATMA
# ============================================================

agent: CustomerServiceAgent = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global agent
    try:
        agent = CustomerServiceAgent()
        print("TechMart AI Agent basariyla baslatildi!")
    except ValueError as e:
        print(f"UYARI: {e}")
        print("Agent olmadan devam ediliyor. Chat ozelligi calismayacak.")
        agent = None
    yield

app = FastAPI(
    title="TechMart AI - Musteri Iletisim Otomasyonu",
    description="YZTA 5.0 Hackathon - AI Destekli KOBİ Müşteri Hizmetleri",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static dosyalar
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


# ============================================================
# ENDPOINT'LER
# ============================================================

@app.get("/", tags=["UI"])
async def serve_frontend():
    """Chat arayüzünü serve eder."""
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "TechMart AI API aktif. /docs adresinden API dokumanina ulasabilirsiniz."}


@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat_endpoint(request: ChatRequest):
    """
    Ana chat endpoint'i.
    Kullanıcı mesajını AI Agent'a iletir ve yanıt döner.
    """
    if agent is None:
        raise HTTPException(
            status_code=503,
            detail="AI Agent hazir degil. Lutfen GEMINI_API_KEY ayarlayin."
        )

    result = await agent.process_message(
        message=request.message,
        session_id=request.session_id
    )

    return ChatResponse(
        response=result["response"],
        session_id=result["session_id"],
        tools_used=result.get("tools_used", []),
        intent=result.get("intent")
    )


@app.get("/order-status/{order_id}", response_model=OrderStatusResponse, tags=["Siparis"])
async def get_order_status(order_id: str):
    """
    Direkt sipariş durumu sorgulama endpoint'i.
    Sipariş numarası ile sipariş bilgilerini döner.
    """
    result_str = check_order_status(order_id)
    result = json.loads(result_str)

    if "hata" in result:
        return OrderStatusResponse(
            found=False,
            order_id=order_id,
            message=result["hata"]
        )

    return OrderStatusResponse(
        found=True,
        order_id=order_id,
        status=result.get("durum"),
        details=result,
        message=f"Siparis {order_id} bulundu. Durum: {result.get('durum')}"
    )


@app.get("/products", tags=["Urunler"])
async def get_products(category: str = ""):
    """Ürün listesi endpoint'i. Opsiyonel kategori filtresi."""
    result_str = list_products(category)
    return json.loads(result_str)


@app.get("/stock/{product_name}", tags=["Stok"])
async def get_stock(product_name: str):
    """Stok durumu sorgulama endpoint'i."""
    result_str = check_stock(product_name)
    return json.loads(result_str)


@app.get("/health", tags=["System"])
async def health_check():
    """Sistem sağlık kontrolü."""
    return {
        "status": "healthy",
        "agent_ready": agent is not None,
        "product_count": len(PRODUCTS)
    }


# ============================================================
# ÇALIŞTIRMA
# ============================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
