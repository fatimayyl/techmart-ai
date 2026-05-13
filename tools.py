"""
YZTA 5.0 Hackathon - Agent Tool Fonksiyonları
Mock veritabanı ile etkileşime giren tool'lar
"""

import json
from mock_db import ORDERS, PRODUCTS, CUSTOMERS, RETURN_REQUESTS, get_next_return_id


# ============================================================
# TOOL FONKSİYONLARI
# ============================================================

def check_order_status(order_id: str) -> str:
    """Sipariş numarası ile sipariş durumunu sorgular."""
    order_id = order_id.strip().upper()
    if order_id in ORDERS:
        order = ORDERS[order_id]
        result = {
            "siparis_no": order["id"],
            "musteri": order["customer_name"],
            "durum": order["status"],
            "siparis_tarihi": order["order_date"],
            "urunler": [
                {"ad": p["name"], "adet": p["quantity"], "fiyat": f"{p['price']:.2f} TL"}
                for p in order["products"]
            ],
            "toplam_tutar": f"{order['total']:.2f} TL",
            "teslimat_adresi": order["address"]
        }
        if order.get("cargo_company"):
            result["kargo_firmasi"] = order["cargo_company"]
            result["takip_no"] = order["tracking_number"]
        if order.get("estimated_delivery"):
            result["tahmini_teslimat"] = order["estimated_delivery"]
        if order.get("delivery_date"):
            result["teslim_tarihi"] = order["delivery_date"]
        if order.get("cancel_reason"):
            result["iptal_nedeni"] = order["cancel_reason"]
        if order.get("return_reason"):
            result["iade_nedeni"] = order["return_reason"]
            result["iade_durumu"] = order.get("return_status", "")
        if order.get("notes"):
            result["notlar"] = order["notes"]
        return json.dumps(result, ensure_ascii=False, indent=2)
    else:
        return json.dumps({
            "hata": f"'{order_id}' numaralı sipariş bulunamadı.",
            "bilgi": "Lütfen sipariş numaranızı kontrol ediniz. Sipariş numaraları 'SP' ile başlar (ör: SP1001)."
        }, ensure_ascii=False)


def search_order_by_customer(customer_name: str = "", phone: str = "") -> str:
    """Müşteri adı veya telefon numarası ile sipariş arar."""
    customer_name = customer_name.strip().lower()
    phone = phone.strip().replace(" ", "")
    found_orders = []

    for order_id, order in ORDERS.items():
        match = False
        if customer_name and customer_name in order["customer_name"].lower():
            match = True
        if phone:
            cust = CUSTOMERS.get(order["customer_id"], {})
            cust_phone = cust.get("phone", "").replace(" ", "")
            if phone in cust_phone:
                match = True
        if match:
            found_orders.append({
                "siparis_no": order["id"],
                "durum": order["status"],
                "toplam": f"{order['total']:.2f} TL",
                "tarih": order["order_date"],
                "urun_sayisi": sum(p["quantity"] for p in order["products"])
            })

    if found_orders:
        return json.dumps({
            "bulunan_siparis_sayisi": len(found_orders),
            "siparisler": found_orders
        }, ensure_ascii=False, indent=2)
    else:
        return json.dumps({
            "hata": "Bu bilgilerle eşleşen sipariş bulunamadı.",
            "bilgi": "Lütfen ad veya telefon numaranızı kontrol ediniz."
        }, ensure_ascii=False)


def check_stock(product_name: str) -> str:
    """Ürün adına göre stok durumunu kontrol eder."""
    product_name = product_name.strip().lower()
    found_products = []

    for prod_id, prod in PRODUCTS.items():
        if (product_name in prod["name"].lower() or
            product_name in prod["description"].lower() or
            product_name in prod["category"].lower()):
            stock_status = "Stokta Var" if prod["stock"] > 0 else "Stokta Yok"
            found_products.append({
                "urun_kodu": prod["id"],
                "urun_adi": prod["name"],
                "kategori": prod["category"],
                "fiyat": f"{prod['price']:.2f} TL",
                "stok_durumu": stock_status,
                "stok_adedi": prod["stock"],
                "aciklama": prod["description"]
            })

    if found_products:
        return json.dumps({
            "bulunan_urun_sayisi": len(found_products),
            "urunler": found_products
        }, ensure_ascii=False, indent=2)
    else:
        return json.dumps({
            "hata": f"'{product_name}' ile eşleşen ürün bulunamadı.",
            "bilgi": "Farklı bir arama terimi deneyebilirsiniz."
        }, ensure_ascii=False)


