# Nöroloji Klinik Asistan Botu

Servis vizit notlarını ve acil konsültasyonları sesli dikte ile
yapılandırılmış metne dönüştüren Telegram botu.

## Nasıl çalışır?

1. `/start` → menüden **Servis Vizit Notu** veya **Acil Konsültasyon** seçin
2. Hasta adı / oda numarası yazın
3. Muayeneyi/öyküyü sesli mesaj olarak gönderin
4. Bot: ses → yazı (Whisper) → yapılandırılmış klinik not (GPT) → size gönderir ve kaydeder
5. `/bugun` : bugünkü tüm notların listesi
6. `/not <id>` : belirli bir notun tam metnini gösterir
7. `/export` : bugünkü notları `.docx` olarak indirir
8. `/ara` (veya menüden **Hasta Ara**) : hasta adına göre geçmiş notlarda arama

---

## 1) Gerekli Hesaplar / Anahtarlar

### a) Telegram Bot Token
1. Telegram'da **@BotFather**'a yazın
2. `/newbot` komutunu gönderin, bir isim ve kullanıcı adı verin
3. Size verilen token'ı not edin (örn: `123456789:AAxxxxxx...`)

### b) Kendi Telegram Kullanıcı ID'niz (güvenlik için)
1. Telegram'da **@userinfobot**'a yazın
2. Size verdiği ID'yi not edin (bot yalnızca bu ID'ye cevap verecek)

### c) OpenAI API Key (klinik not yapılandırma için — GPT)
1. https://platform.openai.com/api-keys adresine gidin
2. Yeni bir API key oluşturun
3. Hesaba en az birkaç dolarlık kredi yükleyin (GPT-4o-mini oldukça ucuzdur;
   ortalama bir not birkaç kuruş tutar)

### d) Groq API Key (ses -> yazı transkripsiyonu için)
1. https://console.groq.com adresine gidin, hesap oluşturun
2. **API Keys** sekmesinden yeni bir anahtar oluşturun
3. Groq'un Whisper transkripsiyonu OpenAI'ya göre çok daha ucuz ve hızlıdır
   (large-v3 modeli için ~$0.111/saat); ücretsiz kotayla başlayabilirsiniz

---

## 2) Railway'e Deploy

### Adım 1 — Kodu GitHub'a yükleyin
Bu klasördeki tüm dosyaları yeni bir GitHub reposuna push edin.
(İsterseniz Railway'in "Deploy from local folder" seçeneğini de kullanabilirsiniz.)

### Adım 2 — Railway'de proje oluşturun
1. https://railway.app adresine gidin, GitHub hesabınızla giriş yapın
2. **New Project → Deploy from GitHub repo** seçin, reponuzu seçin
3. Railway otomatik olarak `requirements.txt` ve `Procfile`'ı algılayıp
   bir **worker** servisi olarak deploy edecektir

### Adım 3 — Ortam değişkenlerini girin
Railway proje ayarlarında **Variables** sekmesine gidip şunları ekleyin:

| Değişken | Değer |
|---|---|
| `TELEGRAM_BOT_TOKEN` | BotFather'dan aldığınız token |
| `OPENAI_API_KEY` | OpenAI API anahtarınız (not yapılandırma - GPT) |
| `GROQ_API_KEY` | Groq API anahtarınız (transkripsiyon - Whisper) |
| `ALLOWED_USER_ID` | Telegram kullanıcı ID'niz |

### Adım 4 — Deploy
Değişkenleri kaydettiğinizde Railway otomatik olarak yeniden deploy eder.
Loglardan `"Bot başlatılıyor (polling)..."` mesajını gördüyseniz bot çalışıyordur.

> Not: Bot **polling** modunda çalışır (webhook gerektirmez), bu yüzden
> Railway'de herhangi bir public URL/domain ayarlamanıza gerek yoktur.
> Sadece servisin sürekli (worker olarak) açık kalması yeterlidir.

### Kalıcı depolama hakkında not
Notlar `notes.db` adlı SQLite dosyasında saklanır. Railway'in ücretsiz
planında dosya sistemi her deploy'da sıfırlanabilir. Notların kalıcı
olmasını istiyorsanız Railway'de bir **Volume** ekleyip `db.py` içindeki
`DB_PATH` değerini o volume'ün yoluna göre güncelleyin (örn. `/data/notes.db`).
İsterseniz bu adımı da sizin için yapabilirim.

---

## 3) Yerelde Test Etme (opsiyonel)

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env       # .env dosyasını kendi bilgilerinizle doldurun
python bot.py
```

---

## 4) Sonraki Adımlar (isteğe bağlı geliştirmeler)

- **Notion/Google Docs entegrasyonu**: Notlar otomatik olarak dışarıya
  senkronize edilsin isterseniz kolayca eklenebilir.
- **Hasta listesinden seçim**: Oda numarası yazmak yerine önceden
  tanımlı bir hasta listesinden inline buton ile seçim yapılabilir.
- **Çoklu kullanıcı desteği**: Birden fazla asistan hekim aynı botu
  kullanacaksa, her notun kime ait olduğunu ayırt eden bir yapı eklenebilir.
- **Kalıcı volume**: Railway'de veri kaybını önlemek için volume kurulumu.

Bunlardan herhangi birini eklememi isterseniz haber verin.
