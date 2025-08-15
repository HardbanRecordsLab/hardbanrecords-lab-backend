# prometheus_app/main.py
import httpx
import os
import asyncio
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, Dict, Any
import json
from datetime import datetime

app = FastAPI(
    title="Prometheus AI Service",
    description="AI-powered content generation for HardbanRecords Lab",
    version="1.0.0"
)

# --- PYDANTIC SCHEMAS ---

class LyricsRequest(BaseModel):
    genre: str
    theme: str
    language: str = "polish"
    mood: Optional[str] = "energetic"
    length: Optional[str] = "standard"  # short, standard, long

class LyricsResponse(BaseModel):
    lyrics: str
    generated_by: str
    genre: str
    theme: str
    generation_time: str
    word_count: int

class DescriptionRequest(BaseModel):
    title: str
    artist: str
    genre: str
    mood: Optional[str] = None
    target_audience: Optional[str] = "general"

class DescriptionResponse(BaseModel):
    short_description: str
    marketing_copy: str
    social_media_caption: str
    hashtags: list[str]
    generated_by: str

class AnalyzeRequest(BaseModel):
    text: str
    analysis_type: str = "sentiment"  # sentiment, genre, themes

class AnalysisResponse(BaseModel):
    analysis_type: str
    results: Dict[str, Any]
    confidence: float
    suggestions: list[str]

# --- GROQ AI CLIENT ---

class GroqClient:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.base_url = "https://api.groq.com/openai/v1"
        
        if not self.api_key:
            print("WARNING: GROQ_API_KEY not found. AI features will not work.")
    
    async def generate_completion(self, messages: list, temperature: float = 0.7, max_tokens: int = 1000):
        """
        Generuje odpowiedź z Groq API używając modelu Llama 3.
        """
        if not self.api_key:
            raise HTTPException(status_code=500, detail="AI service not configured")
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "llama3-8b-8192",  # Szybki model Llama 3
                        "messages": messages,
                        "temperature": temperature,
                        "max_tokens": max_tokens,
                        "top_p": 1,
                        "stream": False
                    }
                )
                
                if response.status_code != 200:
                    error_detail = f"Groq API error: {response.status_code}"
                    try:
                        error_json = response.json()
                        error_detail += f" - {error_json.get('error', {}).get('message', 'Unknown error')}"
                    except:
                        pass
                    raise HTTPException(status_code=500, detail=error_detail)
                
                result = response.json()
                return result["choices"][0]["message"]["content"]
                
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="AI service timeout")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"AI generation failed: {str(e)}")

# Initialize Groq client
groq = GroqClient()

# --- ENDPOINTS ---

@app.post("/generate/lyrics", response_model=LyricsResponse)
async def generate_lyrics(request: LyricsRequest):
    """
    Generuje tekst piosenki używając AI na podstawie gatunku, tematu i nastroju.
    """
    start_time = datetime.now()
    
    # Przygotuj prompt dla AI
    length_instruction = {
        "short": "Napisz krótki tekst (1 zwrotka + refren)",
        "standard": "Napisz pełny tekst (2-3 zwrotki + refren + bridge)",
        "long": "Napisz rozbudowany tekst (3-4 zwrotki + refren + bridge + outro)"
    }.get(request.length, "Napisz pełny tekst piosenki")
    
    system_prompt = f"""Jesteś profesjonalnym autorem tekstów muzycznych. Tworzysz oryginalne, kreatywne teksty w języku {request.language}.

ZASADY:
- Tekst musi być oryginalny i nie naruszać praw autorskich
- Używaj poetyckiego języka odpowiedniego dla gatunku {request.genre}
- Tekst powinien mieć wyraźną strukturę (zwrotka/refren)
- Nastrój: {request.mood}
- {length_instruction}
- Unikaj wulgaryzmów i kontrowersyjnych treści"""

    user_prompt = f"""Napisz tekst piosenki:
- Gatunek: {request.genre}
- Temat: {request.theme}  
- Nastrój: {request.mood}
- Język: {request.language}

Oznacz wyraźnie części piosenki (np. [Zwrotka 1], [Refren], [Zwrotka 2], [Bridge]).
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    # Generuj z AI
    lyrics = await groq.generate_completion(messages, temperature=0.8, max_tokens=1500)
    
    # Policz słowa
    word_count = len(lyrics.split())
    generation_time = (datetime.now() - start_time).total_seconds()
    
    return LyricsResponse(
        lyrics=lyrics,
        generated_by="groq-llama3-8b",
        genre=request.genre,
        theme=request.theme,
        generation_time=f"{generation_time:.2f}s",
        word_count=word_count
    )

@app.post("/generate/description", response_model=DescriptionResponse)
async def generate_description(request: DescriptionRequest):
    """
    Generuje opisy marketingowe dla utworu muzycznego.
    """
    mood_text = f" o nastroju {request.mood}" if request.mood else ""
    
    system_prompt = f"""Jesteś ekspertem od marketingu muzycznego. Tworzysz angażujące opisy utworów muzycznych dla różnych platform.

Grupa docelowa: {request.target_audience}

ZADANIA:
1. Krótki opis (1-2 zdania) - zwięzły, zachęcający
2. Opis marketingowy (50-100 słów) - bardziej szczegółowy, emocjonalny
3. Podpis dla social media (krótki, z emotikonami)
4. 5-8 hashtagów dla social media

