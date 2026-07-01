import streamlit as st
import streamlit.components.v1 as components
import sqlite3
import pandas as pd
from datetime import datetime, date

# ==========================================================
# Smart Parking Management System
# Developed by Osamah AL-murisi
# Python + Streamlit + SQLite
# ==========================================================

DB_NAME = "parking_system.db"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "Osamah2002"

LEFT_CAR_IMAGE = "https://images.unsplash.com/photo-1494976388531-d1058494cdd8?auto=format&fit=crop&w=900&q=80"
RIGHT_CAR_IMAGE = "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=900&q=80"

CAR_TYPES = {
    "Sedan": "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&w=900&q=80",
    "SUV": "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?auto=format&fit=crop&w=900&q=80",
    "Sports Car": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=900&q=80",
    "Pickup Truck": "https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?auto=format&fit=crop&w=900&q=80",
    "Electric Car": "https://images.unsplash.com/photo-1560958089-b8a1929cea89?auto=format&fit=crop&w=900&q=80",
    "Luxury Car": "https://images.unsplash.com/photo-1542362567-b07e54358753?auto=format&fit=crop&w=900&q=80",
}

TRANSLATIONS = {
    "en": {
        "language_name": "English",
        "choose_language": "Choose Language",
        "home": "Home",
        "parking_slots": "Parking Slots",
        "book_slot": "Book Slot",
        "receipt": "Receipt",
        "cancel_booking": "Cancel Booking",
        "admin_dashboard": "Admin Dashboard",
        "developed_by": "Developed by",
        "app_title": "Smart Parking Management System",
        "app_desc": "A professional digital system for managing parking spaces, reservations, car types, online payments, invoices, search, and admin operations.",
        "total_slots": "Total Slots",
        "available": "Available",
        "booked": "Booked",
        "hourly_capacity": "Hourly Capacity",
        "daily_capacity": "Daily Capacity",
        "project_features": "Project Features",
        "parking_slot_management": "Parking Slot Management",
        "parking_slot_management_text": "View all parking slots, check availability, and manage booked or available spaces easily.",
        "smart_booking": "Smart Booking",
        "smart_booking_text": "Customers can book a parking slot by entering their information, car plate number, date, and time.",
        "automatic_price": "Automatic Price Calculation",
        "automatic_price_text": "The system calculates the total price automatically using hourly and daily parking rates.",
        "online_payment_options": "Online Payment Options",
        "online_payment_options_text": "Supports Cash, Credit Card, and Online Payment with provider name and transaction ID.",
        "booking_receipt": "Booking Receipt",
        "booking_receipt_text": "Generates a professional receipt after booking with customer, car, slot, price, and payment details.",
        "admin_dashboard_feature": "Admin Dashboard",
        "admin_dashboard_feature_text": "Admin can add, delete, update slots, export CSV files, search bookings, and track income.",
        "car_types_supported": "Car Types Supported",
        "slots_status_prices": "Parking Slots Status & Prices",
        "hour": "hour",
        "day": "day",
        "vip_available": "VIP Available",
        "customer_name": "Customer Name",
        "phone_number": "Phone Number",
        "car_plate": "Car Plate Number",
        "choose_car_type": "Choose Car Type",
        "selected_car_type": "Selected Car Type",
        "choose_available_slot": "Choose Available Slot",
        "start_date": "Start Date",
        "end_date": "End Date",
        "hours_per_day": "Hours per Day",
        "payment_method": "Payment Method",
        "payment_status": "Payment Status",
        "online_provider": "Online Payment Provider",
        "transaction_id": "Transaction ID",
        "cash": "Cash",
        "credit_card": "Credit Card",
        "online_payment": "Online Payment",
        "paid": "Paid",
        "pending": "Pending",
        "failed": "Failed",
        "pay_note": "Online payment is simulated for the project. No real card or bank information is required.",
        "slot": "Slot",
        "car_type": "Car Type",
        "hourly_price": "Hourly Price",
        "daily_max": "Daily Max Price",
        "days": "Days",
        "one_day_cost": "One Day Cost",
        "total_price": "Total Price",
        "book_now": "Book Now",
        "no_available_slots": "No available parking slots right now.",
        "end_date_error": "End date must be after or equal to start date.",
        "please_fill": "Please fill these fields:",
        "book_success": "booked successfully! Total price:",
        "no_receipt": "No receipt available yet. Please make a booking first.",
        "download_receipt": "Download Receipt TXT",
        "booking_time": "Booking Time",
        "search_cancel": "Search by name, phone, car plate, slot, payment, or transaction",
        "no_bookings": "No bookings found.",
        "no_matching": "No matching booking found.",
        "choose_slot_cancel": "Choose Slot to Cancel",
        "confirm_cancel": "I confirm cancelling this booking",
        "cancel_success": "Booking cancelled successfully!",
        "admin_username": "Admin Username",
        "admin_password": "Admin Password",
        "admin_success": "Admin login successful.",
        "wrong_admin": "Wrong admin username or password.",
        "paid_income": "Paid Income",
        "online_income": "Online Income",
        "search_bookings": "Search Bookings",
        "parking_slots_table": "Parking Slots Table",
        "bookings_table": "Bookings Table",
        "download_slots_csv": "Download Parking Slots CSV",
        "download_bookings_csv": "Download Bookings CSV",
        "manage_slots": "Manage Parking Slots & Prices",
        "new_slot": "New Slot Number, example: F1 or VIP11",
        "new_hourly": "New Slot Hourly Price $",
        "new_daily": "New Slot Daily Max Price $",
        "add_new_slot": "Add New Slot",
        "enter_slot": "Please enter slot number.",
        "slot_added": "Slot added successfully.",
        "choose_update_price": "Choose Slot to Update Prices",
        "updated_hourly": "Updated Hourly Price $",
        "updated_daily": "Updated Daily Max Price $",
        "update_prices": "Update Prices",
        "prices_updated": "Prices updated successfully.",
        "choose_delete_slot": "Choose Slot to Delete",
        "confirm_delete": "I confirm deleting this slot",
        "delete_slot": "Delete Slot",
        "slot_deleted": "Slot deleted successfully!",
        "reset_warning": "Reset System will delete all bookings and restore default slots and prices.",
        "confirm_reset": "I confirm resetting the whole system",
        "reset_system": "Reset System",
        "reset_success": "System reset successfully.",
        "footer": "Smart Parking Management System | Python • Streamlit • SQLite",
    },
    "ar": {
        "language_name": "العربية",
        "choose_language": "اختر اللغة",
        "home": "الرئيسية",
        "parking_slots": "المواقف",
        "book_slot": "حجز موقف",
        "receipt": "الإيصال",
        "cancel_booking": "إلغاء الحجز",
        "admin_dashboard": "لوحة المشرف",
        "developed_by": "تم التطوير بواسطة",
        "app_title": "نظام إدارة مواقف السيارات الذكي",
        "app_desc": "نظام رقمي احترافي لإدارة المواقف، الحجوزات، أنواع السيارات، الدفع الإلكتروني، الإيصالات، البحث، وعمليات المشرف.",
        "total_slots": "إجمالي المواقف",
        "available": "متاح",
        "booked": "محجوز",
        "hourly_capacity": "الطاقة السعرية بالساعة",
        "daily_capacity": "الطاقة السعرية باليوم",
        "project_features": "مميزات المشروع",
        "parking_slot_management": "إدارة المواقف",
        "parking_slot_management_text": "عرض جميع المواقف ومعرفة المتاح والمحجوز وإدارة المساحات بسهولة.",
        "smart_booking": "حجز ذكي",
        "smart_booking_text": "يمكن للعميل حجز موقف بإدخال بياناته ورقم السيارة والتاريخ والوقت.",
        "automatic_price": "حساب السعر تلقائيًا",
        "automatic_price_text": "يقوم النظام بحساب السعر تلقائيًا حسب سعر الساعة والسعر اليومي.",
        "online_payment_options": "خيارات الدفع الإلكتروني",
        "online_payment_options_text": "يدعم الدفع نقدًا، البطاقة، والدفع الإلكتروني مع مزود الدفع ورقم المعاملة.",
        "booking_receipt": "إيصال الحجز",
        "booking_receipt_text": "ينشئ إيصالًا احترافيًا بعد الحجز يحتوي على بيانات العميل والسيارة والموقف والسعر والدفع.",
        "admin_dashboard_feature": "لوحة تحكم المشرف",
        "admin_dashboard_feature_text": "يمكن للمشرف إضافة وحذف وتعديل المواقف، تصدير CSV، البحث في الحجوزات، ومتابعة الدخل.",
        "car_types_supported": "أنواع السيارات المدعومة",
        "slots_status_prices": "حالة المواقف والأسعار",
        "hour": "ساعة",
        "day": "يوم",
        "vip_available": "VIP متاح",
        "customer_name": "اسم العميل",
        "phone_number": "رقم الهاتف",
        "car_plate": "رقم لوحة السيارة",
        "choose_car_type": "اختر نوع السيارة",
        "selected_car_type": "نوع السيارة المختار",
        "choose_available_slot": "اختر موقفًا متاحًا",
        "start_date": "تاريخ البداية",
        "end_date": "تاريخ النهاية",
        "hours_per_day": "عدد الساعات في اليوم",
        "payment_method": "طريقة الدفع",
        "payment_status": "حالة الدفع",
        "online_provider": "مزود الدفع الإلكتروني",
        "transaction_id": "رقم المعاملة",
        "cash": "نقدًا",
        "credit_card": "بطاقة ائتمان",
        "online_payment": "دفع إلكتروني",
        "paid": "مدفوع",
        "pending": "معلق",
        "failed": "فشل",
        "pay_note": "الدفع الإلكتروني هنا محاكاة لأغراض المشروع، ولا يحتاج إدخال بيانات بطاقة أو بنك حقيقية.",
        "slot": "الموقف",
        "car_type": "نوع السيارة",
        "hourly_price": "السعر بالساعة",
        "daily_max": "الحد اليومي",
        "days": "الأيام",
        "one_day_cost": "تكلفة اليوم الواحد",
        "total_price": "السعر الإجمالي",
        "book_now": "احجز الآن",
        "no_available_slots": "لا توجد مواقف متاحة حاليًا.",
        "end_date_error": "تاريخ النهاية يجب أن يكون بعد أو يساوي تاريخ البداية.",
        "please_fill": "يرجى تعبئة هذه الحقول:",
        "book_success": "تم حجزه بنجاح! السعر الإجمالي:",
        "no_receipt": "لا يوجد إيصال حاليًا. يرجى عمل حجز أولًا.",
        "download_receipt": "تحميل الإيصال TXT",
        "booking_time": "وقت الحجز",
        "search_cancel": "ابحث بالاسم، الهاتف، رقم السيارة، الموقف، الدفع، أو رقم المعاملة",
        "no_bookings": "لا توجد حجوزات.",
        "no_matching": "لا توجد نتيجة مطابقة.",
        "choose_slot_cancel": "اختر الموقف لإلغاء الحجز",
        "confirm_cancel": "أؤكد إلغاء هذا الحجز",
        "cancel_success": "تم إلغاء الحجز بنجاح!",
        "admin_username": "اسم مستخدم المشرف",
        "admin_password": "كلمة مرور المشرف",
        "admin_success": "تم تسجيل دخول المشرف بنجاح.",
        "wrong_admin": "اسم المستخدم أو كلمة المرور غير صحيحة.",
        "paid_income": "الدخل المدفوع",
        "online_income": "دخل الدفع الإلكتروني",
        "search_bookings": "البحث في الحجوزات",
        "parking_slots_table": "جدول المواقف",
        "bookings_table": "جدول الحجوزات",
        "download_slots_csv": "تحميل المواقف CSV",
        "download_bookings_csv": "تحميل الحجوزات CSV",
        "manage_slots": "إدارة المواقف والأسعار",
        "new_slot": "رقم موقف جديد، مثال: F1 أو VIP11",
        "new_hourly": "سعر الموقف الجديد بالساعة $",
        "new_daily": "السعر اليومي للموقف الجديد $",
        "add_new_slot": "إضافة موقف جديد",
        "enter_slot": "يرجى إدخال رقم الموقف.",
        "slot_added": "تمت إضافة الموقف بنجاح.",
        "choose_update_price": "اختر موقفًا لتعديل الأسعار",
        "updated_hourly": "السعر الجديد بالساعة $",
        "updated_daily": "السعر اليومي الجديد $",
        "update_prices": "تحديث الأسعار",
        "prices_updated": "تم تحديث الأسعار بنجاح.",
        "choose_delete_slot": "اختر موقفًا للحذف",
        "confirm_delete": "أؤكد حذف هذا الموقف",
        "delete_slot": "حذف الموقف",
        "slot_deleted": "تم حذف الموقف بنجاح!",
        "reset_warning": "إعادة ضبط النظام ستحذف كل الحجوزات وتعيد المواقف والأسعار الافتراضية.",
        "confirm_reset": "أؤكد إعادة ضبط النظام بالكامل",
        "reset_system": "إعادة ضبط النظام",
        "reset_success": "تمت إعادة ضبط النظام بنجاح.",
        "footer": "نظام إدارة مواقف السيارات الذكي | Python • Streamlit • SQLite",
    },
    "tr": {
        "language_name": "Türkçe",
        "choose_language": "Dil Seçin",
        "home": "Ana Sayfa",
        "parking_slots": "Park Yerleri",
        "book_slot": "Yer Ayırt",
        "receipt": "Makbuz",
        "cancel_booking": "Rezervasyonu İptal Et",
        "admin_dashboard": "Yönetici Paneli",
        "developed_by": "Geliştiren",
        "app_title": "Akıllı Otopark Yönetim Sistemi",
        "app_desc": "Park yerleri, rezervasyonlar, araç türleri, çevrimiçi ödeme, makbuzlar, arama ve yönetici işlemleri için profesyonel dijital sistem.",
        "total_slots": "Toplam Yer",
        "available": "Müsait",
        "booked": "Dolu",
        "hourly_capacity": "Saatlik Kapasite",
        "daily_capacity": "Günlük Kapasite",
        "project_features": "Proje Özellikleri",
        "parking_slot_management": "Park Yeri Yönetimi",
        "parking_slot_management_text": "Tüm park yerlerini görüntüleme, müsaitlik kontrolü ve dolu/müsait alanları kolayca yönetme.",
        "smart_booking": "Akıllı Rezervasyon",
        "smart_booking_text": "Müşteriler bilgilerini, plaka numarasını, tarih ve saati girerek park yeri ayırtabilir.",
        "automatic_price": "Otomatik Fiyat Hesaplama",
        "automatic_price_text": "Sistem toplam ücreti saatlik ve günlük park ücretlerine göre otomatik hesaplar.",
        "online_payment_options": "Çevrimiçi Ödeme Seçenekleri",
        "online_payment_options_text": "Nakit, kredi kartı ve sağlayıcı/işlem numarası ile çevrimiçi ödeme desteklenir.",
        "booking_receipt": "Rezervasyon Makbuzu",
        "booking_receipt_text": "Rezervasyondan sonra müşteri, araç, yer, fiyat ve ödeme detaylarını içeren profesyonel makbuz oluşturur.",
        "admin_dashboard_feature": "Yönetici Paneli",
        "admin_dashboard_feature_text": "Yönetici yer ekleyebilir, silebilir, fiyatları güncelleyebilir, CSV dışa aktarabilir, rezervasyon arayabilir ve geliri takip edebilir.",
        "car_types_supported": "Desteklenen Araç Türleri",
        "slots_status_prices": "Park Yeri Durumu ve Fiyatları",
        "hour": "saat",
        "day": "gün",
        "vip_available": "VIP Müsait",
        "customer_name": "Müşteri Adı",
        "phone_number": "Telefon Numarası",
        "car_plate": "Araç Plaka Numarası",
        "choose_car_type": "Araç Türü Seçin",
        "selected_car_type": "Seçilen Araç Türü",
        "choose_available_slot": "Müsait Park Yeri Seçin",
        "start_date": "Başlangıç Tarihi",
        "end_date": "Bitiş Tarihi",
        "hours_per_day": "Günlük Saat",
        "payment_method": "Ödeme Yöntemi",
        "payment_status": "Ödeme Durumu",
        "online_provider": "Çevrimiçi Ödeme Sağlayıcısı",
        "transaction_id": "İşlem Numarası",
        "cash": "Nakit",
        "credit_card": "Kredi Kartı",
        "online_payment": "Çevrimiçi Ödeme",
        "paid": "Ödendi",
        "pending": "Beklemede",
        "failed": "Başarısız",
        "pay_note": "Çevrimiçi ödeme proje için simüle edilmiştir. Gerçek kart veya banka bilgisi gerekmez.",
        "slot": "Yer",
        "car_type": "Araç Türü",
        "hourly_price": "Saatlik Ücret",
        "daily_max": "Günlük Maksimum Ücret",
        "days": "Gün",
        "one_day_cost": "Bir Günlük Ücret",
        "total_price": "Toplam Ücret",
        "book_now": "Şimdi Ayırt",
        "no_available_slots": "Şu anda müsait park yeri yok.",
        "end_date_error": "Bitiş tarihi başlangıç tarihinden sonra veya aynı olmalıdır.",
        "please_fill": "Lütfen bu alanları doldurun:",
        "book_success": "başarıyla ayırtıldı! Toplam ücret:",
        "no_receipt": "Henüz makbuz yok. Lütfen önce rezervasyon yapın.",
        "download_receipt": "Makbuzu TXT Olarak İndir",
        "booking_time": "Rezervasyon Zamanı",
        "search_cancel": "Ad, telefon, plaka, yer, ödeme veya işlem numarası ile ara",
        "no_bookings": "Rezervasyon bulunamadı.",
        "no_matching": "Eşleşen rezervasyon bulunamadı.",
        "choose_slot_cancel": "İptal Edilecek Yeri Seçin",
        "confirm_cancel": "Bu rezervasyonu iptal etmeyi onaylıyorum",
        "cancel_success": "Rezervasyon başarıyla iptal edildi!",
        "admin_username": "Yönetici Kullanıcı Adı",
        "admin_password": "Yönetici Şifresi",
        "admin_success": "Yönetici girişi başarılı.",
        "wrong_admin": "Yönetici adı veya şifre yanlış.",
        "paid_income": "Ödenen Gelir",
        "online_income": "Çevrimiçi Gelir",
        "search_bookings": "Rezervasyonlarda Ara",
        "parking_slots_table": "Park Yerleri Tablosu",
        "bookings_table": "Rezervasyon Tablosu",
        "download_slots_csv": "Park Yerlerini CSV İndir",
        "download_bookings_csv": "Rezervasyonları CSV İndir",
        "manage_slots": "Park Yerleri ve Fiyatları Yönet",
        "new_slot": "Yeni yer numarası, örnek: F1 veya VIP11",
        "new_hourly": "Yeni Yer Saatlik Ücreti $",
        "new_daily": "Yeni Yer Günlük Maksimum Ücreti $",
        "add_new_slot": "Yeni Yer Ekle",
        "enter_slot": "Lütfen yer numarası girin.",
        "slot_added": "Yer başarıyla eklendi.",
        "choose_update_price": "Fiyat Güncellenecek Yeri Seçin",
        "updated_hourly": "Güncel Saatlik Ücret $",
        "updated_daily": "Güncel Günlük Maksimum Ücret $",
        "update_prices": "Fiyatları Güncelle",
        "prices_updated": "Fiyatlar başarıyla güncellendi.",
        "choose_delete_slot": "Silinecek Yeri Seçin",
        "confirm_delete": "Bu yeri silmeyi onaylıyorum",
        "delete_slot": "Yeri Sil",
        "slot_deleted": "Yer başarıyla silindi!",
        "reset_warning": "Sistemi sıfırlamak tüm rezervasyonları siler ve varsayılan yer/fiyatları geri yükler.",
        "confirm_reset": "Tüm sistemi sıfırlamayı onaylıyorum",
        "reset_system": "Sistemi Sıfırla",
        "reset_success": "Sistem başarıyla sıfırlandı.",
        "footer": "Akıllı Otopark Yönetim Sistemi | Python • Streamlit • SQLite",
    }
}


