import os
import threading
from datetime import datetime
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self, model_name="gemini-2.5-flash"):
        self.model_name = model_name
        self.api_key = os.getenv("GEMINI_API_KEY")
        
        if not self.api_key:
            raise ValueError("❌ API Key Gemini tidak ditemukan! Periksa file .env Anda.")
            
        self.client = genai.Client(api_key=self.api_key)

    def get_system_instruction(self):
        waktu_sekarang = datetime.now().strftime("%A, %d %B %Y - Jam %H:%M:%S")
        
        return (
            f"Anda adalah DANAL (Desktop Assistant & Networked AI Agent), asisten desktop All-in-One berbasis Python yang berjalan di komputer pengguna.\n\n"
            f"**PANDUAN PERILAKU & RESPONS:**\n"
            f"1. **Bahasa:** Selalu merespons dalam Bahasa Indonesia yang kasual namun sopan, jelas, ringkas, dan solutif. Hindari penjelasan bertele-tele.\n"
            f"2. **Konteks Waktu:** Saat ini adalah {waktu_sekarang}. Gunakan data ini sebagai kebenaran mutlak jika pengguna bertanya tentang waktu (hari, tanggal, jam, esok, tahun).\n"
            f"3. **Identitas:** Anda terintegrasi dengan sistem operasi pengguna (Arch Linux). Jika relevan, Anda bisa menyarankan perintah terminal (`pacman`, dll).\n"
            f"4. **Format:** Gunakan markdown (bold, bullet points) dengan rapi."
        )

    def kirim_pesan_stream(self, pesan_pengguna, riwayat_chat, callback_chunk, callback_selesai):
        """
        Mengirim pesan ke Gemini dengan fitur Streaming + Threading agar teks mengalir real-time.
        """
        def run():
            try:
                contents = []
                for chat in riwayat_chat:
                    role = "user" if chat["role"] == "user" else "model"
                    contents.append(types.Content(
                        role=role, parts=[types.Part.from_text(text=chat["content"])]
                    ))
                
                contents.append(types.Content(
                    role="user", parts=[types.Part.from_text(text=pesan_pengguna)]
                ))

                config = types.GenerateContentConfig(
                    system_instruction=self.get_system_instruction(),
                    temperature=0.7
                )

                # Menggunakan generate_content_stream agar teks mengalir
                response_stream = self.client.models.generate_content_stream(
                    model=self.model_name,
                    contents=contents,
                    config=config
                )
                
                jawaban_lengkap = ""
                for chunk in response_stream:
                    if chunk.text:
                        jawaban_lengkap += chunk.text
                        # Kirim potongan kata ke GUI secara real-time
                        callback_chunk(chunk.text)
                
                # Jika sudah selesai, panggil callback selesai untuk menyimpan riwayat
                callback_selesai(jawaban_lengkap)
                
            except Exception as e:
                callback_chunk(f"❌ Gagal terhubung ke API Gemini.\nError: {str(e)}")
                callback_selesai(f"❌ Error: {str(e)}")

        # Jalankan di background agar GUI tidak hang/freeze
        threading.Thread(target=run, daemon=True).start()