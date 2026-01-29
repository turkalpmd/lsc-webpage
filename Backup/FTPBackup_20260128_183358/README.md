# FTP Git - Git Benzeri FTP Yönetim Sistemi

Bu sistem, Git'e benzer şekilde dosya değişikliklerini takip eder ve sadece değişen dosyaları FTP sunucusuna push eder.

## Özellikler

- ✅ **Git Hook Desteği**: Git commit sonrası otomatik FTP push (GitHub Actions gibi lokal)
- ✅ **Değişiklik Takibi**: Dosyaların hash değerlerini takip eder, sadece değişen dosyaları push eder
- ✅ **LSCFile Desteği**: LSCFile klasöründeki değişiklikleri otomatik takip eder
- ✅ **Commit Sistemi**: Git gibi commit oluşturma ve geçmiş tutma
- ✅ **Akıllı Push**: Güncellemesi olmayan dosyaları push etmez
- ✅ **Status Gösterimi**: Hangi dosyaların değiştiğini gösterir
- ✅ **Otomatik Dizin Oluşturma**: FTP'de gerekli dizinleri otomatik oluşturur
- ✅ **Git Diff Entegrasyonu**: Git'in kendi diff mekanizmasını kullanır

## Kurulum

Python 3.6+ gereklidir. `ftplib` Python'un standart kütüphanesinde bulunur.

### Git Hook Kurulumu (Önerilen) ⭐

Git commit edildiğinde otomatik olarak değişen dosyaları FTP'ye push etmek için:

```bash
cd FTPServer
python setup_git_hook.py
```

Bu komut Git `post-commit` hook'unu kurar. Artık her `git commit` sonrası:
- ✅ Sadece değişen dosyalar otomatik olarak FTP'ye push edilir
- ✅ LSCFile klasöründeki değişiklikler de takip edilir
- ✅ Manuel push yapmanıza gerek kalmaz

Hook'u kaldırmak için:
```bash
python setup_git_hook.py remove
```

## Kullanım

### 1. Status - Değişiklik Durumunu Kontrol Et

```bash
cd FTPServer
python ftp_git.py status
```

Bu komut şunları gösterir:
- Yeni dosyalar (+)
- Değiştirilmiş dosyalar (~)
- Silinmiş dosyalar (-)
- Değişmemiş dosyalar

### 2. Add - Dosyaları Staging Area'ya Ekle

```bash
# Tüm değişiklikleri ekle
python ftp_git.py add

# Belirli bir dosyayı ekle
python ftp_git.py add dosya.txt
```

### 3. Commit - Değişiklikleri Commit Et

```bash
# Varsayılan mesaj ile commit
python ftp_git.py commit

# Özel mesaj ile commit
python ftp_git.py commit "Yeni özellik eklendi"
```

### 4. Push - Commit'leri FTP'ye Push Et

```bash
python push.py
```

veya

```bash
python ftp_git.py push
```

`push.py` otomatik olarak:
- Değişiklikleri kontrol eder
- Varsa otomatik commit yapar
- Tüm commit'leri FTP'ye push eder
- Sadece değişen dosyaları yükler

### 5. Log - Commit Geçmişini Göster

```bash
python ftp_git.py log
```

### 6. Reset - Index'i Temizle

```bash
python ftp_git.py reset
```

### 7. Check - Push Durumunu Kontrol Et ⭐

Commit'lerin FTP'ye gidip gitmediğini kontrol eder:

```bash
python check_push.py
```

Bu komut şunları gösterir:
- ✅ Push edilmiş commit'ler
- ⏳ Push edilmemiş commit'ler
- 📝 Her commit'teki değişen dosyalar
- 🔍 FTP'deki dosya durumu

## Örnek Kullanım Senaryoları

### Senaryo 1: Git Hook ile Otomatik Push (Önerilen) ⭐