def t(key):
    lang = st.session_state.get("lang", "en")
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)


def get_lang_direction():
    return "rtl" if st.session_state.get("lang", "en") == "ar" else "ltr"


def method_to_db(label):
    if label in [t("cash"), "Cash", "Nakit", "نقدًا"]:
        return "Cash"
    if label in [t("credit_card"), "Credit Card", "Kredi Kartı", "بطاقة ائتمان"]:
        return "Credit Card"
    return "Online Payment"


def status_to_db(label):
    if label in [t("paid"), "Paid", "Ödendi", "مدفوع"]:
        return "Paid"
    if label in [t("failed"), "Failed", "Başarısız", "فشل"]:
        return "Failed"
    return "Pending"


# ==========================================================
# Database
# ==========================================================
def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS parking_slots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slot_number TEXT UNIQUE NOT NULL,
            status TEXT NOT NULL,
            hourly_rate REAL DEFAULT 3,
            daily_rate REAL DEFAULT 20
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL,
            phone_number TEXT,
            car_number TEXT NOT NULL,
            car_type TEXT DEFAULT 'Sedan',
            slot_number TEXT NOT NULL,
            start_date TEXT,
            end_date TEXT,
            days INTEGER DEFAULT 1,
            hours INTEGER DEFAULT 1,
            hourly_rate REAL DEFAULT 3,
            daily_rate REAL DEFAULT 20,
            total_price REAL DEFAULT 3,
            payment_method TEXT DEFAULT 'Cash',
            payment_status TEXT DEFAULT 'Pending',
            online_provider TEXT DEFAULT 'None',
            transaction_id TEXT DEFAULT 'None',
            booking_time TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def fix_old_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(parking_slots)")
    slot_columns = [col[1] for col in cursor.fetchall()]

    slot_needed = {
        "hourly_rate": "ALTER TABLE parking_slots ADD COLUMN hourly_rate REAL DEFAULT 3",
        "daily_rate": "ALTER TABLE parking_slots ADD COLUMN daily_rate REAL DEFAULT 20",
    }

    for col, sql in slot_needed.items():
        if col not in slot_columns:
            try:
                cursor.execute(sql)
            except sqlite3.OperationalError:
                pass

    cursor.execute("PRAGMA table_info(bookings)")
    booking_columns = [col[1] for col in cursor.fetchall()]

    booking_needed = {
        "phone_number": "ALTER TABLE bookings ADD COLUMN phone_number TEXT",
        "car_type": "ALTER TABLE bookings ADD COLUMN car_type TEXT DEFAULT 'Sedan'",
        "start_date": "ALTER TABLE bookings ADD COLUMN start_date TEXT",
        "end_date": "ALTER TABLE bookings ADD COLUMN end_date TEXT",
        "days": "ALTER TABLE bookings ADD COLUMN days INTEGER DEFAULT 1",
        "hours": "ALTER TABLE bookings ADD COLUMN hours INTEGER DEFAULT 1",
        "hourly_rate": "ALTER TABLE bookings ADD COLUMN hourly_rate REAL DEFAULT 3",
        "daily_rate": "ALTER TABLE bookings ADD COLUMN daily_rate REAL DEFAULT 20",
        "total_price": "ALTER TABLE bookings ADD COLUMN total_price REAL DEFAULT 3",
        "payment_method": "ALTER TABLE bookings ADD COLUMN payment_method TEXT DEFAULT 'Cash'",
        "payment_status": "ALTER TABLE bookings ADD COLUMN payment_status TEXT DEFAULT 'Pending'",
        "online_provider": "ALTER TABLE bookings ADD COLUMN online_provider TEXT DEFAULT 'None'",
        "transaction_id": "ALTER TABLE bookings ADD COLUMN transaction_id TEXT DEFAULT 'None'",
    }

    for col, sql in booking_needed.items():
        if col not in booking_columns:
            try:
                cursor.execute(sql)
            except sqlite3.OperationalError:
                pass

    conn.commit()
    conn.close()


