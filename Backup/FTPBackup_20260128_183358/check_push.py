#!/usr/bin/env python3
"""
FTP Push Durumu Kontrolü
Commit'lerin FTP'ye gidip gitmediğini kontrol eder
"""

import os
import sys
import subprocess
import json
from datetime import datetime
from ftp_client import FTPClient

def get_git_commits():
    """Git commit geçmişini al"""
    try:
        result = subprocess.run(
            ['git', 'log', '--oneline', '--all'],
            capture_output=True,
            text=True,
            check=True
        )
        commits = []
        for line in result.stdout.strip().split('\n'):
            if line:
                parts = line.split(' ', 1)
                if len(parts) == 2:
                    commits.append({
                        'id': parts[0],
                        'message': parts[1]
                    })
        return commits
    except:
        return []

def get_pushed_commits():
    """Push edilmiş commit'leri al"""
    git_root = subprocess.run(
        ['git', 'rev-parse', '--show-toplevel'],
        capture_output=True,
        text=True,
        check=True
    ).stdout.strip()
    
    pushed_file = os.path.join(git_root, '.ftpgit', 'pushed_commits.json')
    if os.path.exists(pushed_file):
        with open(pushed_file, 'r') as f:
            return json.load(f)
    return []

def get_changed_files_in_commit(commit_id):
    """Bir commit'teki değişen dosyaları al"""
    try:
        # Commit'teki değişen dosyaları al
        result = subprocess.run(
            ['git', 'show', '--name-only', '--pretty=format:', commit_id],
            capture_output=True,
            text=True,
            check=True
        )
        
        files = [f.strip() for f in result.stdout.split('\n') if f.strip()]
        
        # Eğer boşsa, diff ile dene
        if not files:
            try:
                result = subprocess.run(
                    ['git', 'diff', '--name-only', f'{commit_id}~1', commit_id],
                    capture_output=True,
                    text=True,
                    check=True
                )
                files = [f.strip() for f in result.stdout.split('\n') if f.strip()]
            except:
                pass
        
        return files
    except:
        return []

def check_ftp_file_exists(ftp_client, filepath):
    """FTP'de dosyanın var olup olmadığını kontrol et"""
    try:
        # Sadece LSCFile klasöründeki dosyaları kontrol et
        if not filepath.startswith('LSCFile/'):
            return None  # Kontrol edilmemeli
        
        remote_path = filepath.replace('\\', '/')
        # LSCFile/ prefix'ini kaldır - FTP root'unda kontrol et
        if remote_path.startswith('LSCFile/'):
            remote_path = remote_path[9:]  # 'LSCFile/' uzunluğu 9
        
        remote_dir_path = os.path.dirname(remote_path)
        filename = os.path.basename(remote_path)
        
        # Root dizine dön
        try:
            ftp_client.ftp.cwd('.')
        except:
            pass
        
        # Dizin yapısına git
        if remote_dir_path and remote_dir_path != '.':
            dirs = [d for d in remote_dir_path.split('/') if d]
            for d in dirs:
                try:
                    ftp_client.ftp.cwd(d)
                except:
                    return False
        
        # Dosya listesini al
        files = []
        ftp_client.ftp.retrlines('LIST', files.append)
        
        # Dosyayı ara (dosya adı tam eşleşme veya içeriyor mu kontrol et)
        for f in files:
            # LIST çıktısından dosya adını çıkar
            parts = f.split()
            if len(parts) >= 9:
                file_name = ' '.join(parts[8:])
                if filename == file_name or filename in file_name:
                    return True
        
        return False
    except Exception as e:
        return False

