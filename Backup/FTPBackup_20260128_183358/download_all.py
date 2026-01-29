#!/usr/bin/env python3
"""
Tüm FTP dosyalarını LSCFile klasörüne indir
"""

import sys
from ftp_client import FTPClient

def main():
    # FTP bağlantı bilgileri
    HOST = "lsc.hacettepe.edu.tr"
    USERNAME = "yasamdestegimerkeziw"
    PASSWORD = 'T6"~wKT/'
    
    # FTP istemcisi oluştur
    client = FTPClient(HOST, USERNAME, PASSWORD)
    
    # Bağlan
    print("FTP sunucusuna bağlanılıyor...")
    if not client.connect():
        sys.exit(1)
    
    try:
        # Mevcut dizini göster
        client.get_current_directory()
        
        print("\n" + "="*60)
        print("Tüm dosyalar LSCFile klasörüne indiriliyor...")
        print("="*60 + "\n")
        
        # Tüm dosyaları indir
        count = client.download_all('.', 'LSCFile')
        
        print("\n" + "="*60)
        print(f"İndirme tamamlandı! Toplam {count} öğe indirildi.")
        print("="*60)
        
    except KeyboardInterrupt:
        print("\n\nİndirme iptal edildi.")
    except Exception as e:
        print(f"\n✗ Hata: {e}")
    finally:
        # Bağlantıyı kapat
        client.disconnect()


if __name__ == "__main__":
    main()