def get_default_rates(slot_number):
    if slot_number.startswith("VIP"):
        return 8.0, 45.0

    section = slot_number[0]

    if section == "A":
        return 2.0, 12.0
    if section == "B":
        return 3.0, 18.0
    if section == "C":
        return 4.0, 24.0
    if section == "D":
        return 5.0, 30.0
    if section == "E":
        return 6.0, 35.0

    return 3.0, 20.0


def insert_default_slots():
    conn = get_connection()
    cursor = conn.cursor()

    slots = []

    for section in ["A", "B", "C", "D", "E"]:
        for i in range(1, 21):
            slots.append(f"{section}{i}")

    for i in range(1, 11):
        slots.append(f"VIP{i}")

    for slot in slots:
        hourly_rate, daily_rate = get_default_rates(slot)

        cursor.execute("""
            INSERT OR IGNORE INTO parking_slots 
            (slot_number, status, hourly_rate, daily_rate)
            VALUES (?, ?, ?, ?)
        """, (slot, "Available", hourly_rate, daily_rate))

    conn.commit()
    conn.close()


def reset_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM bookings")
    cursor.execute("DELETE FROM parking_slots")

    conn.commit()
    conn.close()

    insert_default_slots()


def get_all_slots():
    conn = get_connection()

    df = pd.read_sql_query("""
        SELECT id, slot_number, status, hourly_rate, daily_rate
        FROM parking_slots
        ORDER BY 
            CASE 
                WHEN slot_number LIKE 'VIP%' THEN 6
                WHEN slot_number LIKE 'A%' THEN 1
                WHEN slot_number LIKE 'B%' THEN 2
                WHEN slot_number LIKE 'C%' THEN 3
                WHEN slot_number LIKE 'D%' THEN 4
                WHEN slot_number LIKE 'E%' THEN 5
                ELSE 7
            END,
            CAST(
                CASE 
                    WHEN slot_number LIKE 'VIP%' THEN REPLACE(slot_number, 'VIP', '')
                    ELSE SUBSTR(slot_number, 2)
                END AS INTEGER
            )
    """, conn)

    conn.close()
    return df


