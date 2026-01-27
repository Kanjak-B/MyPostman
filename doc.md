# Lancer l'application

## Installer les dépendances

```
"C:/CODING MOOD/PYTHON PROJECTS/MyPostman/MyPostman/.venv/Scripts/python.exe" -m pip install -r requirements.txt
```

## Démarrer le backend (API)

```
"C:/CODING MOOD/PYTHON PROJECTS/MyPostman/MyPostman/.venv/Scripts/python.exe" -m uvicorn app.backend.main:app --reload
```

## Démarrer l'interface (UI)

```
"C:/CODING MOOD/PYTHON PROJECTS/MyPostman/MyPostman/.venv/Scripts/python.exe" -m app.frontend.main
```
