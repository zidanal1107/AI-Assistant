import customtkinter as ctk
# Mengimpor modul LLMClient dari folder core
from core.llm_client import LLMClient

# Mengatur tema global aplikasi
ctk.set_appearance_mode("Dark")  # Memaksa mode gelap agar lebih estetik sesuai desain
ctk.set_default_color_theme("blue") 

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- CONFIGURE WINDOW ---
        self.title("DANAL AI - All-in-One Desktop Assistant")
        self.geometry("1150x700") 
        
        # Inisialisasi Otak AI menggunakan model Qwen yang sudah kamu pull
        self.ai_brain = LLMClient(model_name="gemini-2.5-flash")
        # List untuk menampung riwayat obrolan selama aplikasi menyala
        self.riwayat_chat = []
        
        # Grid layout utama (Kolom 0: Sidebar, Kolom 1: Konten Utama)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR FRAME ---
        # Memberikan warna latar belakang gelap yang seragam (#262626)
        self.sidebar_frame = ctk.CTkFrame(self, width=260, corner_radius=0, fg_color="#262626")
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1) 

        # 1. LOGO / JUDUL APLIKASI
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="✨ DANAL", 
            font=ctk.CTkFont(family="Helvetica", size=26, weight="bold"),
            text_color="white"
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(35, 20), sticky="w")

        # Garis pembatas tipis di bawah logo
        self.separator = ctk.CTkFrame(self.sidebar_frame, height=1, fg_color="#404040")
        self.separator.grid(row=1, column=0, padx=20, pady=(0, 25), sticky="ew")

        # 2. TOMBOL NAVIGASI (Spasi diseragamkan menjadi 1 spasi setelah emoji agar sejajar sempurna)
        self.nav_buttons = []

        self.btn_chat = ctk.CTkButton(
            self.sidebar_frame, text="💬 AI Chat", anchor="w", height=45, 
            font=ctk.CTkFont(size=15), corner_radius=8,
            command=lambda: self.pindah_menu(self.btn_chat, self.buka_menu_chat)
        )
        self.btn_chat.grid(row=2, column=0, padx=20, pady=6, sticky="ew")
        self.nav_buttons.append(self.btn_chat)

        self.btn_vision = ctk.CTkButton(
            self.sidebar_frame, text="👁️ AI Vision", anchor="w", height=45, 
            font=ctk.CTkFont(size=15), corner_radius=8,
            command=lambda: self.pindah_menu(self.btn_vision, self.buka_menu_vision)
        )
        self.btn_vision.grid(row=3, column=0, padx=20, pady=6, sticky="ew")
        self.nav_buttons.append(self.btn_vision)

        self.btn_docs = ctk.CTkButton(
            self.sidebar_frame, text="📂 Documents", anchor="w", height=45, 
            font=ctk.CTkFont(size=15), corner_radius=8,
            command=lambda: self.pindah_menu(self.btn_docs, self.buka_menu_docs)
        )
        self.btn_docs.grid(row=4, column=0, padx=20, pady=6, sticky="ew")
        self.nav_buttons.append(self.btn_docs)

        self.btn_tools = ctk.CTkButton(
            self.sidebar_frame, text="⚙️ System & Tools", anchor="w", height=45, 
            font=ctk.CTkFont(size=15), corner_radius=8,
            command=lambda: self.pindah_menu(self.btn_tools, self.buka_menu_tools)
        )
        self.btn_tools.grid(row=5, column=0, padx=20, pady=6, sticky="ew")
        self.nav_buttons.append(self.btn_tools)

        # 3. BAGIAN BAWAH SIDEBAR (Pemilih Tema)
        self.theme_label = ctk.CTkLabel(self.sidebar_frame, text="Mode Tampilan:", anchor="w", font=ctk.CTkFont(size=12), text_color="gray")
        self.theme_label.grid(row=7, column=0, padx=25, pady=(10, 0), sticky="w")
        
        self.theme_optionmenu = ctk.CTkOptionMenu(
            self.sidebar_frame, values=["Dark", "Light", "System"], command=self.ubah_tema,
            fg_color="#333333", button_color="#404040", button_hover_color="#4d4d4d"
        )
        self.theme_optionmenu.grid(row=8, column=0, padx=20, pady=(5, 25), sticky="ew")

        # --- MAIN CONTENT FRAME ---
        self.main_frame = ctk.CTkFrame(self, corner_radius=15, fg_color=("#f5f5f5", "#1c1c1c"))
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        # Set halaman default awal
        self.tampilkan_halaman_welcome()
        # Mengaktifkan indikator tombol pertama secara default (AI Chat)
        self.set_tombol_aktif(self.btn_chat) 

    # --- LOGIKA NAVIGASI & KOSMETIK ---

    def set_tombol_aktif(self, tombol_aktif):
        """Mengubah warna tombol aktif menjadi biru solid, dan meredupkan yang lain"""
        for btn in self.nav_buttons:
            if btn == tombol_aktif:
                btn.configure(fg_color="#1F6AA5", text_color="white") 
            else:
                btn.configure(fg_color="transparent", text_color="gray90") 

    def pindah_menu(self, tombol, fungsi_halaman):
        self.reset_main_frame()
        self.set_tombol_aktif(tombol)
        fungsi_halaman()

    def ubah_tema(self, tema_baru):
        ctk.set_appearance_mode(tema_baru)

    def reset_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def tampilkan_halaman_welcome(self):
        self.reset_main_frame()
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        welcome_label = ctk.CTkLabel(self.main_frame, text="Selamat Datang di DANAL AI\nSilakan pilih menu di samping untuk memulai.", font=ctk.CTkFont(size=16))
        welcome_label.grid(row=0, column=0)

    # --- HALAMAN CHAT (RESPONSIF & AREA INPUT-OUTPUT DIPERBESAR) ---

    def buka_menu_chat(self):
        # Konfigurasi Grid Utama Halaman Chat
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)  # Baris 0 (Chat Display) mengambil sisa space terbesar
        self.main_frame.grid_rowconfigure(1, weight=0)  # Baris 1 (Input Area) tetap kokoh di bawah
        
        # 1. CHAT DISPLAY (DIperbesar padding internal & ukuran font)
        self.chat_display = ctk.CTkTextbox(
            self.main_frame, 
            state="disabled", 
            corner_radius=12, 
            fg_color=("#ffffff", "#242424"), 
            text_color=("#111111", "#e6e6e6"),
            font=ctk.CTkFont(family="Inter", size=15, weight="normal"), # Ukuran teks output diperbesar
            spacing1=8,  # Jarak antar baris paragraf agar lebih lega
            spacing3=8
        )
        # Menggunakan padx/pady 30 agar teks tidak terlalu menempel ke pinggir frame utama
        self.chat_display.grid(row=0, column=0, padx=30, pady=(30, 15), sticky="nsew")
        
        # 2. INPUT CONTAINER FRAME (Dibuat responsif meluas secara horizontal)
        input_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        input_frame.grid(row=1, column=0, padx=30, pady=(0, 30), sticky="ew")
        input_frame.grid_columnconfigure(0, weight=1) # Entry box akan membesar mengikuti ukuran window
        
        # 3. CHAT ENTRY BOX (Dipertinggi dan diperbesar font-nya)
        self.chat_entry = ctk.CTkEntry(
            input_frame, 
            placeholder_text="Tanya sesuatu ke DANAL AI...",
            height=50, # Tinggi entry box dinaikkan dari default agar elegan
            font=ctk.CTkFont(size=15), # Ukuran teks input diperbesar
            corner_radius=10,
            border_width=1,
            border_color=("#d1d1d1", "#3b3b3b"),
            fg_color=("#f9f9f9", "#2e2e2e")
        )
        self.chat_entry.grid(row=0, column=0, padx=(0, 15), sticky="ew")
        
        # Bind tombol 'Enter'
        self.chat_entry.bind("<Return>", lambda event: self.kirim_pesan_ke_ai())
        
        # 4. TOMBOL KIRIM MODEREN
        self.btn_kirim = ctk.CTkButton(
            input_frame, 
            text="Kirim 🚀", 
            width=120, 
            height=50, # Tinggi disamakan dengan Entry Box agar sejajar presisi
            font=ctk.CTkFont(size=15, weight="bold"),
            corner_radius=10,
            hover_color="#1a5c8f",
            command=self.kirim_pesan_ke_ai
        )
        self.btn_kirim.grid(row=0, column=1, sticky="ns")

    def kirim_pesan_ke_ai(self):
        pesan_user = self.chat_entry.get().strip()
        if not pesan_user:
            return

        # 1. Tampilkan pesan user ke kotak chat (Jarak dikurangi menjadi hanya 1 baris kosong setelahnya)
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", f"👤 Anda:\n{pesan_user}\n\n")
        
        # Siapkan placeholder untuk jawaban DANAL
        self.chat_display.insert("end", "🤖 DANAL:\n")
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")
        
        self.chat_entry.delete(0, "end")

        # Fungsi yang menangani setiap kata yang masuk dari Gemini
        def terima_potongan_kata(chunk_teks):
            self.chat_display.configure(state="normal")
            self.chat_display.insert("end", chunk_teks)
            self.chat_display.configure(state="disabled")
            self.chat_display.see("end")

        # Fungsi yang dipanggil saat Gemini SUDAH SELESAI mengetik seluruhnya
        def selesai_merespons(jawaban_penuh):
            self.chat_display.configure(state="normal")
            # Cukup beri 2 kali newline (\n\n) sebagai pembatas tegas antar gelembung chat berikutnya
            self.chat_display.insert("end", "\n\n") 
            self.chat_display.configure(state="disabled")
            
            # Simpan ke riwayat memori jangka pendek aplikasi
            self.riwayat_chat.append({"role": "user", "content": pesan_user})
            self.riwayat_chat.append({"role": "assistant", "content": jawaban_penuh})
            self.chat_display.see("end")

        # 2. Panggil fungsi stream dari LLMClient
        self.ai_brain.kirim_pesan_stream(
            pesan_user, 
            self.riwayat_chat, 
            terima_potongan_kata, 
            selesai_merespons
        )
        
    # --- HALAMAN LAIN (Menunggu Tahap Selanjutnya) ---

    def buka_menu_vision(self):
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        label = ctk.CTkLabel(self.main_frame, text="👁️ AI Vision Mode (Kamera/Gambar)", font=ctk.CTkFont(size=18, weight="bold"))
        label.grid(row=0, column=0, pady=20)

    def buka_menu_docs(self):
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        label = ctk.CTkLabel(self.main_frame, text="📂 PDF Reader & Summarizer", font=ctk.CTkFont(size=18, weight="bold"))
        label.grid(row=0, column=0, pady=20)

    def buka_menu_tools(self):
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        label = ctk.CTkLabel(self.main_frame, text="⚙️ System Automation & Tools", font=ctk.CTkFont(size=18, weight="bold"))
        label.grid(row=0, column=0, pady=20)