def get_available_slots():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT slot_number
        FROM parking_slots
        WHERE status = 'Available'
        ORDER BY slot_number
    """)

    data = cursor.fetchall()
    conn.close()

    return [x[0] for x in data]


def get_slot_rates(slot_number):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT hourly_rate, daily_rate
        FROM parking_slots
        WHERE slot_number = ?
    """, (slot_number,))

    result = cursor.fetchone()
    conn.close()

    if result:
        return float(result[0]), float(result[1])

    return 3.0, 20.0


def calculate_days(start_date, end_date):
    return max((end_date - start_date).days + 1, 1)


def calculate_total_price(hourly_rate, daily_rate, days, hours):
    one_day_cost = min(hourly_rate * hours, daily_rate)
    return one_day_cost * days


def get_bookings():
    conn = get_connection()

    df = pd.read_sql_query("""
        SELECT 
            id,
            user_name,
            phone_number,
            car_number,
            car_type,
            slot_number,
            start_date,
            end_date,
            days,
            hours,
            hourly_rate,
            daily_rate,
            total_price,
            payment_method,
            payment_status,
            online_provider,
            transaction_id,
            booking_time
        FROM bookings
        ORDER BY booking_time DESC
    """, conn)

    conn.close()
    return df


def book_slot(
    user_name,
    phone_number,
    car_number,
    car_type,
    slot_number,
    start_date,
    end_date,
    days,
    hours,
    payment_method,
    payment_status,
    online_provider,
    transaction_id
):
    conn = get_connection()
    cursor = conn.cursor()

    booking_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    hourly_rate, daily_rate = get_slot_rates(slot_number)
    total_price = calculate_total_price(hourly_rate, daily_rate, days, hours)

    cursor.execute("""
        INSERT INTO bookings 
        (
            user_name, phone_number, car_number, car_type, slot_number,
            start_date, end_date, days, hours,
            hourly_rate, daily_rate, total_price,
            payment_method, payment_status, online_provider, transaction_id, booking_time
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_name,
        phone_number,
        car_number,
        car_type,
        slot_number,
        str(start_date),
        str(end_date),
        days,
        hours,
        hourly_rate,
        daily_rate,
        total_price,
        payment_method,
        payment_status,
        online_provider,
        transaction_id,
        booking_time
    ))

    cursor.execute("""
        UPDATE parking_slots
        SET status = 'Booked'
        WHERE slot_number = ?
    """, (slot_number,))

    conn.commit()
    conn.close()

    return {
        "user_name": user_name,
        "phone_number": phone_number,
        "car_number": car_number,
        "car_type": car_type,
        "slot_number": slot_number,
        "start_date": str(start_date),
        "end_date": str(end_date),
        "days": days,
        "hours": hours,
        "hourly_rate": hourly_rate,
        "daily_rate": daily_rate,
        "total_price": total_price,
        "payment_method": payment_method,
        "payment_status": payment_status,
        "online_provider": online_provider,
        "transaction_id": transaction_id,
        "booking_time": booking_time
    }


def cancel_booking(slot_number):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM bookings WHERE slot_number = ?", (slot_number,))
    cursor.execute("UPDATE parking_slots SET status = 'Available' WHERE slot_number = ?", (slot_number,))

    conn.commit()
    conn.close()


def add_parking_slot(slot_number, hourly_rate, daily_rate):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO parking_slots 
        (slot_number, status, hourly_rate, daily_rate)
        VALUES (?, ?, ?, ?)
    """, (slot_number, "Available", hourly_rate, daily_rate))

    conn.commit()
    conn.close()


def update_slot_prices(slot_number, hourly_rate, daily_rate):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE parking_slots
        SET hourly_rate = ?, daily_rate = ?
        WHERE slot_number = ?
    """, (hourly_rate, daily_rate, slot_number))

    conn.commit()
    conn.close()


def delete_parking_slot(slot_number):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM bookings WHERE slot_number = ?", (slot_number,))
    cursor.execute("DELETE FROM parking_slots WHERE slot_number = ?", (slot_number,))

    conn.commit()
    conn.close()


def dataframe_to_csv_bytes(df):
    return df.to_csv(index=False).encode("utf-8-sig")


def create_receipt_text(invoice):
    return f"""
========================================
SMART PARKING BOOKING RECEIPT
========================================
Customer Name : {invoice.get("user_name", "")}
Phone Number  : {invoice.get("phone_number", "")}
Car Plate No. : {invoice.get("car_number", "")}
Car Type      : {invoice.get("car_type", "")}
Slot Number   : {invoice.get("slot_number", "")}

Start Date    : {invoice.get("start_date", "")}
End Date      : {invoice.get("end_date", "")}
Days          : {invoice.get("days", "")}
Hours / Day   : {invoice.get("hours", "")}

Hourly Price  : ${float(invoice.get("hourly_rate", 0)):.2f}
Daily Max     : ${float(invoice.get("daily_rate", 0)):.2f}
Total Price   : ${float(invoice.get("total_price", 0)):.2f}

Payment Method : {invoice.get("payment_method", "")}
Payment Status : {invoice.get("payment_status", "")}
Online Provider: {invoice.get("online_provider", "")}
Transaction ID : {invoice.get("transaction_id", "")}

