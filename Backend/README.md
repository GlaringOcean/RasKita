# Backend FastAPI App

This project is a FastAPI-based backend located in the `Backend/` folder. The main file to run is `main.py`.

## 📁 Folder Structure
```
project-root/
├── Backend/
│ ├── main.py
│ ├── requirements.txt
│ └── ...
├── ...
```
---
## ⚙️ Setup & Run the FastAPI Server
Follow the instructions below in your **VS Code terminal**:
---
### Upgrade Pip, Setuptools  and Wheel
```
python -m pip install --upgrade pip setuptools wheel
```
### Install dependencies
```
pip install -r requirements.txt
```
### Run the FastAPI server
```
cd Backend
python -m uvicorn main:app --reload
```
---

## 🌐 If you want to run the server on another device:
```
python -m uvicorn main:app --host 0.0.0.0 --reload
```
