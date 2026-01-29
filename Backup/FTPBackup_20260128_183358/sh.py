#!/usr/bin/env python3
"""
FTP Push - Tüm commit'leri FTP'ye push et
"""

import sys
from ftp_git import FTPGit
from ftp_client import FTPClient

def main():
    # FTP bağlantı bilgileri
    HOST = "lsc.hacettepe.edu.tr"
    USERNAME = "yasamdestegimerkeziw"
    PASSWORD = 'T6"~wKT/'
    
    print("FTP sunucusuna bağlanılıyor...")
    ftp_client = FTPClient(HOST, USERNAME, PASSWORD)
    
    if not ftp_client.connect():
        print("✗ FTP bağlantısı başarısız!")
        sys.exit(1)
    
    try:
        # FTPGit oluştur
        git = FTPGit('.', ftp_client)
        
        # Status göster
        print("\n" + "="*60)
        print("📊 Mevcut Durum")
        print("="*60)
        status = git.status()
        
        # Eğer değişiklik varsa commit et
        if len(status['new']) > 0 or len(status['modified']) > 0 or len(status['deleted']) > 0:
            print("\n" + "="*60)
            print("💾 Değişiklikler commit ediliyor...")
            print("="*60)
            git.commit("Auto-commit before push")
        
        # Push et
        print("\n" + "="*60)
        print("📤 FTP'ye push ediliyor...")
        print("="*60)
        git.push()
        
        # Log göster
        print("\n" + "="*60)
        git.log()
        
    except KeyboardInterrupt:
        print("\n\nİşlem iptal edildi.")
    except Exception as e:
        print(f"\n✗ Hata: {e}")
        import traceback
        traceback.print_exc()
    finally:
        ftp_client.disconnect()


if __name__ == "__main__":
    main()