Booking Time  : {invoice.get("booking_time", "")}
========================================
Developed by Osamah AL-murisi
========================================
"""


# ==========================================================
# Style
# ==========================================================
def apply_style():
    direction = get_lang_direction()

    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Cairo', sans-serif;
            direction: {direction};
        }}

        .stApp {{
            background: linear-gradient(135deg, #07111f 0%, #0f172a 50%, #102a43 100%);
            color: white;
        }}

        header[data-testid="stHeader"],
        div[data-testid="stToolbar"],
        div[data-testid="stDecoration"],
        div[data-testid="stStatusWidget"],
        section[data-testid="stSidebar"] {{
            display: none !important;
        }}

        #MainMenu, footer {{
            visibility: hidden !important;
        }}

        .block-container {{
            max-width: 1450px !important;
            padding-top: 0rem !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
            padding-bottom: 3rem !important;
        }}

        .lang-box {{
            width: 260px;
            margin: 10px auto 10px auto;
        }}

        .st-key-menu_toggle_btn {{
            display: flex !important;
            justify-content: center !important;
        }}

        .st-key-menu_toggle_btn button {{
            background: transparent !important;
            color: white !important;
            border: none !important;
            width: 115px !important;
            height: 65px !important;
            font-size: 44px !important;
            font-weight: 900 !important;
            box-shadow: none !important;
            margin-top: -155px !important;
            margin-bottom: 25px !important;
            text-shadow: 0 5px 20px rgba(0,0,0,0.55) !important;
            cursor: pointer !important;
        }}

        div[data-testid="stExpander"] {{
            width: 560px !important;
            max-width: 94% !important;
            margin: -38px auto 30px auto !important;
            background: rgba(255,255,255,0.08) !important;
            border: 1px solid rgba(255,255,255,0.18) !important;
            border-radius: 24px !important;
            box-shadow: 0 22px 50px rgba(0,0,0,0.38) !important;
            overflow: hidden !important;
            padding-bottom: 18px !important;
        }}

        div[data-testid="stExpander"] summary {{
            min-height: 55px !important;
            padding: 10px 22px !important;
            background: rgba(15,23,42,0.90) !important;
            color: white !important;
            font-size: 22px !important;
            font-weight: 900 !important;
        }}

        div[data-testid="stExpander"] summary p {{
            color: white !important;
            font-size: 22px !important;
            font-weight: 900 !important;
        }}

        .st-key-menu_home,
        .st-key-menu_slots,
        .st-key-menu_book,
        .st-key-menu_receipt,
        .st-key-menu_cancel,
        .st-key-menu_admin {{
            width: 100% !important;
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
        }}

        .st-key-menu_home button,
        .st-key-menu_slots button,
        .st-key-menu_book button,
        .st-key-menu_receipt button,
        .st-key-menu_cancel button,
        .st-key-menu_admin button {{
            width: 380px !important;
            max-width: 380px !important;
            min-width: 380px !important;
            height: 58px !important;
            background: linear-gradient(135deg, rgba(30,41,59,0.96), rgba(51,65,85,0.96)) !important;
            color: white !important;
            border-radius: 17px !important;
            margin: 7px auto 14px auto !important;
            font-weight: 900 !important;
            font-size: 16px !important;
            border: 1px solid rgba(255,255,255,0.16) !important;
            box-shadow: 0 12px 25px rgba(0,0,0,0.22) !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            text-align: center !important;
            white-space: nowrap !important;
        }}

        .st-key-menu_home button:hover,
        .st-key-menu_slots button:hover,
        .st-key-menu_book button:hover,
        .st-key-menu_receipt button:hover,
        .st-key-menu_cancel button:hover,
        .st-key-menu_admin button:hover {{
            background: linear-gradient(135deg, rgba(14,165,233,0.38), rgba(20,184,166,0.30)) !important;
            border: 1px solid rgba(56,189,248,0.60) !important;
            transform: scale(1.01) !important;
        }}

        .side-dev {{
            width: 380px !important;
            max-width: 380px !important;
            min-width: 380px !important;
            margin: 22px auto 0 auto !important;
            padding: 16px 20px !important;
            border-radius: 18px !important;
            background: linear-gradient(135deg, rgba(14,165,233,0.34), rgba(20,184,166,0.26)) !important;
            border: 1px solid rgba(56,189,248,0.45) !important;
            text-align: center !important;
            color: #38bdf8 !important;
            font-weight: 900 !important;
            font-size: 15px !important;
            line-height: 1.8 !important;
            box-shadow: 0 12px 30px rgba(0,0,0,0.25) !important;
            user-select: none !important;
        }}

        .section-title {{
            font-size: 34px;
            font-weight: 900;
            color: white;
            margin: 0 0 15px 0;
            text-shadow: 0 4px 15px rgba(0,0,0,0.7);
        }}

        .note {{
            color: #cbd5e1;
            font-size: 18px;
            margin-bottom: 22px;
            line-height: 1.8;
            font-weight: 600;
        }}

        div[data-testid="stMetric"] {{
            background: rgba(255,255,255,0.08);
            padding: 22px;
            border-radius: 22px;
            border: 1px solid rgba(255,255,255,0.14);
            box-shadow: 0 15px 35px rgba(0,0,0,0.22);
        }}

        div[data-testid="stMetric"] label {{
            color: #cbd5e1 !important;
            font-size: 16px !important;
            font-weight: 800 !important;
        }}

        div[data-testid="stMetricValue"] {{
            color: white !important;
            font-size: 34px !important;
            font-weight: 900 !important;
        }}

        .feature-card {{
            background: rgba(56,189,248,0.12);
            border: 1px solid rgba(56,189,248,0.35);
            border-radius: 22px;
            padding: 28px;
            min-height: 210px;
            text-align: center;
            margin-bottom: 22px;
            box-shadow: 0 16px 35px rgba(0,0,0,0.25);
            transition: 0.3s ease-in-out;
        }}

        .feature-card:hover {{
            transform: translateY(-6px);
            background: rgba(56,189,248,0.18);
            border: 1px solid rgba(56,189,248,0.60);
        }}

        .feature-icon {{
            font-size: 44px;
            margin-bottom: 12px;
        }}

        .feature-title {{
            font-size: 20px;
            font-weight: 900;
            color: white;
            margin-bottom: 10px;
        }}

        .feature-text {{
            font-size: 15px;
            color: #cbd5e1;
            line-height: 1.7;
            font-weight: 700;
        }}

        .parking-card {{
            padding: 18px;
            border-radius: 22px;
            text-align: center;
            font-size: 15px;
            font-weight: 900;
            margin-bottom: 17px;
            box-shadow: 0 14px 30px rgba(0,0,0,0.22);
        }}

        .available {{
            background: linear-gradient(135deg, #dcfce7, #86efac);
            color: #14532d;
            border: 2px solid #22c55e;
        }}

        .booked {{
            background: linear-gradient(135deg, #fee2e2, #fca5a5);
            color: #7f1d1d;
            border: 2px solid #ef4444;
        }}

        .vip {{
            background: linear-gradient(135deg, #fef3c7, #fbbf24);
            color: #78350f;
            border: 2px solid #f59e0b;
        }}

        .price-box, .receipt-box, .car-preview, .payment-box {{
            background: rgba(56,189,248,0.12);
            border: 1px solid rgba(56,189,248,0.35);
            border-radius: 18px;
            padding: 18px;
            color: #e0f2fe;
            font-size: 17px;
            font-weight: 900;
            margin: 18px 0;
            text-align: center;
            box-shadow: 0 12px 30px rgba(0,0,0,0.20);
        }}

        .receipt-box {{
            text-align: {("right" if direction == "rtl" else "left")};
            line-height: 1.8;
        }}

        .car-img {{
            width: 100%;
            max-width: 520px;
            height: 260px;
            object-fit: cover;
            border-radius: 22px;
            border: 2px solid rgba(56,189,248,0.55);
            box-shadow: 0 15px 35px rgba(0,0,0,0.35);
            margin-top: 10px;
        }}

        .stButton>button {{
            background: linear-gradient(135deg, #0ea5e9, #14b8a6);
            color: white;
            border-radius: 14px;
            min-height: 48px;
            font-size: 17px;
            font-weight: 900;
            border: none;
            padding: 0 26px;
        }}

        input, textarea, select {{
            border-radius: 14px !important;
        }}

        .stAlert {{
            border-radius: 16px;
        }}

        div[data-testid="stDataFrame"] {{
            border-radius: 18px;
            overflow: hidden;
        }}

        .footer {{
            margin-top: 40px;
            padding: 20px;
            text-align: center;
            color: #cbd5e1;
            background: rgba(255,255,255,0.06);
            border-radius: 18px;
            border: 1px solid rgba(255,255,255,0.12);
        }}
        </style>
    """, unsafe_allow_html=True)


