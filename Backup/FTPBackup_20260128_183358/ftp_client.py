#!/usr/bin/env python3
"""
FTP İstemcisi - lsc.hacettepe.edu.tr'ye bağlanmak için
"""

import ftplib
import os
import sys
from pathlib import Path

class FTPClient:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.ftp = None
    
    def connect(self):
        """FTP sunucusuna bağlan"""
        try:
            self.ftp = ftplib.FTP(self.host)
            self.ftp.login(self.username, self.password)
            print(f"✓ {self.host} sunucusuna başarıyla bağlandı!")
            return True
        except ftplib.all_errors as e:
            print(f"✗ Bağlantı hatası: {e}")
            return False
    
    def disconnect(self):
        """FTP bağlantısını kapat"""
        if self.ftp:
            try:
                self.ftp.quit()
                print("✓ Bağlantı kapatıldı.")
            except:
                self.ftp.close()
    
    def list_files(self, directory='.'):
        """Dosya listesini göster"""
        try:
            files = []
            self.ftp.retrlines('LIST', files.append)
            print(f"\n📁 {directory} dizini içeriği:")
            print("-" * 60)
            for file in files:
                print(file)
            return files
        except ftplib.all_errors as e:
            print(f"✗ Liste hatası: {e}")
            return []
    
    def download_file(self, remote_file, local_file=None):
        """Dosya indir"""
        if local_file is None:
            local_file = os.path.basename(remote_file)
        
        try:
            with open(local_file, 'wb') as f:
                self.ftp.retrbinary(f'RETR {remote_file}', f.write)
            print(f"✓ {remote_file} → {local_file} indirildi!")
            return True
        except ftplib.all_errors as e:
            print(f"✗ İndirme hatası: {e}")
            return False
    
    def upload_file(self, local_file, remote_file=None):
        """Dosya yükle"""
        if not os.path.exists(local_file):
            print(f"✗ Dosya bulunamadı: {local_file}")
            return False
        
        if remote_file is None:
            remote_file = os.path.basename(local_file)
        
        try:
            with open(local_file, 'rb') as f:
                self.ftp.storbinary(f'STOR {remote_file}', f)
            print(f"✓ {local_file} → {remote_file} yüklendi!")
            return True
        except ftplib.all_errors as e:
            print(f"✗ Yükleme hatası: {e}")
            return False
    
    def change_directory(self, directory):
        """Dizin değiştir"""
        try:
            self.ftp.cwd(directory)
            print(f"✓ Dizin değiştirildi: {directory}")
            return True
        except ftplib.all_errors as e:
            print(f"✗ Dizin değiştirme hatası: {e}")
            return False
    
    def get_current_directory(self):
        """Mevcut dizini göster"""
        try:
            pwd = self.ftp.pwd()
            print(f"📂 Mevcut dizin: {pwd}")
            return pwd
        except ftplib.all_errors as e:
            print(f"✗ Hata: {e}")
            return None
    
    def create_directory(self, directory):
        """Dizin oluştur"""
        try:
            self.ftp.mkd(directory)
            print(f"✓ Dizin oluşturuldu: {directory}")
            return True
        except ftplib.all_errors as e:
            print(f"✗ Dizin oluşturma hatası: {e}")
            return False
    
    def delete_file(self, filename):
        """Dosya sil"""
        try:
            self.ftp.delete(filename)
            print(f"✓ Dosya silindi: {filename}")
            return True
        except ftplib.all_errors as e:
            print(f"✗ Silme hatası: {e}")
            return False
    
    def _is_directory(self, name):
        """Bir öğenin dizin olup olmadığını kontrol et"""
        try:
            current = self.ftp.pwd()
            try:
                self.ftp.cwd(name)
                self.ftp.cwd(current)
                return True
            except:
                return False
        except:
            return False
    
    def download_all(self, remote_dir='.', local_dir='LSCFile'):
        """Tüm dosya ve klasörleri recursive olarak indir"""
        import os
        
        # Yerel klasörü oluştur
        os.makedirs(local_dir, exist_ok=True)
        
        try:
            # Mevcut dizini kaydet
            original_dir = self.ftp.pwd()
            
            # Uzak dizine geç
            if remote_dir != '.':
                self.ftp.cwd(remote_dir)
            
            # Dosya listesini al (NLST kullanarak)
            try:
                names = self.ftp.nlst()
            except:
                # NLST desteklenmiyorsa LIST kullan
                items = []
                self.ftp.retrlines('LIST', items.append)
                names = []
                for item in items:
                    parts = item.split()
                    if len(parts) >= 9:
                        # Dosya adı genellikle son kısımda
                        name = ' '.join(parts[8:])
                        if name not in ['.', '..']:
                            names.append(name)
            
            downloaded_count = 0
            
            for name in names:
                # Özel dizinleri atla
                if name in ['.', '..']:
                    continue
                
                local_path = os.path.join(local_dir, name)
                
                # Dizin mi kontrol et
                if self._is_directory(name):
                    # Dizin ise recursive indir
                    print(f"📁 Dizin indiriliyor: {name}")
                    try:
                        self.ftp.cwd(name)
                        sub_count = self.download_all('.', local_path)
                        downloaded_count += sub_count
                        self.ftp.cwd('..')  # Üst dizine dön
                    except Exception as e:
                        print(f"  ✗ {name} dizin hatası: {e}")
                else:
                    # Dosya ise indir
                    print(f"📄 Dosya indiriliyor: {name}")
                    try:
                        with open(local_path, 'wb') as f:
                            self.ftp.retrbinary(f'RETR {name}', f.write)
                        downloaded_count += 1
                        print(f"  ✓ {name} indirildi")
                    except Exception as e:
                        print(f"  ✗ {name} indirme hatası: {e}")
            
            # Orijinal dizine dön
            if remote_dir != '.':
                self.ftp.cwd(original_dir)
            
            return downloaded_count
            
        except ftplib.all_errors as e:
            print(f"✗ İndirme hatası: {e}")
            return 0


def main():
    # FTP bağlantı bilgileri
    HOST = "lsc.hacettepe.edu.tr"
    USERNAME = "yasamdestegimerkeziw"
    PASSWORD = 'T6"~wKT/'
    
    # FTP istemcisi oluştur
    client = FTPClient(HOST, USERNAME, PASSWORD)
    
    # Bağlan
    if not client.connect():
        sys.exit(1)
    
    try:
        # Örnek kullanımlar
        print("\n" + "="*60)
        print("FTP İstemcisi - Komutlar:")
        print("="*60)
        
        # Mevcut dizini göster
        client.get_current_directory()
        
        # Dosya listesini göster
        client.list_files()
        
        # İnteraktif mod için örnek
        print("\n" + "="*60)
        print("Kullanım örnekleri:")
        print("="*60)
        print("# Dosya listesi:")
        print("client.list_files()")
        print("\n# Dosya indir:")
        print("client.download_file('uzak_dosya.txt', 'yerel_dosya.txt')")
        print("\n# Dosya yükle:")
        print("client.upload_file('yerel_dosya.txt', 'uzak_dosya.txt')")
        print("\n# Dizin değiştir:")
        print("client.change_directory('dizin_adi')")
        print("\n# Dizin oluştur:")
        print("client.create_directory('yeni_dizin')")
        
    finally:
        # Bağlantıyı kapat
        client.disconnect()


if __name__ == "__main__":
    main()