def list_products(category: str = "") -> str:
    """Kategoriye göre ürün listeler. Boş bırakılırsa tüm ürünler listelenir."""
    category = category.strip().lower()
    filtered = []

    for prod_id, prod in PRODUCTS.items():
        if not category or category in prod["category"].lower():
            stock_text = "Stokta Var" if prod["stock"] > 0 else "Stokta Yok"
            filtered.append({
                "urun_kodu": prod["id"],
                "ad": f"{prod['image']} {prod['name']}",
                "kategori": prod["category"],
                "fiyat": f"{prod['price']:.2f} TL",
                "stok": stock_text
            })

    if filtered:
        return json.dumps({
            "toplam_urun": len(filtered),
            "urunler": filtered
        }, ensure_ascii=False, indent=2)
    else:
        avail = list(set(p["category"] for p in PRODUCTS.values()))
        return json.dumps({
            "hata": f"'{category}' kategorisinde ürün bulunamadı.",
            "mevcut_kategoriler": avail
        }, ensure_ascii=False)


def create_return_request(order_id: str, reason: str) -> str:
    """İade talebi oluşturur."""
    order_id = order_id.strip().upper()
    if order_id not in ORDERS:
        return json.dumps({
            "hata": f"'{order_id}' numaralı sipariş bulunamadı.",
            "bilgi": "Lütfen sipariş numaranızı kontrol ediniz."
        }, ensure_ascii=False)

    order = ORDERS[order_id]
    if order["status"] not in ["Teslim Edildi"]:
        return json.dumps({
            "hata": "İade talebi oluşturulamadı.",
            "neden": f"Siparişinizin mevcut durumu: '{order['status']}'. Yalnızca 'Teslim Edildi' durumundaki siparişler iade edilebilir."
        }, ensure_ascii=False)

    return_id = get_next_return_id()
    return_request = {
        "iade_no": return_id,
        "siparis_no": order_id,
        "musteri": order["customer_name"],
        "neden": reason,
        "durum": "İade Talebi Alındı",
        "bilgi": "İade talebiniz başarıyla oluşturuldu. En kısa sürede size kargo bilgileri iletilecektir."
    }
    RETURN_REQUESTS.append(return_request)
    return json.dumps(return_request, ensure_ascii=False, indent=2)


# ============================================================
# GEMINI FUNCTION CALLING İÇİN TOOL TANIMLARI
# ============================================================

TOOL_DEFINITIONS = [
    {
        "name": "check_order_status",
        "description": "Sipariş numarası ile sipariş durumunu, kargo bilgisini ve detaylarını sorgular. Sipariş numarası SP ile başlar (örnek: SP1001).",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "Sipariş numarası (ör: SP1001)"
                }
            },
            "required": ["order_id"]
        }
    },
    {
        "name": "search_order_by_customer",
        "description": "Müşteri adı veya telefon numarası ile siparişleri arar. En az bir parametre verilmelidir.",
        "parameters": {
            "type": "object",
            "properties": {
                "customer_name": {
                    "type": "string",
                    "description": "Müşteri adı (ör: Ahmet Yılmaz)"
                },
                "phone": {
                    "type": "string",
                    "description": "Telefon numarası (ör: 0532 123 4567)"
                }
            },
            "required": []
        }
    },
    {
        "name": "check_stock",
        "description": "Ürün adına göre stok durumunu ve fiyat bilgisini kontrol eder.",
        "parameters": {
            "type": "object",
            "properties": {
                "product_name": {
                    "type": "string",
                    "description": "Aranacak ürün adı (ör: iPhone, kulaklık, ayakkabı)"
                }
            },
            "required": ["product_name"]
        }
    },
    {
        "name": "list_products",
        "description": "Mağazadaki ürünleri kategoriye göre listeler. Mevcut kategoriler: Elektronik, Giyim, Ev Eşyası.",
        "parameters": {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "description": "Ürün kategorisi (Elektronik, Giyim, Ev Eşyası). Boş bırakılırsa tüm ürünler listelenir."
                }
            },
            "required": []
        }
    },
    {
        "name": "create_return_request",
        "description": "Teslim edilmiş bir sipariş için iade talebi oluşturur.",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "İade edilecek sipariş numarası (ör: SP1001)"
                },
                "reason": {
                    "type": "string",
                    "description": "İade nedeni"
                }
            },
            "required": ["order_id", "reason"]
        }
    }
]

# Tool fonksiyonlarını isimle eşleştiren sözlük
TOOL_FUNCTIONS = {
    "check_order_status": check_order_status,
    "search_order_by_customer": search_order_by_customer,
    "check_stock": check_stock,
    "list_products": list_products,
    "create_return_request": create_return_request,
}