# ==========================================================
# Header
# ==========================================================
def car_header():
    components.html(f"""
    <html>
    <head>
    <style>
        body {{
            margin: 0;
            padding: 0;
            background: transparent;
        }}

        .purple-menu-bar {{
            width: 100%;
            height: 185px;
            background: linear-gradient(135deg, #8b00ff, #6a00d4);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 70px;
            box-sizing: border-box;
            overflow: hidden;
        }}

        .car-box {{
            width: 245px;
            height: 140px;
            border-radius: 25px;
            overflow: hidden;
            border: 3px solid rgba(255,255,255,0.45);
            box-shadow: 0 15px 35px rgba(0,0,0,0.45);
            background: rgba(255,255,255,0.12);
        }}

        .car-box img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: block;
        }}

        .center-space {{
            width: 160px;
            height: 80px;
        }}
    </style>
    </head>
    <body>
        <div class="purple-menu-bar">
            <div class="car-box">
                <img src="{LEFT_CAR_IMAGE}">
            </div>
            <div class="center-space"></div>
            <div class="car-box">
                <img src="{RIGHT_CAR_IMAGE}">
            </div>
        </div>
    </body>
    </html>
    """, height=190)


def language_selector():
    lang_options = {
        "English 🇬🇧": "en",
        "العربية 🇸🇦": "ar",
        "Türkçe 🇹🇷": "tr",
    }

    current_lang = st.session_state.get("lang", "en")
    reverse = {v: k for k, v in lang_options.items()}

    selected = st.selectbox(
        t("choose_language"),
        list(lang_options.keys()),
        index=list(lang_options.keys()).index(reverse[current_lang]),
        key="language_select_box"
    )

    new_lang = lang_options[selected]

    if new_lang != st.session_state.get("lang", "en"):
        st.session_state.lang = new_lang
        st.rerun()