```bash
# 1. Git hook'unu kur (sadece bir kez)
cd FTPServer
python setup_git_hook.py

# 2. Normal Git workflow'unu kullan
git add .
git commit -m "Yeni özellik eklendi"

# 3. Otomatik olarak sadece değişen dosyalar FTP'ye push edilir! 🎉
# Manuel push yapmanıza gerek yok!
```

### Senaryo 2: Manuel Push

```bash
# 1. Dosyalarda değişiklik yap
# ... dosyaları düzenle ...

# 2. Durumu kontrol et
python ftp_git.py status

# 3. Değişiklikleri ekle
python ftp_git.py add

# 4. Commit oluştur
python ftp_git.py commit "Bug fix: CSS düzeltmesi"

# 5. FTP'ye push et
python push.py
```

### Senaryo 3: Git + FTP Git Hibrit Kullanım

```bash
# 1. Git hook'unu kur
python setup_git_hook.py

# 2. Normal Git kullan
git add LSCFile/index.html
git commit -m "Ana sayfa güncellendi"

# 3. Otomatik push! Sadece index.html FTP'ye yüklenir
```

## Nasıl Çalışır?

1. **Değişiklik Takibi**: Her dosyanın MD5 hash değeri hesaplanır ve `.ftpgit/index.json` dosyasında saklanır.

2. **Commit Sistemi**: Her commit, değişiklik yapılan dosyaların listesini ve hash değerlerini içerir. Commit'ler `.ftpgit/commits.json` dosyasında saklanır.

3. **Akıllı Push**: 
   - Sadece commit edilmiş değişiklikler push edilir
   - Aynı dosya birden fazla commit'te olsa bile sadece bir kez yüklenir
   - Push edilen commit'ler `.ftpgit/pushed_commits.json` dosyasında takip edilir
   - Güncellemesi olmayan dosyalar push edilmez

4. **Dizin Yapısı**: FTP'de gerekli alt dizinler otomatik olarak oluşturulur.

## Dosya Yapısı

```
FTPServer/
├── ftp_client.py         # FTP bağlantı sınıfı
├── ftp_git.py            # Git benzeri yönetim sistemi
├── push.py               # Otomatik push scripti
├── git_ftp_hook.py       # Git post-commit hook scripti ⭐
├── setup_git_hook.py     # Git hook kurulum scripti ⭐
├── check_push.py          # Push durumu kontrol scripti ⭐
├── download_all.py        # Tüm dosyaları indir
├── ftp_interactive.py     # İnteraktif FTP istemcisi
└── .ftpgit/              # Git benzeri metadata (otomatik oluşturulur)
    ├── index.json          # Dosya hash'leri
    ├── commits.json        # Commit geçmişi
    └── pushed_commits.json # Push edilen commit'ler
```

## Nasıl Çalışır?

### Git Hook Mekanizması

1. **Git Commit**: Normal `git commit` yaparsınız
2. **Hook Tetiklenir**: Git otomatik olarak `post-commit` hook'unu çalıştırır
3. **Değişiklik Tespiti**: `git diff` ile sadece değişen dosyalar bulunur
4. **FTP Push**: Sadece değişen dosyalar FTP'ye push edilir
5. **LSCFile Desteği**: LSCFile klasöründeki değişiklikler de otomatik takip edilir

### Avantajlar

- ✅ **Git'in kendi mekanizmasını kullanır**: Daha güvenilir ve hızlı
- ✅ **Otomatik**: Manuel push yapmanıza gerek yok
- ✅ **Sadece değişen dosyalar**: Zaman ve bant genişliği tasarrufu
- ✅ **LSCFile desteği**: LSCFile klasöründeki değişiklikler de takip edilir

## Notlar

- `.ftpgit` klasörü Git'teki `.git` klasörü gibi çalışır
- Git hook kurulduktan sonra her commit otomatik olarak FTP'ye push edilir
- Sadece değişen dosyalar push edilir, bu sayede zaman ve bant genişliği tasarrufu sağlanır
- LSCFile klasöründeki dosyalar da Git ile takip edilirse otomatik push edilir
- Hook'u devre dışı bırakmak için: `python setup_git_hook.py remove`
