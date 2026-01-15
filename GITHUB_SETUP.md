# GitHub Setup Guide

Panduan lengkap untuk push SubCandalena ke GitHub.

## 📋 Prasyarat

1. **Git terinstall**
   ```powershell
   git --version
   ```
   Jika belum ada, download dari: https://git-scm.com/download/win

2. **GitHub Account**
   - Buat akun di https://github.com jika belum punya
   - Verify email Anda

3. **SSH Key (Optional tapi Recommended)**
   ```powershell
   # Generate SSH key
   ssh-keygen -t ed25519 -C "your_email@example.com"
   
   # Copy public key
   cat ~/.ssh/id_ed25519.pub
   
   # Tambahkan ke GitHub: Settings > SSH and GPG keys > New SSH key
   ```

## 🚀 Langkah-Langkah Push ke GitHub

### Step 1: Buat Repository Baru di GitHub

1. Login ke GitHub
2. Klik tombol **"+"** di kanan atas → **"New repository"**
3. Isi form:
   - **Repository name**: `SubCandalena` atau `SubHunterX-Pro`
   - **Description**: `🎯 Enterprise Subdomain Reconnaissance & Intelligence Suite`
   - **Visibility**: Public atau Private (pilih sesuai kebutuhan)
   - **JANGAN centang**: "Initialize this repository with a README"
4. Klik **"Create repository"**

### Step 2: Inisialisasi Git di Projek Lokal

Buka PowerShell/Terminal di folder projek Anda, lalu jalankan:

```powershell
# Navigasi ke folder projek
cd "C:\Users\DELL\OneDrive\ドキュメント\ALL in ONE\TOOLS\SubCandalena"

# Inisialisasi git repository
git init

# Tambahkan semua file ke staging
git add .

# Buat commit pertama
git commit -m "Initial commit: SubCandalena v3.0 - Enterprise Subdomain Reconnaissance Suite"
```

### Step 3: Hubungkan dengan GitHub Repository

```powershell
# Ganti 'yourusername' dengan username GitHub Anda
git remote add origin https://github.com/yourusername/SubCandalena.git

# Atau jika pakai SSH:
git remote add origin git@github.com:yourusername/SubCandalena.git

# Verify remote
git remote -v
```

### Step 4: Push ke GitHub

```powershell
# Push ke branch main
git branch -M main
git push -u origin main
```

### Step 5: Verify Upload

1. Buka https://github.com/yourusername/SubCandalena
2. Pastikan semua file sudah terupload
3. Check README.md tampil dengan baik

## 🔧 Update README dengan Link GitHub Aktual

Setelah repository dibuat, update link di README.md:

1. Cari dan ganti `yourusername` dengan username GitHub Anda
2. Commit dan push perubahan:

```powershell
git add README.md
git commit -m "Update: Replace placeholder links with actual GitHub repository"
git push
```

## 📝 Workflow Selanjutnya

### Membuat Perubahan

```powershell
# Edit file-file yang diperlukan
# Lalu:

# Check status
git status

# Tambahkan file yang diubah
git add .

# Commit dengan pesan yang jelas
git commit -m "Add: Fitur baru X"

# Push ke GitHub
git push
```

### Membuat Branch untuk Fitur Baru

```powershell
# Buat branch baru
git checkout -b feature/nama-fitur

# Lakukan perubahan
# ...

# Commit
git add .
git commit -m "Add: Deskripsi fitur"

# Push branch
git push -u origin feature/nama-fitur

# Buat Pull Request di GitHub
```

## 🎨 Mempercantik Repository

### 1. Tambahkan Topics

Di GitHub repository → Settings → Topics, tambahkan:
- `subdomain-enumeration`
- `reconnaissance`
- `pentesting`
- `bug-bounty`
- `security-tools`
- `python`
- `asyncio`
- `cybersecurity`

### 2. Tambahkan Description

Edit description di GitHub untuk SEO yang lebih baik.

### 3. Pin Repository

Pin repository di profile Anda untuk showcase.

### 4. Enable GitHub Pages (Optional)

Untuk hosting documentation:
- Settings → Pages
- Source: Deploy from branch `main`
- Folder: `/docs` atau root

### 5. Buat GitHub Actions (Optional)

Untuk CI/CD automation - sudah disediakan dalam file `.github/workflows/`

## 🔐 Keamanan

### Jangan Push File Sensitif

Pastikan `.gitignore` sudah benar:
```
*.db
config/secrets.yaml
config/api_keys.yaml
.env
```

### Check Sebelum Push

```powershell
# Check apa yang akan di-push
git status

# Check diff
git diff

# Check file yang akan di-commit
git diff --staged
```

### Hapus File Sensitif dari History (Jika Ter-push)

```powershell
# Hapus file dari history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch config/secrets.yaml" \
  --prune-empty --tag-name-filter cat -- --all

# Force push (HATI-HATI!)
git push origin --force --all
```

## 🌟 Tips & Best Practices

### Commit Message Guidelines

```
Type: Brief description

Types:
- Add: Menambah fitur baru
- Fix: Memperbaiki bug
- Update: Update fitur existing
- Docs: Update dokumentasi
- Refactor: Refactoring code
- Test: Menambah test
- Style: Formatting code

Contoh:
- Add: Integration with AlienVault OTX API
- Fix: Screenshot capture timeout issue
- Update: Improve brute force performance
- Docs: Add tutorial for API integration
```

### Branching Strategy

```
main (production-ready)
├── develop (development)
│   ├── feature/new-passive-source
│   ├── feature/dashboard-improvements
│   └── fix/dns-timeout-bug
└── hotfix/critical-bug-fix
```

### Frequent Commits

Commit sering dengan pesan yang jelas, jangan tunggu terlalu banyak perubahan.

## 🐛 Troubleshooting

### Error: "remote origin already exists"

```powershell
git remote remove origin
git remote add origin https://github.com/yourusername/SubCandalena.git
```

### Error: "Permission denied (publickey)"

Setup SSH key dengan benar atau gunakan HTTPS.

### Error: "Large files"

Jika ada file besar (>100MB):
```powershell
# Install Git LFS
git lfs install

# Track large files
git lfs track "*.db"
git add .gitattributes
```

### File Tidak Ke-push

Cek `.gitignore`, mungkin file tersebut di-exclude.

## 📞 Need Help?

- GitHub Docs: https://docs.github.com
- Git Documentation: https://git-scm.com/doc
- Stack Overflow: https://stackoverflow.com/questions/tagged/git

---

Good luck! 🚀
