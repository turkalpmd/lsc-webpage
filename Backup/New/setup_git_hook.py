#!/usr/bin/env python3
"""
Git Hook Kurulum Scripti
Git post-commit hook'unu otomatik olarak kurar
"""

import os
import sys
import subprocess
from pathlib import Path

def setup_git_hook():
    """Git post-commit hook'unu kur"""
    
    # Git repo kontrolü
    try:
        git_dir = subprocess.run(
            ['git', 'rev-parse', '--git-dir'],
            capture_output=True,
            text=True,
            check=True
        ).stdout.strip()
    except:
        print("✗ Bu bir Git repository değil. Önce 'git init' yapın.")
        sys.exit(1)
    
    hooks_dir = os.path.join(git_dir, 'hooks')
    post_commit_hook = os.path.join(hooks_dir, 'post-commit')
    
    # Hooks dizinini oluştur
    os.makedirs(hooks_dir, exist_ok=True)
    
    # Mevcut script'in yolunu bul
    script_dir = os.path.dirname(os.path.abspath(__file__))
    git_ftp_hook = os.path.join(script_dir, 'git_ftp_hook.py')
    
    if not os.path.exists(git_ftp_hook):
        print(f"✗ git_ftp_hook.py bulunamadı: {git_ftp_hook}")
        sys.exit(1)
    
    # Hook script'ini oluştur
    hook_content = f"""#!/bin/bash
# Git post-commit hook - Otomatik FTP push
# Bu dosya otomatik olarak oluşturulmuştur

cd "{script_dir}/.."
python3 "{git_ftp_hook}"
"""
    
    # Hook dosyasını yaz
    with open(post_commit_hook, 'w') as f:
        f.write(hook_content)
    
    # Çalıştırılabilir yap
    os.chmod(post_commit_hook, 0o755)
    
    print("✓ Git post-commit hook başarıyla kuruldu!")
    print(f"  Hook konumu: {post_commit_hook}")
    print("\nArtık her 'git commit' sonrası değişen dosyalar otomatik olarak FTP'ye push edilecek.")
    print("\nNot: Hook'u devre dışı bırakmak için:")
    print(f"  rm {post_commit_hook}")

def remove_git_hook():
    """Git post-commit hook'unu kaldır"""
    try:
        git_dir = subprocess.run(
            ['git', 'rev-parse', '--git-dir'],
            capture_output=True,
            text=True,
            check=True
        ).stdout.strip()
    except:
        print("✗ Bu bir Git repository değil.")
        sys.exit(1)
    
    post_commit_hook = os.path.join(git_dir, 'hooks', 'post-commit')
    
    if os.path.exists(post_commit_hook):
        os.remove(post_commit_hook)
        print("✓ Git post-commit hook kaldırıldı.")
    else:
        print("⚠️  Hook zaten kurulu değil.")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'remove':
        remove_git_hook()
    else:
        setup_git_hook()

if __name__ == "__main__":
    main()