Używaj profesjonalnego, ale przystępnego języka polskiego."""

    user_prompt = f"""Stwórz opisy marketingowe dla utworu:
- Tytuł: "{request.title}"
- Artysta: {request.artist}
- Gatunek: {request.genre}{mood_text}

Zwróć odpowiedź w formacie JSON:
{{
  "short_description": "...",
  "marketing_copy": "...", 
  "social_media_caption": "...",
  "hashtags": ["#tag1", "#tag2", ...]
}}"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    response_text = await groq.generate_completion(messages, temperature=0.7, max_tokens=800)
    
    # Próbuj sparsować JSON z odpowiedzi AI
    try:
        # Wyciągnij JSON z odpowiedzi (może być w ```json``` bloku)
        if "```json" in response_text:
            json_start = response_text.find("```json") + 7
            json_end = response_text.find("```", json_start)
            json_text = response_text[json_start:json_end].strip()
        else:
            json_text = response_text.strip()
        
        parsed_response = json.loads(json_text)
        
        return DescriptionResponse(
            short_description=parsed_response.get("short_description", ""),
            marketing_copy=parsed_response.get("marketing_copy", ""),
            social_media_caption=parsed_response.get("social_media_caption", ""),
            hashtags=parsed_response.get("hashtags", []),
            generated_by="groq-llama3-8b"
        )
        
    except json.JSONDecodeError:
        # Fallback - zwróć raw response jako short_description
        return DescriptionResponse(
            short_description=response_text[:200] + "...",
            marketing_copy=response_text,
            social_media_caption=f"🎵 {request.title} - {request.artist} 🎵",
            hashtags=[f"#{request.genre.lower()}", "#music", "#newrelease"],
            generated_by="groq-llama3-8b"
        )

@app.post("/analyze/text", response_model=AnalysisResponse)
async def analyze_text(request: AnalyzeRequest):
    """
    Analizuje tekst pod kątem sentymentu, gatunku, lub tematyki.
    """
    analysis_prompts = {
        "sentiment": "Przeanalizuj sentiment tego tekstu. Określ czy jest pozytywny, negatywny, czy neutralny. Podaj procent pewności i główne powody.",
        "genre": "Określ gatunek muzyczny na podstawie tego tekstu piosenki. Wskaż główny gatunek i 2-3 potencjalne podgatunki.",
        "themes": "Zidentyfikuj główne tematy i motywy w tym tekście. Jakie emocje i znaczenia są obecne?"
    }
    
    system_prompt = "Jesteś ekspertem analizy tekstów muzycznych. Analizujesz teksty pod kątem różnych aspektów i dajesz konkretne, pomocne odpowiedzi."
    
    user_prompt = f"""{analysis_prompts.get(request.analysis_type, analysis_prompts['sentiment'])}

TEKST DO ANALIZY:
{request.text}

Zwróć odpowiedź w formacie JSON z polami: analysis, confidence (0.0-1.0), suggestions[]"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    response_text = await groq.generate_completion(messages, temperature=0.3, max_tokens=600)
    
    # Próbuj wyciągnąć strukturalne dane z odpowiedzi
    try:
        if "```json" in response_text:
            json_start = response_text.find("```json") + 7
            json_end = response_text.find("```", json_start)
            json_text = response_text[json_start:json_end].strip()
            parsed = json.loads(json_text)
        else:
            # Fallback parsing
            parsed = {"analysis": response_text, "confidence": 0.8, "suggestions": []}
        
        return AnalysisResponse(
            analysis_type=request.analysis_type,
            results=parsed,
            confidence=parsed.get("confidence", 0.8),
            suggestions=parsed.get("suggestions", ["Spróbuj bardziej szczegółowej analizy"])
        )
        
    except:
        # Fallback response
        return AnalysisResponse(
            analysis_type=request.analysis_type,
            results={"analysis": response_text, "raw_response": True},
            confidence=0.7,
            suggestions=["Analiza dostępna w formacie tekstowym"]
        )

@app.get("/ai/status")
async def ai_status():
    """
    Sprawdza status usługi AI i dostępność modeli.
    """
    status = {
        "service": "prometheus-ai",
        "status": "running",
        "ai_provider": "groq",
        "model": "llama3-8b-8192",
        "api_key_configured": bool(groq.api_key),
        "features": [
            "lyrics_generation",
            "description_generation", 
            "text_analysis"
        ]
    }
    
    # Test AI connectivity
    if groq.api_key:
        try:
            test_messages = [{"role": "user", "content": "Odpowiedz 'OK' jeśli działasz."}]
            test_response = await groq.generate_completion(test_messages, max_tokens=10)
            status["ai_test"] = "passed"
            status["ai_response"] = test_response.strip()
        except Exception as e:
            status["ai_test"] = "failed"
            status["ai_error"] = str(e)
    else:
        status["ai_test"] = "skipped - no API key"
    
    return status

@app.get("/")
def root():
    """
    Główny endpoint serwisu AI.
    """
    return {
        "service": "Prometheus AI Service",
        "version": "1.0.0",
        "description": "AI-powered content generation for HardbanRecords Lab",
        "endpoints": {
            "lyrics": "/generate/lyrics",
            "descriptions": "/generate/description",
            "analysis": "/analyze/text",
            "status": "/ai/status",
            "docs": "/docs"
        }
    }