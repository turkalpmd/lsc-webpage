# LSC FTP Yönetim Sistemi

Bu proje, `lsc.hacettepe.edu.tr` FTP sunucusuna bağlanmak ve Git benzeri bir sistemle dosya yönetimi yapmak için Python tabanlı bir sistem içerir.

## 📁 Proje Yapısı

```
LSC/
├── FTPServer/          # FTP yönetim araçları
│   ├── ftp_client.py      # FTP bağlantı sınıfı
│   ├── ftp_git.py         # Git benzeri yönetim sistemi ⭐
│   ├── push.py            # Otomatik push scripti ⭐
│   ├── download_all.py    # Tüm dosyaları indir
│   ├── ftp_interactive.py # İnteraktif FTP istemcisi
│   └── README.md           # Detaylı dokümantasyon
└── LSCFile/            # İndirilen dosyalar (otomatik oluşturulur)
```

## 🚀 Hızlı Başlangıç

### Git Hook ile Otomatik FTP Push ⭐ (Önerilen)

En önemli özellik: **Git commit edildiğinde otomatik FTP push!**

```bash
cd FTPServer

# 1. Git hook'unu kur (sadece bir kez)
python setup_git_hook.py

# 2. Normal Git kullan
git add .
git commit -m "Yeni özellik eklendi"

# 3. Otomatik olarak sadece değişen dosyalar FTP'ye push edilir! 🎉
```

### Manuel Push Sistemi

```bash
cd FTPServer

# 1. Değişiklik durumunu kontrol et
python ftp_git.py status

# 2. Değişiklikleri commit et
python ftp_git.py commit "Yeni özellik eklendi"

# 3. FTP'ye push et (sadece değişen dosyalar!)
python push.py
```

**Git Hook Avantajları:**
- ✅ Git commit sonrası otomatik push (GitHub Actions gibi lokal)
- ✅ Sadece değişen dosyalar push edilir
- ✅ LSCFile klasöründeki değişiklikler de takip edilir
- ✅ Manuel push yapmanıza gerek yok

## 📖 Detaylı Kullanım

Detaylı kullanım kılavuzu için `FTPServer/README.md` dosyasına bakın.

### Temel Komutlar

```bash
cd FTPServer

# Status - Değişiklik durumunu göster
python ftp_git.py status

# Add - Dosyaları staging area'ya ekle
python ftp_git.py add

# Commit - Değişiklikleri commit et
python ftp_git.py commit "Mesaj"

# Push - Commit'leri FTP'ye push et
python push.py

# Log - Commit geçmişini göster
python ftp_git.py log

# Check - Push durumunu kontrol et
python check_push.py
```

## ✨ Özellikler

### Git Benzeri Sistem
- ✅ **Git Hook Desteği**: Git commit sonrası otomatik FTP push (GitHub Actions gibi lokal) ⭐
- ✅ **LSCFile Desteği**: LSCFile klasöründeki değişiklikleri otomatik takip eder
- ✅ **Değişiklik Takibi**: Git diff ile sadece değişen dosyaları bulur
- ✅ **Akıllı Push**: Sadece değişen dosyaları push eder
- ✅ **Commit Sistemi**: Git gibi commit oluşturma ve geçmiş tutma
- ✅ **Status Gösterimi**: Hangi dosyaların değiştiğini gösterir

### FTP İşlemleri
- ✅ FTP sunucusuna bağlanma
- ✅ Dosya listesi görüntüleme
- ✅ Dosya indirme/yükleme
- ✅ Dizin işlemleri
- ✅ Tüm dosyaları recursive indirme

## 🔧 Kurulum

Python 3.6+ gereklidir. `ftplib` Python'un standart kütüphanesinde bulunur, ek paket kurulumu gerekmez.

## 📝 Örnek Kullanım Senaryosu

```bash
cd FTPServer

# 1. Dosyalarda değişiklik yap
# ... dosyaları düzenle ...

# 2. Durumu kontrol et
python ftp_git.py status

# 3. Değişiklikleri commit et
python ftp_git.py commit "Bug fix: CSS düzeltmesi"

# 4. FTP'ye push et (sadece değişen dosyalar push edilir!)
python push.py
```

## 📚 Daha Fazla Bilgi

Detaylı dokümantasyon için `FTPServer/README.md` dosyasına bakın.

## ⚠️ Notlar

- Şifre ve kullanıcı adı bilgileri kod içinde saklanmaktadır. Üretim ortamında bu bilgileri environment variable veya config dosyasından okumanız önerilir.
- `.ftpgit` klasörü Git'teki `.git` klasörü gibi çalışır ve otomatik oluşturulur.
- Sadece değişen dosyalar push edilir, bu sayede zaman ve bant genişliği tasarrufu sağlanır.



For all pushing:

cd FTPServer 
python upload_all_from_lscfile.py --only-changed