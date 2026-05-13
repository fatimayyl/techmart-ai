"""
YZTA 5.0 Hackathon - Mock Veritabanı
TechMart Online Mağaza için örnek veriler
"""

from datetime import datetime, timedelta
import random

# ============================================================
# ÜRÜN VERİTABANI
# ============================================================
PRODUCTS = {
    "PRD001": {
        "id": "PRD001",
        "name": "iPhone 15 Pro Max",
        "category": "Elektronik",
        "price": 74999.99,
        "stock": 12,
        "description": "Apple iPhone 15 Pro Max 256GB Titanium Mavi",
        "image": "📱"
    },
    "PRD002": {
        "id": "PRD002",
        "name": "Samsung Galaxy S24 Ultra",
        "category": "Elektronik",
        "price": 64999.99,
        "stock": 8,
        "description": "Samsung Galaxy S24 Ultra 512GB Titanium Gri",
        "image": "📱"
    },
    "PRD003": {
        "id": "PRD003",
        "name": "MacBook Air M3",
        "category": "Elektronik",
        "price": 49999.99,
        "stock": 5,
        "description": "Apple MacBook Air M3 15 inç 16GB RAM 512GB SSD",
        "image": "💻"
    },
    "PRD004": {
        "id": "PRD004",
        "name": "Sony WH-1000XM5",
        "category": "Elektronik",
        "price": 12499.99,
        "stock": 20,
        "description": "Sony WH-1000XM5 Kablosuz Gürültü Önleyici Kulaklık",
        "image": "🎧"
    },
    "PRD005": {
        "id": "PRD005",
        "name": "Nike Air Max 270",
        "category": "Giyim",
        "price": 4299.99,
        "stock": 35,
        "description": "Nike Air Max 270 React Erkek Spor Ayakkabı",
        "image": "👟"
    },
    "PRD006": {
        "id": "PRD006",
        "name": "Levi's 501 Original",
        "category": "Giyim",
        "price": 1899.99,
        "stock": 0,
        "description": "Levi's 501 Original Fit Erkek Jean Pantolon",
        "image": "👖"
    },
    "PRD007": {
        "id": "PRD007",
        "name": "Dyson V15 Detect",
        "category": "Ev Eşyası",
        "price": 29999.99,
        "stock": 3,
        "description": "Dyson V15 Detect Absolute Kablosuz Süpürge",
        "image": "🧹"
    },
    "PRD008": {
        "id": "PRD008",
        "name": "Philips Airfryer XXL",
        "category": "Ev Eşyası",
        "price": 8499.99,
        "stock": 15,
        "description": "Philips Airfryer XXL Premium HD9867 Siyah",
        "image": "🍳"
    },
    "PRD009": {
        "id": "PRD009",
        "name": "Apple Watch Series 9",
        "category": "Elektronik",
        "price": 17999.99,
        "stock": 0,
        "description": "Apple Watch Series 9 45mm GPS + Cellular",
        "image": "⌚"
    },
    "PRD010": {
        "id": "PRD010",
        "name": "JBL Charge 5",
        "category": "Elektronik",
        "price": 4999.99,
        "stock": 25,
        "description": "JBL Charge 5 Taşınabilir Bluetooth Hoparlör",
        "image": "🔊"
    },
    "PRD011": {
        "id": "PRD011",
        "name": "Adidas Ultraboost 23",
        "category": "Giyim",
        "price": 5499.99,
        "stock": 18,
        "description": "Adidas Ultraboost Light 23 Koşu Ayakkabısı",
        "image": "👟"
    },
    "PRD012": {
        "id": "PRD012",
        "name": "Arzum Okka Minio",
        "category": "Ev Eşyası",
        "price": 3299.99,
        "stock": 40,
        "description": "Arzum Okka Minio Türk Kahvesi Makinesi",
        "image": "☕"
    },
    "PRD013": {
        "id": "PRD013",
        "name": "iPad Air M2",
        "category": "Elektronik",
        "price": 27999.99,
        "stock": 7,
        "description": "Apple iPad Air M2 11 inç 256GB Wi-Fi",
        "image": "📱"
    },
    "PRD014": {
        "id": "PRD014",
        "name": "The North Face Puffer",
        "category": "Giyim",
        "price": 7999.99,
        "stock": 10,
        "description": "The North Face 1996 Retro Nuptse Şişme Mont",
        "image": "🧥"
    },
    "PRD015": {
        "id": "PRD015",
        "name": "Robot Süpürge Roborock S8",
        "category": "Ev Eşyası",
        "price": 22999.99,
        "stock": 6,
        "description": "Roborock S8 Pro Ultra Robot Süpürge ve Paspas",
        "image": "🤖"
    },
    "PRD016": {
        "id": "PRD016",
        "name": "PS5 DualSense Controller",
        "category": "Elektronik",
        "price": 2499.99,
        "stock": 30,
        "description": "Sony PlayStation 5 DualSense Kablosuz Oyun Kolu",
        "image": "🎮"
    }
}

