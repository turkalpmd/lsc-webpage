#!/usr/bin/env python3
"""
İnteraktif FTP İstemcisi - Komut satırından kullanım
"""

import ftplib
import os
import sys
from ftp_client import FTPClient

def print_help():
    """Yardım mesajını göster"""
    print("""
╔══════════════════════════════════════════════════════════╗
║           FTP İstemcisi - Komutlar                       ║
╚══════════════════════════════════════════════════════════╝

Komutlar:
  ls, list              - Dosya listesini göster
  pwd                   - Mevcut dizini göster
  cd <dizin>            - Dizin değiştir
  mkdir <dizin>         - Dizin oluştur
  download <dosya>      - Dosya indir
  upload <dosya>        - Dosya yükle
  delete <dosya>        - Dosya sil
  help                  - Bu yardım mesajını göster
  quit, exit            - Çıkış

Örnekler:
  ls
  cd public_html
  download index.html
  upload test.txt
  mkdir yeni_dizin
""")

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
    
    # Mevcut dizini göster
    client.get_current_directory()
    
    print("\nİnteraktif mod aktif. 'help' yazarak komutları görebilirsiniz.\n")
    
    try:
        while True:
            try:
                command = input("ftp> ").strip()
                
                if not command:
                    continue
                
                parts = command.split()
                cmd = parts[0].lower()
                
                if cmd in ['quit', 'exit', 'q']:
                    break
                
                elif cmd in ['help', 'h', '?']:
                    print_help()
                
                elif cmd in ['ls', 'list', 'dir']:
                    if len(parts) > 1:
                        client.list_files(parts[1])
                    else:
                        client.list_files()
                
                elif cmd == 'pwd':
                    client.get_current_directory()
                
                elif cmd == 'cd':
                    if len(parts) > 1:
                        client.change_directory(parts[1])
                    else:
                        print("Kullanım: cd <dizin>")
                
                elif cmd == 'mkdir':
                    if len(parts) > 1:
                        client.create_directory(parts[1])
                    else:
                        print("Kullanım: mkdir <dizin>")
                
                elif cmd == 'download' or cmd == 'get':
                    if len(parts) > 1:
                        remote_file = parts[1]
                        local_file = parts[2] if len(parts) > 2 else None
                        client.download_file(remote_file, local_file)
                    else:
                        print("Kullanım: download <uzak_dosya> [yerel_dosya]")
                
                elif cmd == 'upload' or cmd == 'put':
                    if len(parts) > 1:
                        local_file = parts[1]
                        remote_file = parts[2] if len(parts) > 2 else None
                        client.upload_file(local_file, remote_file)
                    else:
                        print("Kullanım: upload <yerel_dosya> [uzak_dosya]")
                
                elif cmd == 'delete' or cmd == 'rm':
                    if len(parts) > 1:
                        client.delete_file(parts[1])
                    else:
                        print("Kullanım: delete <dosya>")
                
                else:
                    print(f"Bilinmeyen komut: {cmd}. 'help' yazarak komutları görebilirsiniz.")
            
            except KeyboardInterrupt:
                print("\n\nÇıkılıyor...")
                break
            except EOFError:
                print("\n\nÇıkılıyor...")
                break
            except Exception as e:
                print(f"Hata: {e}")
    
    finally:
        # Bağlantıyı kapat
        client.disconnect()
        print("Güle güle!")


if __name__ == "__main__":
    main()
