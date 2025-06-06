# Backend FastAPI App

Proyek ini adalah backend berbasis **FastAPI** yang terletak di dalam folder `Backend/`. File utama yang dijalankan adalah `main.py`.

## 📁 Struktur Folder

project-root/
├── Backend/
│ ├── main.py
│ ├── requirements.txt
│ └── ...


## ⚙️ Persiapan & Menjalankan Server FastAPI

Ikuti panduan di bawah ini melalui **terminal VS Code**:

---

# Upgrade Pip
python -m pip install --upgrade pip setuptools wheel

# Install dependencies
pip install -r requirements.txt

# Jalankan FastAPI server
cd Backend
python -m  uvicorn main:app --reload

```
### Jika ingin dijalankan di device lain:
``` bash
# Jalankan FastAPI di semua alamat IP (0.0.0.0)
python -m  uvicorn main:app --host 0.0.0.0 --reload