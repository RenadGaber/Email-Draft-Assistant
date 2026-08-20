# Email Draft Assistant — Gemini Version (Local Setup)

## الفرق عن نسخة Anthropic
- بنستخدم مكتبة `google-generativeai` بدل `anthropic`
- الموديل: `gemini-3.6-flash` (سريع ومتوازن من ناحية السعر)
- الـ `frontend.html` **متغيرش خالص** — لأنه بيكلم السيرفر بتاعك (`localhost:5000`) مش بيكلم Google مباشرة

## هتجيب الـ API key منين؟
1. روح لـ **aistudio.google.com/apikey**
2. سجّل دخول بحساب Google عادي
3. دوس **"Create API key"**
4. انسخ الـ key (بيبدأ بحروف عادية مش `sk-`)

Google بتديك حد استخدام مجاني يوميًا كويس لمشروع تدريبي زي ده.

## خطوات التشغيل

### 1. ثبّت المكتبات
```
pip install -r requirements.txt
```

### 2. حط الـ API key
افتح `app.py` ولاقي:
```python
genai.configure(api_key=os.environ.get("GEMINI_API_KEY", "YOUR_API_KEY_HERE"))
```
استبدل `YOUR_API_KEY_HERE` بالـ key بتاعك.

### 3. شغّل السيرفر
```
python app.py
```
هيشتغل على `http://127.0.0.1:5000` — سيب الـ Terminal مفتوح.

### 4. افتح الواجهة
دبل كليك على `frontend.html`.

## لو ظهر خطأ استيراد (`ModuleNotFoundError`)
اتأكد إن `pip install -r requirements.txt` خلص من غير أخطاء. لو لسه فيه مشكلة، جرب:
```
pip install google-generativeai --upgrade
```