def main():
    # FTP bağlantı bilgileri
    HOST = "lsc.hacettepe.edu.tr"
    USERNAME = "yasamdestegimerkeziw"
    PASSWORD = 'T6"~wKT/'
    
    print("="*60)
    print("📊 FTP Push Durumu Kontrolü")
    print("="*60)
    
    # Git repo kontrolü
    try:
        git_root = subprocess.run(
            ['git', 'rev-parse', '--show-toplevel'],
            capture_output=True,
            text=True,
            check=True
        ).stdout.strip()
    except:
        print("✗ Bu bir Git repository değil.")
        sys.exit(1)
    
    # Commit'leri al
    commits = get_git_commits()
    pushed_commits = get_pushed_commits()
    
    if not commits:
        print("\n⚠️  Henüz commit yok.")
        sys.exit(0)
    
    print(f"\n📜 Toplam {len(commits)} commit bulundu")
    print(f"📤 {len(pushed_commits)} commit push edilmiş")
    
    # FTP'ye bağlan
    print("\n🔌 FTP sunucusuna bağlanılıyor...")
    ftp_client = FTPClient(HOST, USERNAME, PASSWORD)
    
    if not ftp_client.connect():
        print("✗ FTP bağlantısı başarısız!")
        sys.exit(1)
    
    try:
        print("\n" + "="*60)
        print("📋 Commit Durumları")
        print("="*60)
        
        # Son 10 commit'i kontrol et
        recent_commits = commits[:10]
        
        for commit in recent_commits:
            commit_id_short = commit['id'][:8]
            is_pushed = commit_id_short in pushed_commits or commit['id'] in pushed_commits
            
            if is_pushed:
                status = "✅ PUSHED"
            else:
                status = "⏳ PENDING"
            
            print(f"\n[{status}] {commit_id_short}")
            print(f"  Mesaj: {commit['message']}")
            
            if not is_pushed:
                # Değişen dosyaları göster (sadece LSCFile ve önemli dosyalar)
                changed_files = get_changed_files_in_commit(commit['id'])
                # Sadece LSCFile klasöründeki dosyaları göster
                lscfile_files = [f for f in changed_files if f.startswith('LSCFile/')]
                if lscfile_files:
                    print(f"  📝 {len(lscfile_files)} LSCFile dosyası değişmiş (push edilmemiş)")
                    if len(lscfile_files) <= 5:
                        for f in lscfile_files:
                            print(f"     - {f}")
                    else:
                        for f in lscfile_files[:5]:
                            print(f"     - {f}")
                        print(f"     ... ve {len(lscfile_files) - 5} dosya daha")
                elif changed_files:
                    print(f"  📝 {len(changed_files)} dosya değişmiş (push edilmemiş - LSCFile dışı)")
        
        # Push edilmemiş commit'leri göster
        unpushed = [c for c in commits if c['id'][:8] not in pushed_commits and c['id'] not in pushed_commits]
        
        if unpushed:
            print("\n" + "="*60)
            print(f"⚠️  {len(unpushed)} commit push edilmemiş!")
            print("="*60)
            print("\nPush etmek için:")
            print("  cd FTPServer")
            print("  python push.py")
        else:
            print("\n" + "="*60)
            print("✅ Tüm commit'ler push edilmiş!")
            print("="*60)
        
        # FTP'deki dosyaları kontrol et (sadece LSCFile)
        print("\n" + "="*60)
        print("🔍 FTP'deki Dosya Kontrolü (Son 3 commit - Sadece LSCFile)")
        print("="*60)
        
        for commit in commits[:3]:
            changed_files = get_changed_files_in_commit(commit['id'])
            # Sadece LSCFile klasöründeki dosyaları filtrele
            lscfile_files = [f for f in changed_files if f.startswith('LSCFile/')]
            
            if lscfile_files:
                print(f"\n📦 Commit: {commit['id'][:8]} - {commit['message'][:50]}...")
                checked = 0
                found = 0
                
                for filepath in lscfile_files[:10]:  # İlk 10 LSCFile dosyasını kontrol et
                    exists = check_ftp_file_exists(ftp_client, filepath)
                    if exists is not None:  # None ise kontrol edilmemeli
                        checked += 1
                        if exists:
                            found += 1
                            print(f"  ✅ {filepath}")
                        else:
                            print(f"  ❌ {filepath} (FTP'de bulunamadı)")
                
                if checked > 0:
                    print(f"  📊 {found}/{checked} dosya FTP'de mevcut")
            else:
                print(f"\n📦 Commit: {commit['id'][:8]} - {commit['message'][:50]}...")
                print(f"  ℹ️  Bu commit'te LSCFile dosyası yok (FTPServer dosyaları push edilmez)")
    
    finally:
        ftp_client.disconnect()
    
    print("\n" + "="*60)
    print("✓ Kontrol tamamlandı!")
    print("="*60)

if __name__ == "__main__":
    main()
