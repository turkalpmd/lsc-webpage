#!/usr/bin/env python3
"""
Git benzeri FTP yönetim sistemi
Değişiklik takibi, commit ve push işlemleri
"""

import os
import json
import hashlib
import sys
from datetime import datetime
from pathlib import Path
from ftp_client import FTPClient

class FTPGit:
    def __init__(self, root_dir='.', ftp_client=None):
        self.root_dir = os.path.abspath(root_dir)
        self.git_dir = os.path.join(self.root_dir, '.ftpgit')
        self.index_file = os.path.join(self.git_dir, 'index.json')
        self.commits_file = os.path.join(self.git_dir, 'commits.json')
        self.ftp_client = ftp_client
        
        # .ftpgit klasörünü oluştur
        os.makedirs(self.git_dir, exist_ok=True)
        
        # Dosyaları yükle
        self.index = self._load_json(self.index_file, {})
        self.commits = self._load_json(self.commits_file, [])
    
    def _load_json(self, filepath, default):
        """JSON dosyasını yükle"""
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return default
        return default
    
    def _save_json(self, filepath, data):
        """JSON dosyasına kaydet"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _get_file_hash(self, filepath):
        """Dosyanın hash değerini hesapla"""
        try:
            with open(filepath, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return None
    
    def _get_all_files(self, directory='.', ignore_dirs=None):
        """Tüm dosyaları recursive olarak bul"""
        if ignore_dirs is None:
            ignore_dirs = ['.ftpgit', '.git', '__pycache__', 'node_modules', '.DS_Store']
        
        files = []
        directory = os.path.abspath(directory)
        
        for root, dirs, filenames in os.walk(directory):
            # İgnore edilecek dizinleri filtrele
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            
            for filename in filenames:
                if filename in ignore_dirs:
                    continue
                
                filepath = os.path.join(root, filename)
                rel_path = os.path.relpath(filepath, self.root_dir)
                files.append(rel_path)
        
        return files
    
    def status(self):
        """Değişiklik durumunu göster (git status gibi)"""
        print("\n" + "="*60)
        print("📊 FTP Git Status")
        print("="*60)
        
        all_files = self._get_all_files(self.root_dir)
        
        modified = []
        new = []
        unchanged = []
        
        for filepath in all_files:
            full_path = os.path.join(self.root_dir, filepath)
            
            if not os.path.exists(full_path):
                continue
            
            current_hash = self._get_file_hash(full_path)
            stored_hash = self.index.get(filepath, {}).get('hash')
            
            if stored_hash is None:
                new.append(filepath)
            elif current_hash != stored_hash:
                modified.append(filepath)
            else:
                unchanged.append(filepath)
        
        # Son commit'te olmayan dosyalar
        deleted = []
        for filepath in self.index.keys():
            full_path = os.path.join(self.root_dir, filepath)
            if not os.path.exists(full_path):
                deleted.append(filepath)
        
        print(f"\n📝 Yeni dosyalar ({len(new)}):")
        for f in new:
            print(f"  + {f}")
        
        print(f"\n✏️  Değiştirilmiş dosyalar ({len(modified)}):")
        for f in modified:
            print(f"  ~ {f}")
        
        print(f"\n🗑️  Silinmiş dosyalar ({len(deleted)}):")
        for f in deleted:
            print(f"  - {f}")
        
        print(f"\n✓ Değişmemiş dosyalar: {len(unchanged)}")
        
        if len(new) == 0 and len(modified) == 0 and len(deleted) == 0:
            print("\n✓ Çalışma dizini temiz, commit edilecek bir şey yok.")
        
        return {
            'new': new,
            'modified': modified,
            'deleted': deleted,
            'unchanged': len(unchanged)
        }
    
    def add(self, filepath=None):
        """Dosyaları staging area'ya ekle (git add gibi)"""
        if filepath:
            # Tek dosya ekle
            full_path = os.path.join(self.root_dir, filepath)
            if not os.path.exists(full_path):
                print(f"✗ Dosya bulunamadı: {filepath}")
                return False
            
            file_hash = self._get_file_hash(full_path)
            if file_hash:
                self.index[filepath] = {
                    'hash': file_hash,
                    'size': os.path.getsize(full_path),
                    'modified': datetime.now().isoformat()
                }
                print(f"✓ Eklendi: {filepath}")
                return True
        else:
            # Tüm değişiklikleri ekle
            status = self.status()
            added = 0
            
            for f in status['new'] + status['modified']:
                full_path = os.path.join(self.root_dir, f)
                file_hash = self._get_file_hash(full_path)
                if file_hash:
                    self.index[f] = {
                        'hash': file_hash,
                        'size': os.path.getsize(full_path),
                        'modified': datetime.now().isoformat()
                    }
                    added += 1
            
            # Silinmiş dosyaları index'ten çıkar
            for f in status['deleted']:
                if f in self.index:
                    del self.index[f]
                    added += 1
            
            self._save_json(self.index_file, self.index)
            print(f"\n✓ {added} dosya staging area'ya eklendi.")
            return True
    
    def commit(self, message="Update files"):
        """Değişiklikleri commit et (git commit gibi)"""
        status = self.status()
        
        if len(status['new']) == 0 and len(status['modified']) == 0 and len(status['deleted']) == 0:
            print("✗ Commit edilecek değişiklik yok. Önce 'add' yapın.")
            return False
        
        # Önce add yap
        self.add()
        
        # Commit oluştur
        commit = {
            'id': hashlib.md5(f"{datetime.now()}{message}".encode()).hexdigest()[:8],
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'files': {
                'new': status['new'],
                'modified': status['modified'],
                'deleted': status['deleted']
            },
            'index': self.index.copy()
        }
        
        self.commits.append(commit)
        self._save_json(self.commits_file, self.commits)
        
        print(f"\n✓ Commit oluşturuldu: {commit['id']}")
        print(f"  Mesaj: {message}")
        print(f"  Yeni: {len(status['new'])}, Değiştirilmiş: {len(status['modified'])}, Silinmiş: {len(status['deleted'])}")
        
        return commit['id']
    
    def push(self, remote_dir='.'):
        """Commit'leri FTP'ye push et (git push gibi)"""
        if not self.ftp_client:
            print("✗ FTP client bağlantısı yok!")
            return False
        
        if not self.ftp_client.ftp:
            print("✗ FTP sunucusuna bağlı değil!")
            return False
        
        # Push edilmemiş commit'leri bul
        pushed_commits = self._load_json(
            os.path.join(self.git_dir, 'pushed_commits.json'),
            []
        )
        
        unpushed = [c for c in self.commits if c['id'] not in pushed_commits]
        
        if len(unpushed) == 0:
            print("✓ Push edilecek commit yok. Her şey güncel!")
            return True
        
        print(f"\n📤 {len(unpushed)} commit push ediliyor...")
        print("="*60)
        
        pushed_count = 0
        uploaded_files = set()
        
        for commit in unpushed:
            print(f"\n📦 Commit: {commit['id']} - {commit['message']}")
            
            # Yeni ve değiştirilmiş dosyaları yükle
            for filepath in commit['files']['new'] + commit['files']['modified']:
                if filepath in uploaded_files:
                    continue
                
                local_path = os.path.join(self.root_dir, filepath)
                if not os.path.exists(local_path):
                    continue
                
                # LSCFile/ prefix'ini kaldır - FTP root'una yükle
                remote_path = filepath.replace('\\', '/')  # Windows path desteği
                if remote_path.startswith('LSCFile/'):
                    remote_path = remote_path[9:]  # 'LSCFile/' uzunluğu 9
                remote_dir_path = os.path.dirname(remote_path)
                
                # Dosyayı yükle
                try:
                    # Önce root dizine dön - mutlaka root'a git
                    try:
                        # Root'a dönmek için birkaç kez üst dizine çık
                        for _ in range(10):  # Maksimum 10 seviye yukarı
                            try:
                                self.ftp_client.ftp.cwd('..')
                            except:
                                break
                    except:
                        pass
                    
                    # Dizin yapısını oluştur
                    if remote_dir_path and remote_dir_path != '.':
                        dirs = [d for d in remote_dir_path.split('/') if d]
                        for d in dirs:
                            try:
                                # Dizine geçmeyi dene
                                self.ftp_client.ftp.cwd(d)
                            except:
                                # Dizin yoksa oluştur
                                try:
                                    self.ftp_client.ftp.mkd(d)
                                    self.ftp_client.ftp.cwd(d)
                                except Exception as e:
                                    # Dizin zaten var olabilir, tekrar dene
                                    try:
                                        self.ftp_client.ftp.cwd(d)
                                    except:
                                        raise Exception(f"Dizin oluşturulamadı: {d} - {e}")
                    
                    # Dosyayı yükle
                    with open(local_path, 'rb') as f:
                        filename = os.path.basename(remote_path)
                        # Debug: FTP'ye hangi yola yüklendiğini göster
                        current_dir = self.ftp_client.ftp.pwd()
                        print(f"  📤 FTP'ye yükleniyor: {current_dir}/{filename} (orijinal: {filepath})")
                        self.ftp_client.ftp.storbinary(f'STOR {filename}', f)
                    
                    uploaded_files.add(filepath)
                    print(f"  ✓ Yüklendi: {filepath} → FTP: {current_dir}/{filename}")
                except Exception as e:
                    print(f"  ✗ Hata ({filepath}): {e}")
            
            # Silinmiş dosyaları FTP'den sil
            for filepath in commit['files']['deleted']:
                remote_path = filepath.replace('\\', '/')
                # LSCFile/ prefix'ini kaldır
                if remote_path.startswith('LSCFile/'):
                    remote_path = remote_path[9:]  # 'LSCFile/' uzunluğu 9
                try:
                    # Root dizine dön
                    self.ftp_client.ftp.cwd(remote_dir)
                    
                    # Dizin yapısına git
                    remote_dir_path = os.path.dirname(remote_path)
                    if remote_dir_path and remote_dir_path != '.':
                        dirs = [d for d in remote_dir_path.split('/') if d]
                        for d in dirs:
                            self.ftp_client.ftp.cwd(d)
                    
                    filename = os.path.basename(remote_path)
                    self.ftp_client.ftp.delete(filename)
                    print(f"  ✓ Silindi: {filepath}")
                except Exception as e:
                    print(f"  ✗ Silme hatası ({filepath}): {e}")
            
            pushed_commits.append(commit['id'])
            pushed_count += 1
        
        # Push edilen commit'leri kaydet
        self._save_json(
            os.path.join(self.git_dir, 'pushed_commits.json'),
            pushed_commits
        )
        
        print(f"\n✓ {pushed_count} commit başarıyla push edildi!")
        return True
    
    def log(self):
        """Commit geçmişini göster (git log gibi)"""
        print("\n" + "="*60)
        print("📜 Commit Geçmişi")
        print("="*60)
        
        if len(self.commits) == 0:
            print("\nHenüz commit yok.")
            return
        
        pushed_commits = self._load_json(
            os.path.join(self.git_dir, 'pushed_commits.json'),
            []
        )
        
        for commit in reversed(self.commits):
            status = "✓ PUSHED" if commit['id'] in pushed_commits else "⏳ PENDING"
            date = datetime.fromisoformat(commit['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
            
            print(f"\n[{status}] {commit['id']}")
            print(f"  Mesaj: {commit['message']}")
            print(f"  Tarih: {date}")
            print(f"  Dosyalar: +{len(commit['files']['new'])}, ~{len(commit['files']['modified'])}, -{len(commit['files']['deleted'])}")
    
    def reset(self):
        """Index'i temizle (git reset gibi)"""
        self.index = {}
        self._save_json(self.index_file, self.index)
        print("✓ Index temizlendi.")


def main():
    """Ana fonksiyon - komut satırı arayüzü"""
    if len(sys.argv) < 2:
        print("""
FTP Git - Git benzeri FTP yönetim sistemi

Kullanım:
  python ftp_git.py <komut> [argümanlar]

Komutlar:
  status              - Değişiklik durumunu göster
  add [dosya]         - Dosyaları staging area'ya ekle
  commit [mesaj]      - Değişiklikleri commit et
  push                - Commit'leri FTP'ye push et
  log                 - Commit geçmişini göster
  reset               - Index'i temizle

Örnekler:
  python ftp_git.py status
  python ftp_git.py add
  python ftp_git.py commit "Yeni özellik eklendi"
  python ftp_git.py push
  python ftp_git.py log
        """)
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    # FTP bağlantı bilgileri
    HOST = "lsc.hacettepe.edu.tr"
    USERNAME = "yasamdestegimerkeziw"
    PASSWORD = 'T6"~wKT/'
    
    # FTP client oluştur (push için gerekli)
    ftp_client = None
    if command == 'push':
        ftp_client = FTPClient(HOST, USERNAME, PASSWORD)
        if not ftp_client.connect():
            print("✗ FTP bağlantısı başarısız!")
            sys.exit(1)
    
    # FTPGit oluştur
    git = FTPGit('.', ftp_client)
    
    try:
        if command == 'status':
            git.status()
        
        elif command == 'add':
            if len(sys.argv) > 2:
                git.add(sys.argv[2])
            else:
                git.add()
        
        elif command == 'commit':
            message = sys.argv[2] if len(sys.argv) > 2 else "Update files"
            git.commit(message)
        
        elif command == 'push':
            git.push()
        
        elif command == 'log':
            git.log()
        
        elif command == 'reset':
            git.reset()
        
        else:
            print(f"✗ Bilinmeyen komut: {command}")
            sys.exit(1)
    
    finally:
        if ftp_client:
            ftp_client.disconnect()


if __name__ == "__main__":
    main()
