from gui.main_window import MainWindow

def main():
    # Menginisialisasi kelas jendela utama kita
    app = MainWindow()
    
    # Memulai loop aplikasi agar jendela tetap terbuka dan mendengarkan klik user
    app.mainloop()

if __name__ == "__main__":
    main()