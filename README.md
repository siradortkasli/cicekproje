<div align="center">

# 🌸 ÇiçekSepeti Benzeri E-Ticaret ve Sipariş Yönetim Sistemi

**Python · Django · Microsoft SQL Server · HTML · CSS · JavaScript**

Müşteri alışveriş deneyimini, firma operasyonlarını ve yönetici onay süreçlerini bir araya getiren, üniversite projesi kapsamında geliştirilmiş web uygulaması.

</div>

---

## 📌 Proje Hakkında

Bu proje, çiçek ve hediye ürünlerinin çevrim içi listelenmesi, sepete eklenmesi, sipariş oluşturulması ve sipariş durumunun takip edilmesi amacıyla geliştirilmiştir. Uygulama; **müşteri**, **firma** ve **yönetici** rollerini destekleyen bir iş akışı içerir.

Geliştirme sürecinde Django tabanlı web mimarisi, ilişkisel veri modelleri, SQL Server bağlantısı, arayüz geliştirme ve rol bazlı yönetim süreçleri üzerine çalıştım.



## ✨ Özellikler

### 👤 Müşteri tarafı
- Kullanıcı kaydı, giriş ve çıkış işlemleri
- Kategoriye göre ürün listeleme ve ürün detay sayfası
- Ürün yorumları ve değerlendirmeleri
- Alışveriş sepetine ürün ekleme, çıkarma ve miktar güncelleme
- Sipariş oluşturma, sipariş geçmişi ve sipariş durumunu takip etme
- Firma tarafından yüklenen ürün hazırlık görselini **onaylama veya reddetme**
- Siparişe mesaj kartı ekleme

### 🏪 Firma tarafı
- Firma kaydı, girişi ve kontrol paneli
- Ürün ekleme, düzenleme ve listeleme
- Firma siparişlerini görüntüleme ve sipariş durumlarını güncelleme
- Sipariş hazırlık görseli yükleme
- Sipariş iptal süreçleri

### 🛡️ Yönetim ve veri katmanı
- Django yönetici paneli
- Firma ve ürün onay alanları
- Django ORM ile ilişkisel veri modelleri
- Microsoft SQL Server bağlantısı ve SQL sorgu dosyaları
- Kategori, ürün, sepet ve sipariş işlemlerine yönelik JSON API uç noktaları

## 🧰 Kullanılan Teknolojiler

| Katman | Teknolojiler |
|---|---|
| Backend | Python, Django |
| Frontend | HTML, CSS, JavaScript |
| Veri tabanı | Microsoft SQL Server, Django ORM |
| Veri tabanı çalışmaları | SQL sorguları; Stored Procedure, Trigger, Function ve View örnekleri |
| API | Django ile JSON tabanlı uç noktalar |
| Geliştirme | Git, GitHub |

## 🗂️ Proje Yapısı

```text
cicekproje/
├── accounts/       # Kullanıcı hesapları ve oturum işlemleri
├── company/        # Firma yönetimi
├── store/          # Ürün, sepet, sipariş ve API işlemleri
├── config/         # Django ayarları ve URL yapılandırması
├── static/         # Statik dosyalar
├── manage.py
└── SQLQuery*.sql   # SQL çalışmaları
```

## 🖥️ Ekran Görüntüleri

Projenin ana sayfa, ürün detay, sepet, firma paneli ve sipariş takip ekranlarının görüntüleri bu bölüme eklenecektir.

<!-- Örnek: ![Ana Sayfa](docs/screenshots/ana-sayfa.png) -->

## ⚙️ Yerel Kurulum

Bu depo eğitim amaçlı geliştirilmiştir. Çalıştırmak için Python, Django ile uyumlu bağımlılıklar ve Microsoft SQL Server yapılandırması gereklidir.

1. Depoyu klonlayın:
   ```bash
   git clone https://github.com/siradortkasli/cicekproje.git
   cd cicekproje
   ```
2. Bir sanal ortam oluşturup etkinleştirin:
   ```bash
   python -m venv .venv
   ```
   Windows PowerShell için: `.venv\Scripts\Activate.ps1`
3. Projeyle uyumlu Python paketlerini yükleyin. **Depoda doğrulanmış bir `requirements.txt` bulunmadığından kesin sürüm ve tam bağımlılık listesi henüz belgelenmemiştir.**
4. SQL Server veritabanınızı hazırlayın ve `config/settings.py` dosyasındaki veritabanı bağlantısını kendi ortamınıza göre, gizli bilgileri kodda açık bırakmayacak şekilde yapılandırın.
5. Veritabanı ve bağımlılıklar hazır olduğunda:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

> Kurulum adımları tam otomatik ve yeniden üretilebilir hale getirilene kadar ek ortam yapılandırması gerekebilir.

