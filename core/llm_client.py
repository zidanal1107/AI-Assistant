import os
from datetime import datetime  # <-- 1. Import library waktu
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self, model_name="gemini-2.5-flash"):
        self.model_name = model_name
        self.api_key = os.getenv("GEMINI_API_KEY")
        
        if not self.api_key:
            raise ValueError("❌ API Key Gemini tidak ditemukan!")
            
        self.client = genai.Client(api_key=self.api_key)

    def get_system_instruction(self):
        """
        Fungsi untuk selalu memperbarui waktu saat ini secara real-time
        setiap kali pesan dikirim.
        """
        waktu_sekarang = datetime.now().strftime("%A, %d %B %Y (Jam %H:%M)")
        
        return (
            f"Kamu adalah DANAL, sebuah AI Desktop Assistant All-in-One yang cerdas. "
            f"Jawablah pertanyaan pengguna dengan bahasa Indonesia yang baik, santun, dan ringkas.\n"
            f"KONTEKS WAKTU PENTING: Hari ini/saat ini di komputer pengguna adalah {waktu_sekarang}. "
            f"Gunakan informasi ini jika pengguna bertanya tentang waktu, hari, esok, atau tahun."
        )

    def kirim_pesan(self, pesan_pengguna, riwayat_chat=[]):
        try:
            contents = []
            for chat in riwayat_chat:
                role = "user" if chat["role"] == "user" else "model"
                contents.append(types.Content(
                    role=role,
                    parts=[types.Part.from_text(text=chat["content"])]
                ))
            
            contents.append(types.Content(
                role="user",
                parts=[types.Part.from_text(text=pesan_pengguna)]
            ))

            # <-- 2. Panggil fungsi bertenaga waktu real-time di sini
            config = types.GenerateContentConfig(
                system_instruction=self.get_system_instruction(),
                temperature=0.7
            )

            response = self.client.models.generate_content(
                model=self.model_name,
                contents=contents,
                config=config
            )
            
            return response.text
            
        except Exception as e:
            return f"❌ Gagal terhubung ke API Gemini.\nError: {str(e)}"