# ==========================================================
# Pages
# ==========================================================
def home_page():
    slots_df = get_all_slots()

    total_slots = len(slots_df)
    available_slots = len(slots_df[slots_df["status"] == "Available"])
    booked_slots = len(slots_df[slots_df["status"] == "Booked"])
    total_hourly_capacity = slots_df["hourly_rate"].sum()
    total_daily_capacity = slots_df["daily_rate"].sum()

    st.markdown(f'<div class="section-title">🚗 {t("app_title")}</div>', unsafe_allow_html=True)

    st.markdown(f"""
        <div class="note">
            {t("app_desc")}
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(t("total_slots"), total_slots)

    with col2:
        st.metric(t("available"), available_slots)

    with col3:
        st.metric(t("booked"), booked_slots)

    with col4:
        st.metric(t("hourly_capacity"), f"${total_hourly_capacity:.2f}")

    with col5:
        st.metric(t("daily_capacity"), f"${total_daily_capacity:.2f}")

    st.markdown(f'<div class="section-title" style="margin-top:40px;">✨ {t("project_features")}</div>', unsafe_allow_html=True)

    f1, f2, f3 = st.columns(3)

    with f1:
        st.markdown(f"""
            <div class="feature-card">
                <div class="feature-icon">🅿️</div>
                <div class="feature-title">{t("parking_slot_management")}</div>
                <div class="feature-text">{t("parking_slot_management_text")}</div>
            </div>
        """, unsafe_allow_html=True)

    with f2:
        st.markdown(f"""
            <div class="feature-card">
                <div class="feature-icon">📌</div>
                <div class="feature-title">{t("smart_booking")}</div>
                <div class="feature-text">{t("smart_booking_text")}</div>
            </div>
        """, unsafe_allow_html=True)

    with f3:
        st.markdown(f"""
            <div class="feature-card">
                <div class="feature-icon">💵</div>
                <div class="feature-title">{t("automatic_price")}</div>
                <div class="feature-text">{t("automatic_price_text")}</div>
            </div>
        """, unsafe_allow_html=True)

    f4, f5, f6 = st.columns(3)

    with f4:
        st.markdown(f"""
            <div class="feature-card">
                <div class="feature-icon">💳</div>
                <div class="feature-title">{t("online_payment_options")}</div>
                <div class="feature-text">{t("online_payment_options_text")}</div>
            </div>
        """, unsafe_allow_html=True)

    with f5:
        st.markdown(f"""
            <div class="feature-card">
                <div class="feature-icon">🧾</div>
                <div class="feature-title">{t("booking_receipt")}</div>
                <div class="feature-text">{t("booking_receipt_text")}</div>
            </div>
        """, unsafe_allow_html=True)

    with f6:
        st.markdown(f"""
            <div class="feature-card">
                <div class="feature-icon">🔐</div>
                <div class="feature-title">{t("admin_dashboard_feature")}</div>
                <div class="feature-text">{t("admin_dashboard_feature_text")}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown(f'<div class="section-title" style="margin-top:40px;">🚘 {t("car_types_supported")}</div>', unsafe_allow_html=True)

    cols = st.columns(3)
    for index, (car_type, image_url) in enumerate(CAR_TYPES.items()):
        with cols[index % 3]:
            st.markdown(
                f"""
                <div class="car-preview">
                    <b>{car_type}</b><br>
                    <img class="car-img" src="{image_url}">
                </div>
                """,
                unsafe_allow_html=True
            )


def slots_page():
    st.markdown(f'<div class="section-title">🅿️ {t("slots_status_prices")}</div>', unsafe_allow_html=True)

    slots_df = get_all_slots()
    cols = st.columns(5)

    for index, row in slots_df.iterrows():
        col = cols[index % 5]
        slot_number = row["slot_number"]
        status = row["status"]
        hourly_rate = float(row["hourly_rate"])
        daily_rate = float(row["daily_rate"])

        if status == "Booked":
            card_class = "booked"
            icon = "🔴"
            label = t("booked")
        elif slot_number.startswith("VIP"):
            card_class = "vip"
            icon = "⭐"
            label = t("vip_available")
        else:
            card_class = "available"
            icon = "🟢"
            label = t("available")

        col.markdown(
            f"""
            <div class="parking-card {card_class}">
                {icon}<br>
                {slot_number}<br>
                {label}<br>
                💵 ${hourly_rate:.2f} / {t("hour")}<br>
                📅 ${daily_rate:.2f} / {t("day")}
            </div>
            """,
            unsafe_allow_html=True
        )


def book_page():
    st.markdown(f'<div class="section-title">📌 {t("book_slot")}</div>', unsafe_allow_html=True)

    available_slots = get_available_slots()

    if len(available_slots) == 0:
        st.warning(t("no_available_slots"))
        return

    col1, col2 = st.columns(2)

    with col1:
        user_name = st.text_input(t("customer_name"), key="book_customer_name")

    with col2:
        phone_number = st.text_input(t("phone_number"), key="book_phone_number")

    car_number = st.text_input(t("car_plate"), key="book_car_number")

    car_type = st.selectbox(
        t("choose_car_type"),
        list(CAR_TYPES.keys()),
        key="book_car_type"
    )

    st.markdown(
        f"""
        <div class="car-preview">
            <b>{t("selected_car_type")}: {car_type}</b><br>
            <img class="car-img" src="{CAR_TYPES[car_type]}">
        </div>
        """,
        unsafe_allow_html=True
    )

    selected_slot = st.selectbox(
        t("choose_available_slot"),
        available_slots,
        key="book_selected_slot"
    )

    hourly_rate, daily_rate = get_slot_rates(selected_slot)

    col_start, col_end = st.columns(2)

    with col_start:
        start_date = st.date_input(t("start_date"), value=date.today(), key="book_start_date")

    with col_end:
        end_date = st.date_input(t("end_date"), value=date.today(), key="book_end_date")

    if end_date < start_date:
        st.error(t("end_date_error"))
        return

    days = calculate_days(start_date, end_date)

    hours = st.number_input(
        t("hours_per_day"),
        min_value=1,
        max_value=24,
        value=1,
        step=1,
        key="book_hours"
    )

    payment_labels = [t("cash"), t("credit_card"), t("online_payment")]

    payment_method_label = st.selectbox(
        t("payment_method"),
        payment_labels,
        key="book_payment_method"
    )

    payment_method = method_to_db(payment_method_label)

    online_provider = "None"
    transaction_id = "None"

    if payment_method == "Online Payment":
        st.markdown(
            f"""
            <div class="payment-box">
                {t("pay_note")}
            </div>
            """,
            unsafe_allow_html=True
        )

        col_online1, col_online2 = st.columns(2)

        with col_online1:
            online_provider = st.selectbox(
                t("online_provider"),
                ["PayPal", "Stripe", "Apple Pay", "Google Pay", "Bank Transfer"],
                key="book_online_provider"
            )

        with col_online2:
            transaction_id = st.text_input(
                t("transaction_id"),
                value=f"TXN-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                key="book_transaction_id"
            )

        payment_status_label = st.selectbox(
            t("payment_status"),
            [t("paid"), t("pending"), t("failed")],
            index=0,
            key="book_payment_status_online"
        )
    else:
        payment_status_label = st.selectbox(
            t("payment_status"),
            [t("paid"), t("pending")],
            key="book_payment_status_normal"
        )

    payment_status = status_to_db(payment_status_label)

    day_cost = min(hourly_rate * hours, daily_rate)
    total_price = calculate_total_price(hourly_rate, daily_rate, days, int(hours))

    st.markdown(
        f"""
        <div class="price-box">
            {t("slot")}: {selected_slot}<br>
            {t("car_type")}: {car_type}<br>
            {t("hourly_price")}: ${hourly_rate:.2f}<br>
            {t("daily_max")}: ${daily_rate:.2f}<br>
            {t("start_date")}: {start_date} | {t("end_date")}: {end_date}<br>
            {t("days")}: {days} | {t("hours_per_day")}: {hours}<br>
            {t("payment_method")}: {payment_method_label}<br>
            {t("payment_status")}: {payment_status_label}<br>
            {t("online_provider")}: {online_provider}<br>
            {t("transaction_id")}: {transaction_id}<br>
            {t("one_day_cost")}: ${day_cost:.2f}<br>
            {t("total_price")}: ${total_price:.2f}
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(t("book_now"), key="book_now_button"):
        missing_fields = []

        if not user_name.strip():
            missing_fields.append(t("customer_name"))

        if not phone_number.strip():
            missing_fields.append(t("phone_number"))

        if not car_number.strip():
            missing_fields.append(t("car_plate"))

        if payment_method == "Online Payment" and not transaction_id.strip():
            missing_fields.append(t("transaction_id"))

        if missing_fields:
            st.warning(t("please_fill") + " " + ", ".join(missing_fields))
            return

        invoice = book_slot(
            user_name.strip(),
            phone_number.strip(),
            car_number.strip(),
            car_type,
            selected_slot,
            start_date,
            end_date,
            days,
            int(hours),
            payment_method,
            payment_status,
            online_provider,
            transaction_id.strip()
        )

        st.session_state.last_invoice = invoice
        st.session_state.page = "receipt"
        st.success(f"{selected_slot} {t('book_success')} ${total_price:.2f}")
        st.balloons()
        st.rerun()


def receipt_page():
    st.markdown(f'<div class="section-title">🧾 {t("receipt")}</div>', unsafe_allow_html=True)

    invoice = st.session_state.get("last_invoice", None)

    if not invoice:
        st.warning(t("no_receipt"))
        return

    car_type = invoice.get("car_type", "Sedan")
    car_image = CAR_TYPES.get(car_type, CAR_TYPES["Sedan"])

    st.markdown(
        f"""
        <div class="receipt-box">
            <b>{t("customer_name")}:</b> {invoice["user_name"]}<br>
            <b>{t("phone_number")}:</b> {invoice["phone_number"]}<br>
            <b>{t("car_plate")}:</b> {invoice["car_number"]}<br>
            <b>{t("car_type")}:</b> {car_type}<br>
            <img class="car-img" src="{car_image}"><br><br>

            <b>{t("slot")}:</b> {invoice["slot_number"]}<br>
            <b>{t("start_date")}:</b> {invoice["start_date"]}<br>
            <b>{t("end_date")}:</b> {invoice["end_date"]}<br>
            <b>{t("days")}:</b> {invoice["days"]}<br>
            <b>{t("hours_per_day")}:</b> {invoice["hours"]}<br><br>

            <b>{t("hourly_price")}:</b> ${invoice["hourly_rate"]:.2f}<br>
            <b>{t("daily_max")}:</b> ${invoice["daily_rate"]:.2f}<br>
            <b>{t("total_price")}:</b> ${invoice["total_price"]:.2f}<br>
            <b>{t("payment_method")}:</b> {invoice["payment_method"]}<br>
            <b>{t("payment_status")}:</b> {invoice["payment_status"]}<br>
            <b>{t("online_provider")}:</b> {invoice["online_provider"]}<br>
            <b>{t("transaction_id")}:</b> {invoice["transaction_id"]}<br>
            <b>{t("booking_time")}:</b> {invoice["booking_time"]}<br>
        </div>
        """,
        unsafe_allow_html=True
    )

    receipt_text = create_receipt_text(invoice)

    st.download_button(
        label=t("download_receipt"),
        data=receipt_text,
        file_name=f"receipt_{invoice['slot_number']}.txt",
        mime="text/plain"
    )


def cancel_page():
    st.markdown(f'<div class="section-title">❌ {t("cancel_booking")}</div>', unsafe_allow_html=True)

    bookings_df = get_bookings()

    if bookings_df.empty:
        st.warning(t("no_bookings"))
        return

    search_text = st.text_input(t("search_cancel"))

    filtered_df = bookings_df.copy()

    if search_text.strip():
        keyword = search_text.strip().lower()
        filtered_df = filtered_df[
            filtered_df["user_name"].astype(str).str.lower().str.contains(keyword) |
            filtered_df["phone_number"].astype(str).str.lower().str.contains(keyword) |
            filtered_df["car_number"].astype(str).str.lower().str.contains(keyword) |
            filtered_df["car_type"].astype(str).str.lower().str.contains(keyword) |
            filtered_df["slot_number"].astype(str).str.lower().str.contains(keyword) |
            filtered_df["payment_method"].astype(str).str.lower().str.contains(keyword) |
            filtered_df["payment_status"].astype(str).str.lower().str.contains(keyword) |
            filtered_df["transaction_id"].astype(str).str.lower().str.contains(keyword)
        ]

    if filtered_df.empty:
        st.warning(t("no_matching"))
        return

    booked_slots = filtered_df["slot_number"].tolist()
    selected_slot = st.selectbox(t("choose_slot_cancel"), booked_slots)

    booking_info = filtered_df[filtered_df["slot_number"] == selected_slot].iloc[0]

    st.markdown(
        f"""
        <div class="price-box">
            {t("customer_name")}: {booking_info["user_name"]}<br>
            {t("phone_number")}: {booking_info["phone_number"]}<br>
            {t("car_plate")}: {booking_info["car_number"]}<br>
            {t("car_type")}: {booking_info["car_type"]}<br>
            {t("slot")}: {booking_info["slot_number"]}<br>
            {t("payment_method")}: {booking_info["payment_method"]} - {booking_info["payment_status"]}<br>
            {t("online_provider")}: {booking_info["online_provider"]}<br>
            {t("transaction_id")}: {booking_info["transaction_id"]}<br>
            {t("total_price")}: ${float(booking_info["total_price"]):.2f}
        </div>
        """,
        unsafe_allow_html=True
    )

    confirm_cancel = st.checkbox(t("confirm_cancel"))

    if st.button(t("cancel_booking"), disabled=not confirm_cancel):
        cancel_booking(selected_slot)
        st.success(t("cancel_success"))
        st.rerun()


def admin_page():
    st.markdown(f'<div class="section-title">🔐 {t("admin_dashboard")}</div>', unsafe_allow_html=True)

    admin_username = st.text_input(t("admin_username"))
    admin_password = st.text_input(t("admin_password"), type="password")

    if admin_username == ADMIN_USERNAME and admin_password == ADMIN_PASSWORD:
        st.success(t("admin_success"))

        slots_df = get_all_slots()
        bookings_df = get_bookings()

        paid_income = bookings_df[bookings_df["payment_status"] == "Paid"]["total_price"].sum() if not bookings_df.empty else 0
        online_income = bookings_df[bookings_df["payment_method"] == "Online Payment"]["total_price"].sum() if not bookings_df.empty else 0

        c1, c2, c3, c4, c5 = st.columns(5)

        with c1:
            st.metric(t("total_slots"), len(slots_df))

        with c2:
            st.metric(t("available"), len(slots_df[slots_df["status"] == "Available"]))

        with c3:
            st.metric(t("booked"), len(slots_df[slots_df["status"] == "Booked"]))

        with c4:
            st.metric(t("paid_income"), f"${paid_income:.2f}")

        with c5:
            st.metric(t("online_income"), f"${online_income:.2f}")

        st.markdown(f'<div class="section-title" style="margin-top:30px;">{t("search_bookings")}</div>', unsafe_allow_html=True)

        search_text = st.text_input(t("search_cancel"))

        filtered_bookings = bookings_df.copy()

        if search_text.strip():
            keyword = search_text.strip().lower()
            filtered_bookings = filtered_bookings[
                filtered_bookings["user_name"].astype(str).str.lower().str.contains(keyword) |
                filtered_bookings["phone_number"].astype(str).str.lower().str.contains(keyword) |
                filtered_bookings["car_number"].astype(str).str.lower().str.contains(keyword) |
                filtered_bookings["car_type"].astype(str).str.lower().str.contains(keyword) |
                filtered_bookings["slot_number"].astype(str).str.lower().str.contains(keyword) |
                filtered_bookings["payment_method"].astype(str).str.lower().str.contains(keyword) |
                filtered_bookings["payment_status"].astype(str).str.lower().str.contains(keyword) |
                filtered_bookings["online_provider"].astype(str).str.lower().str.contains(keyword) |
                filtered_bookings["transaction_id"].astype(str).str.lower().str.contains(keyword)
            ]

        st.markdown(f'<div class="section-title" style="margin-top:30px;">{t("parking_slots_table")}</div>', unsafe_allow_html=True)
        st.dataframe(slots_df, use_container_width=True, hide_index=True)

        st.download_button(
            label=t("download_slots_csv"),
            data=dataframe_to_csv_bytes(slots_df),
            file_name="parking_slots.csv",
            mime="text/csv"
        )

        st.markdown(f'<div class="section-title" style="margin-top:30px;">{t("bookings_table")}</div>', unsafe_allow_html=True)
        st.dataframe(filtered_bookings, use_container_width=True, hide_index=True)

        st.download_button(
            label=t("download_bookings_csv"),
            data=dataframe_to_csv_bytes(filtered_bookings),
            file_name="bookings.csv",
            mime="text/csv"
        )

        st.markdown(f'<div class="section-title" style="margin-top:30px;">{t("manage_slots")}</div>', unsafe_allow_html=True)

        col_add, col_update, col_delete = st.columns(3)

        with col_add:
            new_slot = st.text_input(t("new_slot"))
            new_hourly_rate = st.number_input(t("new_hourly"), min_value=0.5, max_value=100.0, value=3.0, step=0.5)
            new_daily_rate = st.number_input(t("new_daily"), min_value=1.0, max_value=500.0, value=20.0, step=1.0)

            if st.button(t("add_new_slot")):
                if new_slot.strip() == "":
                    st.warning(t("enter_slot"))
                else:
                    add_parking_slot(new_slot.upper(), float(new_hourly_rate), float(new_daily_rate))
                    st.success(t("slot_added"))
                    st.rerun()

        with col_update:
            all_slots_for_price = slots_df["slot_number"].tolist()

            if len(all_slots_for_price) > 0:
                price_slot = st.selectbox(t("choose_update_price"), all_slots_for_price)
                current_hourly_rate, current_daily_rate = get_slot_rates(price_slot)

                updated_hourly_rate = st.number_input(
                    t("updated_hourly"),
                    min_value=0.5,
                    max_value=100.0,
                    value=float(current_hourly_rate),
                    step=0.5
                )

                updated_daily_rate = st.number_input(
                    t("updated_daily"),
                    min_value=1.0,
                    max_value=500.0,
                    value=float(current_daily_rate),
                    step=1.0
                )

                if st.button(t("update_prices")):
                    update_slot_prices(price_slot, float(updated_hourly_rate), float(updated_daily_rate))
                    st.success(t("prices_updated"))
                    st.rerun()

        with col_delete:
            all_slots = slots_df["slot_number"].tolist()

            if len(all_slots) > 0:
                delete_slot = st.selectbox(t("choose_delete_slot"), all_slots)
                confirm_delete = st.checkbox(t("confirm_delete"))

                if st.button(t("delete_slot"), disabled=not confirm_delete):
                    delete_parking_slot(delete_slot)
                    st.success(t("slot_deleted"))
                    st.rerun()

        st.markdown("---")
        st.warning(t("reset_warning"))

        confirm_reset = st.checkbox(t("confirm_reset"))

        if st.button(t("reset_system"), disabled=not confirm_reset):
            reset_database()
            st.success(t("reset_success"))
            st.rerun()

    elif admin_username != "" or admin_password != "":
        st.error(t("wrong_admin"))


# ==========================================================
# Main
# ==========================================================
def go_to_page(page_name):
    st.session_state.page = page_name
    st.session_state.show_menu = False
    st.rerun()


def main():
    st.set_page_config(
        page_title="Smart Parking System",
        page_icon="🚗",
        layout="wide"
    )

    if "lang" not in st.session_state:
        st.session_state.lang = "en"

    if "page" not in st.session_state:
        st.session_state.page = "home"

    if "show_menu" not in st.session_state:
        st.session_state.show_menu = False

    create_tables()
    fix_old_database()
    insert_default_slots()
    apply_style()

    car_header()

    language_selector()

    if st.button("☰", key="menu_toggle_btn"):
        st.session_state.show_menu = not st.session_state.show_menu
        st.rerun()

    if st.session_state.show_menu:
        with st.expander("☰ Menu", expanded=True):

            if st.button(f"🏠 {t('home')}", key="menu_home"):
                go_to_page("home")

            if st.button(f"🅿️ {t('parking_slots')}", key="menu_slots"):
                go_to_page("slots")

            if st.button(f"📌 {t('book_slot')}", key="menu_book"):
                go_to_page("book")

            if st.button(f"🧾 {t('receipt')}", key="menu_receipt"):
                go_to_page("receipt")

            if st.button(f"❌ {t('cancel_booking')}", key="menu_cancel"):
                go_to_page("cancel")

            if st.button(f"🔐 {t('admin_dashboard')}", key="menu_admin"):
                go_to_page("admin")

            st.markdown(
                f"""
                <div class="side-dev">
                    <div>{t("developed_by")}</div>
                    <div>Osamah AL-murisi</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    if st.session_state.page == "home":
        home_page()

    elif st.session_state.page == "slots":
        slots_page()

    elif st.session_state.page == "book":
        book_page()

    elif st.session_state.page == "receipt":
        receipt_page()

    elif st.session_state.page == "cancel":
        cancel_page()

    elif st.session_state.page == "admin":
        admin_page()

    st.markdown(f"""
        <div class="footer">
            {t("footer")} | Developed by Osamah AL-murisi
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()