from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Email Draft Assistant API")

# السماح للفرونت اند (React) يكلم الـ API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # لاحقاً نحددها بدومين الفرونت بالظبط
    allow_methods=["*"],
    allow_headers=["*"],
)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """
أنت مساعد كتابة إيميلات احترافية لموظفي مبيعات ودعم فني.
مهمتك: تاخد نقاط مبعثرة من الموظف وتحولها لإيميل رسمي جاهز للإرسال.

قواعد صارمة:
1. اكتب الإيميل بنفس اللغة اللي كاتب بيها المستخدم النقاط
2. حافظ على نبرة احترافية تناسب نوع الإيميل
3. لازم يكون فيه: تحية مناسبة + جسم الإيميل منظم + خاتمة مناسبة
4. متضفش معلومات مش موجودة في النقاط اللي المستخدم كتبها
5. الإيميل يكون مختصر ومباشر، من غير حشو زيادة
6. لو النقاط ناقصة معلومة أساسية، استخدم placeholder زي [اسم العميل]

أنواع الإيميلات وأسلوب كل واحد:
- quote: واضح، فيه تفاصيل السعر والشروط، نبرة واثقة
- follow-up: ودود بس فيه urgency خفيف
- apology: متواضع وصادق، فيه حل للمشكلة
- complaint_response: متفهم ومطمّن، بيعترف بالمشكلة ويقدم حل واضح
"""

class EmailRequest(BaseModel):
    email_type: str  # quote / follow-up / apology / complaint_response
    points: str

class EmailResponse(BaseModel):
    email: str

@app.post("/generate-email", response_model=EmailResponse)
def generate_email(req: EmailRequest):
    if not req.points.strip():
        raise HTTPException(status_code=400, detail="النقاط فاضية")

    prompt = f"""{SYSTEM_PROMPT}

نوع الإيميل: {req.email_type}
النقاط اللي كتبها الموظف:
{req.points}

اكتب الإيميل كامل دلوقتي (subject + body).
"""
    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )
        return EmailResponse(email=response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def health_check():
    return {"status": "running"}