# ============================================================
# MÜŞTERİ VERİTABANI
# ============================================================
CUSTOMERS = {
    "MUS001": {
        "id": "MUS001",
        "name": "Ahmet Yılmaz",
        "email": "ahmet.yilmaz@email.com",
        "phone": "0532 123 4567",
        "address": "Kadıköy, İstanbul"
    },
    "MUS002": {
        "id": "MUS002",
        "name": "Elif Demir",
        "email": "elif.demir@email.com",
        "phone": "0545 987 6543",
        "address": "Çankaya, Ankara"
    },
    "MUS003": {
        "id": "MUS003",
        "name": "Mehmet Kaya",
        "email": "mehmet.kaya@email.com",
        "phone": "0555 456 7890",
        "address": "Bornova, İzmir"
    },
    "MUS004": {
        "id": "MUS004",
        "name": "Zeynep Arslan",
        "email": "zeynep.arslan@email.com",
        "phone": "0542 321 6548",
        "address": "Nilüfer, Bursa"
    },
    "MUS005": {
        "id": "MUS005",
        "name": "Can Öztürk",
        "email": "can.ozturk@email.com",
        "phone": "0538 654 3210",
        "address": "Muratpaşa, Antalya"
    }
}

# ============================================================
# SİPARİŞ VERİTABANI
# ============================================================
ORDERS = {
    "SP1001": {
        "id": "SP1001",
        "customer_id": "MUS001",
        "customer_name": "Ahmet Yılmaz",
        "products": [
            {"product_id": "PRD001", "name": "iPhone 15 Pro Max", "quantity": 1, "price": 74999.99}
        ],
        "total": 74999.99,
        "status": "Kargoda",
        "cargo_company": "Yurtiçi Kargo",
        "tracking_number": "YK7839201456",
        "order_date": "2026-05-08",
        "estimated_delivery": "2026-05-14",
        "address": "Kadıköy, İstanbul",
        "notes": "Kapıda ödeme"
    },
    "SP1002": {
        "id": "SP1002",
        "customer_id": "MUS002",
        "customer_name": "Elif Demir",
        "products": [
            {"product_id": "PRD004", "name": "Sony WH-1000XM5", "quantity": 1, "price": 12499.99},
            {"product_id": "PRD010", "name": "JBL Charge 5", "quantity": 1, "price": 4999.99}
        ],
        "total": 17499.98,
        "status": "Teslim Edildi",
        "cargo_company": "Aras Kargo",
        "tracking_number": "AK4521098763",
        "order_date": "2026-05-01",
        "estimated_delivery": "2026-05-05",
        "delivery_date": "2026-05-04",
        "address": "Çankaya, Ankara",
        "notes": ""
    },
    "SP1003": {
        "id": "SP1003",
        "customer_id": "MUS003",
        "customer_name": "Mehmet Kaya",
        "products": [
            {"product_id": "PRD003", "name": "MacBook Air M3", "quantity": 1, "price": 49999.99},
            {"product_id": "PRD013", "name": "iPad Air M2", "quantity": 1, "price": 27999.99}
        ],
        "total": 77999.98,
        "status": "Hazırlanıyor",
        "cargo_company": None,
        "tracking_number": None,
        "order_date": "2026-05-12",
        "estimated_delivery": "2026-05-16",
        "address": "Bornova, İzmir",
        "notes": "Hediye paketi yapılsın"
    },
    "SP1004": {
        "id": "SP1004",
        "customer_id": "MUS001",
        "customer_name": "Ahmet Yılmaz",
        "products": [
            {"product_id": "PRD005", "name": "Nike Air Max 270", "quantity": 2, "price": 4299.99}
        ],
        "total": 8599.98,
        "status": "Teslim Edildi",
        "cargo_company": "MNG Kargo",
        "tracking_number": "MN9087654321",
        "order_date": "2026-04-25",
        "estimated_delivery": "2026-04-30",
        "delivery_date": "2026-04-29",
        "address": "Kadıköy, İstanbul",
        "notes": ""
    },
    "SP1005": {
        "id": "SP1005",
        "customer_id": "MUS004",
        "customer_name": "Zeynep Arslan",
        "products": [
            {"product_id": "PRD007", "name": "Dyson V15 Detect", "quantity": 1, "price": 29999.99}
        ],
        "total": 29999.99,
        "status": "İptal Edildi",
        "cargo_company": None,
        "tracking_number": None,
        "order_date": "2026-05-10",
        "estimated_delivery": None,
        "cancel_reason": "Müşteri talebi ile iptal edildi",
        "address": "Nilüfer, Bursa",
        "notes": ""
    },
    "SP1006": {
        "id": "SP1006",
        "customer_id": "MUS005",
        "customer_name": "Can Öztürk",
        "products": [
            {"product_id": "PRD008", "name": "Philips Airfryer XXL", "quantity": 1, "price": 8499.99},
            {"product_id": "PRD012", "name": "Arzum Okka Minio", "quantity": 1, "price": 3299.99}
        ],
        "total": 11799.98,
        "status": "Kargoya Verildi",
        "cargo_company": "PTT Kargo",
        "tracking_number": "PT1234567890",
        "order_date": "2026-05-11",
        "estimated_delivery": "2026-05-15",
        "address": "Muratpaşa, Antalya",
        "notes": ""
    },
    "SP1007": {
        "id": "SP1007",
        "customer_id": "MUS002",
        "customer_name": "Elif Demir",
        "products": [
            {"product_id": "PRD014", "name": "The North Face Puffer", "quantity": 1, "price": 7999.99}
        ],
        "total": 7999.99,
        "status": "Kargoda",
        "cargo_company": "Sürat Kargo",
        "tracking_number": "SK6789012345",
        "order_date": "2026-05-09",
        "estimated_delivery": "2026-05-14",
        "address": "Çankaya, Ankara",
        "notes": ""
    },
    "SP1008": {
        "id": "SP1008",
        "customer_id": "MUS003",
        "customer_name": "Mehmet Kaya",
        "products": [
            {"product_id": "PRD016", "name": "PS5 DualSense Controller", "quantity": 2, "price": 2499.99},
            {"product_id": "PRD002", "name": "Samsung Galaxy S24 Ultra", "quantity": 1, "price": 64999.99}
        ],
        "total": 69999.97,
        "status": "Ödeme Bekleniyor",
        "cargo_company": None,
        "tracking_number": None,
        "order_date": "2026-05-13",
        "estimated_delivery": None,
        "address": "Bornova, İzmir",
        "notes": "Havale ile ödeme yapılacak"
    },
    "SP1009": {
        "id": "SP1009",
        "customer_id": "MUS004",
        "customer_name": "Zeynep Arslan",
        "products": [
            {"product_id": "PRD015", "name": "Robot Süpürge Roborock S8", "quantity": 1, "price": 22999.99}
        ],
        "total": 22999.99,
        "status": "Kargoda",
        "cargo_company": "Yurtiçi Kargo",
        "tracking_number": "YK1122334455",
        "order_date": "2026-05-07",
        "estimated_delivery": "2026-05-13",
        "address": "Nilüfer, Bursa",
        "notes": ""
    },
    "SP1010": {
        "id": "SP1010",
        "customer_id": "MUS005",
        "customer_name": "Can Öztürk",
        "products": [
            {"product_id": "PRD011", "name": "Adidas Ultraboost 23", "quantity": 1, "price": 5499.99},
            {"product_id": "PRD005", "name": "Nike Air Max 270", "quantity": 1, "price": 4299.99}
        ],
        "total": 9799.98,
        "status": "Teslim Edildi",
        "cargo_company": "Aras Kargo",
        "tracking_number": "AK9988776655",
        "order_date": "2026-04-28",
        "estimated_delivery": "2026-05-03",
        "delivery_date": "2026-05-02",
        "address": "Muratpaşa, Antalya",
        "notes": ""
    },
    "SP1011": {
        "id": "SP1011",
        "customer_id": "MUS001",
        "customer_name": "Ahmet Yılmaz",
        "products": [
            {"product_id": "PRD009", "name": "Apple Watch Series 9", "quantity": 1, "price": 17999.99}
        ],
        "total": 17999.99,
        "status": "İade Sürecinde",
        "cargo_company": "Yurtiçi Kargo",
        "tracking_number": "YK5566778899",
        "order_date": "2026-04-20",
        "delivery_date": "2026-04-24",
        "return_reason": "Ürün beklentileri karşılamadı",
        "return_status": "İade kargoya verildi, depoya ulaşması bekleniyor",
        "address": "Kadıköy, İstanbul",
        "notes": ""
    }
}

# ============================================================
# İADE TALEPLERİ
# ============================================================
RETURN_REQUESTS = []

_return_counter = 5000


def get_next_return_id():
    """Yeni iade talebi ID'si oluştur."""
    global _return_counter
    _return_counter += 1
    return f"IAD{_return_counter}"
