# А.Аварзэд Хүргэлт — Дуудах систем

## Хэрхэн ажилладаг
- Үйлчлүүлэгч `yoursite.com` → "Дуудах" дарна
- Таны утсанд (owner.html) шууд дуу+мэдэгдэл ирнэ
- Та "Боломжтой" эсвэл "Боломжгүй" дарна

## Render.com дээр деплой хийх (үнэгүй)

1. https://github.com → New repository → "hurgelt" нэртэй үүсгэ
2. Эдгээр файлуудыг upload хий:
   - server.py
   - requirements.txt
   - Procfile
   - static/index.html
   - static/owner.html

3. https://render.com → Sign up (GitHub-аар нэвтэр)
4. New → Web Service → GitHub repo сонго
5. Settings:
   - Name: avarzed-hurgelt
   - Runtime: Python 3
   - Build command: pip install -r requirements.txt
   - Start command: gunicorn server:app --worker-class=gthread --threads=4 --timeout=120
6. Deploy → URL авна (жишээ: avarzed-hurgelt.onrender.com)

## Хэрэглэх
- Үйлчлүүлэгчдэд: `https://avarzed-hurgelt.onrender.com`
- Өөрийн самбар: `https://avarzed-hurgelt.onrender.com/owner`
  (энэ хуудсыг утсандаа нээж байгаарай)
