# ============================================
# GEREKLİ KÜTÜPHANELERİ İÇE AKTAR
# ============================================
import pygame  # Oyun geliştirme kütüphanesi - grafik, ses, input yönetimi sağlar
import sys  # Sistem işlemleri için - programı kapatmak için kullanacağız
import random  # Rastgele sayı üretmek için - elmanın konumunu belirlemede kullanacağız

# ============================================
# PYGAME'İ BAŞLAT
# ============================================
pygame.init()  # Pygame'in tüm modüllerini başlatır (görüntü, ses, font vb.)

# ============================================
# RENK TANIMLARI (RGB FORMATINDA)
# ============================================
# RGB = Red, Green, Blue - Her değer 0-255 arası
BLACK = (0, 0, 0)  # Siyah - arka plan için
WHITE = (255, 255, 255)  # Beyaz - metin için
RED = (255, 0, 0)  # Kırmızı - elma için
GREEN = (0, 255, 0)  # Yeşil - yılan için
DARK_GREEN = (0, 200, 0)  # Koyu yeşil - yılanın başı için (farklılaştırma)

# ============================================
# EKRAN AYARLARI
# ============================================
SCREEN_WIDTH = 600  # Pencere genişliği piksel cinsinden
SCREEN_HEIGHT = 600  # Pencere yüksekliği piksel cinsinden
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Oyun penceresini oluştur
pygame.display.set_caption("Snake Oyunu")  # Pencere başlığını ayarla

# ============================================
# IZGARA SİSTEMİ AYARLARI
# ============================================
CELL_SIZE = 20  # Her karenin boyutu (20x20 piksel) - yılanın her parçası bir kare
GRID_WIDTH = SCREEN_WIDTH // CELL_SIZE  # Yatayda kaç kare var: 600 // 20 = 30 kare
GRID_HEIGHT = SCREEN_HEIGHT // CELL_SIZE  # Dikeyde kaç kare var: 600 // 20 = 30 kare

# ============================================
# OYUN HIZI AYARI
# ============================================
clock = pygame.time.Clock()  # FPS kontrolü için Clock objesi oluştur
FPS = 10  # Saniyede 10 kare - yılan saniyede 10 kez hareket eder (yavaş = kolay)

# ============================================
# YILANIN BAŞLANGIÇ DURUMU
# ============================================
# Yılanı liste olarak tanımlıyoruz - her eleman (x, y) koordinat tuple'ı
# Liste kullanma sebebi: Yılan büyüdükçe parça ekleyeceğiz
snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]  # Başlangıçta tek parça, ekranın ortasında (15, 15)

# Yılanın hareket yönü - (x_değişimi, y_değişimi) formatında
# (1, 0) = sağa, (-1, 0) = sola, (0, 1) = aşağı, (0, -1) = yukarı
snake_direction = (1, 0)  # Başlangıçta sağa doğru hareket ediyor

# ============================================
# ELMANIN BAŞLANGIÇ KONUMU
# ============================================
# Elma rastgele bir konumda oluşturulur
# random.randint(a, b) → a ile b arasında (dahil) rastgele tam sayı üretir
apple = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
# GRID_WIDTH - 1 dememizin sebebi: indeksler 0'dan başlar, son indeks 29'dur (0-29 arası 30 kare)

# ============================================
# SKOR TAKİBİ
# ============================================
score = 0  # Başlangıç skoru 0 - her elma yendiğinde artacak

# ============================================
# FONT AYARI (SKOR GÖSTERMEK İÇİN)
# ============================================
font = pygame.font.Font(None, 36)  # None = varsayılan font, 36 = font boyutu


# ============================================
# YARDIMCI FONKSİYON: YILANI ÇİZ
# ============================================
def draw_snake():
    """
    Yılanın tüm parçalarını ekrana çizer.
    Her parça için bir kare (dikdörtgen) çizer.
    """
    for i, segment in enumerate(snake):
        # enumerate() hem indeksi hem değeri verir
        # i = parçanın sırası (0, 1, 2...), segment = (x, y) koordinatı

        if i == 0:  # İlk parça yılanın başı
            color = DARK_GREEN  # Baş koyu yeşil - görsel ayrım için
        else:  # Diğer parçalar gövde
            color = GREEN  # Gövde açık yeşil

        # pygame.draw.rect() → dikdörtgen çizer
        # Parametreler: (surface, renk, rect)
        # rect = (x_piksel, y_piksel, genişlik, yükseklik)
        pygame.draw.rect(
            screen,  # Çizim yapılacak yüzey
            color,  # Renk
            (segment[0] * CELL_SIZE,  # Izgara x'ini piksele çevir: x * 20
             segment[1] * CELL_SIZE,  # Izgara y'yi piksele çevir: y * 20
             CELL_SIZE,  # Genişlik: 20 piksel
             CELL_SIZE)  # Yükseklik: 20 piksel
        )


# ============================================
# YARDIMCI FONKSİYON: ELMAYI ÇİZ
# ============================================
def draw_apple():
    """
    Elmayı ekrana kırmızı kare olarak çizer.
    """
    pygame.draw.rect(
        screen,  # Çizim yüzeyi
        RED,  # Kırmızı renk
        (apple[0] * CELL_SIZE,  # Elmanın x koordinatını piksele çevir
         apple[1] * CELL_SIZE,  # Elmanın y koordinatını piksele çevir
         CELL_SIZE,  # Genişlik
         CELL_SIZE)  # Yükseklik
    )


# ============================================
# YARDIMCI FONKSİYON: SKORU GÖSTER
# ============================================
def draw_score():
    """
    Ekranın sol üst köşesinde skoru gösterir.
    """
    # font.render() → metin yüzeyi oluşturur
    # Parametreler: (metin, antialiasing, renk)
    score_text = font.render(f"Skor: {score}", True, WHITE)
    # f"Skor: {score}" → f-string, score değişkenini metne gömer
    # True → antialiasing aktif (daha düzgün metin)
    # WHITE → beyaz renk

    # screen.blit() → bir yüzeyi başka bir yüzeye çizer
    # Parametreler: (kaynak_yüzey, (x, y) konumu)
    screen.blit(score_text, (10, 10))  # Sol üst köşeye (10, 10) koordinatına çiz


# ============================================
# YARDIMCI FONKSİYON: YENİ ELMA OLUŞTUR
# ============================================
def create_new_apple():
    """
    Yılanın üzerinde olmayan rastgele bir konumda yeni elma oluşturur.
    """
    while True:  # Uygun konum bulana kadar döngü
        # Rastgele bir konum seç
        new_apple = (random.randint(0, GRID_WIDTH - 1),
                     random.randint(0, GRID_HEIGHT - 1))

        # Eğer bu konum yılanın herhangi bir parçasıyla çakışmıyorsa
        if new_apple not in snake:
            # 'not in' operatörü: liste içinde olup olmadığını kontrol eder
            return new_apple  # Bu konumu döndür ve fonksiyondan çık
        # Çakışıyorsa döngü devam eder, yeni rastgele konum dener


# ============================================
# YARDIMCI FONKSİYON: OYUN BİTTİ EKRANI
# ============================================
def game_over():
    """
    Oyun bittiğinde ekrana 'Game Over' mesajı gösterir.
    """
    # Ekranı siyaha boya (önceki çizimleri temizle)
    screen.fill(BLACK)

    # 'Game Over' metni oluştur
    game_over_text = font.render("GAME OVER!", True, RED)
    # Metni ekranın ortasına yerleştirmek için konum hesapla
    # get_rect() → metnin dikdörtgen bilgilerini verir (genişlik, yükseklik vb.)
    text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
    # center parametresi → dikdörtgenin merkezini belirtilen noktaya ayarlar
    screen.blit(game_over_text, text_rect)  # Metni çiz

    # Final skorunu göster
    final_score_text = font.render(f"Final Skor: {score}", True, WHITE)
    score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
    screen.blit(final_score_text, score_rect)

    # Yeniden başlatma talimatı
    restart_text = font.render("Tekrar oynamak icin R'ye basin", True, WHITE)
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))
    screen.blit(restart_text, restart_rect)

    pygame.display.flip()  # Ekranı güncelle - çizimleri göster

    # Kullanıcının R tuşuna basmasını bekle
    waiting = True  # Bekleme döngüsü kontrolü
    while waiting:
        for event in pygame.event.get():  # Tüm olayları kontrol et
            if event.type == pygame.QUIT:  # Pencere kapatılırsa
                pygame.quit()  # Pygame'i kapat
                sys.exit()  # Programdan çık
            if event.type == pygame.KEYDOWN:  # Bir tuşa basılırsa
                if event.key == pygame.K_r:  # R tuşuna basılmışsa
                    waiting = False  # Bekleme döngüsünden çık
                    return True  # Oyunu yeniden başlat


# ============================================
# ANA OYUN DÖNGÜSÜ
# ============================================
def main_game():
    """
    Ana oyun mantığını içeren fonksiyon.
    """
    # global anahtar kelimesi: Fonksiyon dışındaki değişkenleri değiştirmek için gerekli
    global snake, snake_direction, apple, score

    # Oyun durumu değişkenlerini sıfırla (yeniden başlatma için)
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]  # Yılanı ortada tek parça olarak başlat
    snake_direction = (1, 0)  # Sağa doğru hareket
    apple = create_new_apple()  # Yeni elma oluştur
    score = 0  # Skoru sıfırla

    running = True  # Oyun döngüsü kontrolü - False olunca döngü biter

    while running:  # Oyun döngüsü - her kare için bir kez çalışır

        # ====================================
        # OLAY YÖNETİMİ (Input Handling)
        # ====================================
        for event in pygame.event.get():  # Tüm olayları tek tek al
            if event.type == pygame.QUIT:  # Pencere kapatma olayı (X'e tıklama)
                pygame.quit()  # Pygame'i temiz bir şekilde kapat
                sys.exit()  # Python programını sonlandır

            # Klavye tuş basma olayı
            if event.type == pygame.KEYDOWN:
                # Yön tuşlarına göre hareket yönünü değiştir
                # Ama ters yöne gitmeye izin verme (geri gitmek = kendine çarpma)

                if event.key == pygame.K_UP and snake_direction != (0, 1):
                    # Yukarı ok tuşu VE şu anda aşağı gitmiyorsa
                    snake_direction = (0, -1)  # Yukarı git (y ekseninde -)

                elif event.key == pygame.K_DOWN and snake_direction != (0, -1):
                    # Aşağı ok tuşu VE şu anda yukarı gitmiyorsa
                    snake_direction = (0, 1)  # Aşağı git (y ekseninde +)

                elif event.key == pygame.K_LEFT and snake_direction != (1, 0):
                    # Sol ok tuşu VE şu anda sağa gitmiyorsa
                    snake_direction = (-1, 0)  # Sola git (x ekseninde -)

                elif event.key == pygame.K_RIGHT and snake_direction != (-1, 0):
                    # Sağ ok tuşu VE şu anda sola gitmiyorsa
                    snake_direction = (1, 0)  # Sağa git (x ekseninde +)

        # ====================================
        # YILANIN HAREKETİ
        # ====================================
        # Yeni baş pozisyonunu hesapla
        # snake[0] = mevcut baş, snake_direction = hareket yönü
        new_head = (
            snake[0][0] + snake_direction[0],  # Yeni x = eski x + yön x
            snake[0][1] + snake_direction[1]  # Yeni y = eski y + yön y
        )

        # ====================================
        # ÇARPIŞMA KONTROLÜ
        # ====================================

        # Duvara çarpma kontrolü
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or  # Sol veya sağ duvar
                new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):  # Üst veya alt duvar
            # Oyun bitti
            if game_over():  # game_over() fonksiyonu True dönerse (R'ye basıldı)
                return True  # main_game'den çık, oyunu yeniden başlat
            else:
                return False  # Çıkış yapıldı

        # Kendine çarpma kontrolü
        if new_head in snake:  # Yeni baş, yılanın gövdesindeki herhangi bir parçayla çakışıyor mu?
            if game_over():
                return True
            else:
                return False

        # ====================================
        # YILANI GÜNCELLE
        # ====================================
        # Yeni başı listenin başına ekle
        snake.insert(0, new_head)
        # insert(0, x) → x'i listenin 0. indeksine ekler (başa ekler)
        # Şimdi yılan bir parça uzun, kuyruğu kaldırmalıyız (elma yenmediyse)

        # ====================================
        # ELMA YENDİ Mİ KONTROLÜ
        # ====================================
        if new_head == apple:  # Yılanın başı elmayla çakıştı mı?
            score += 1  # Skoru 1 artır
            apple = create_new_apple()  # Yeni elma oluştur
            # Kuyruğu kaldırma! Yılan büyüsün
        else:
            # Elma yenmediyse, kuyruğu kaldır (yılan aynı boyutta kalır)
            snake.pop()
            # pop() → listenin son elemanını kaldırır ve döndürür
            # Bu sayede yılan hareket eder ama boyutu değişmez

        # ====================================
        # EKRANI GÜNCELLEme
        # ====================================
        screen.fill(BLACK)  # Ekranı siyaha boya (önceki kareyi temizle)

        draw_snake()  # Yılanı çiz
        draw_apple()  # Elmayı çiz
        draw_score()  # Skoru çiz

        pygame.display.flip()  # Tüm çizimleri ekrana yansıt
        # flip() kullanma sebebi: Double buffering - önce arka planda çizer, sonra gösterir
        # Bu sayede titreme (flickering) olmaz

        # ====================================
        # FPS KONTROLÜ
        # ====================================
        clock.tick(FPS)  # FPS değerine göre bekle
        # FPS = 10 ise, her kare arası yaklaşık 100ms (1000ms / 10) bekler
        # Bu sayede oyun istikrarlı hızda çalışır


# ============================================
# PROGRAMIN GİRİŞ NOKTASI
# ============================================
if __name__ == "__main__":
    # Bu satır: "Eğer bu dosya doğrudan çalıştırılıyorsa (import edilmiyorsa)"
    # Python'da standart bir yapı - modül olarak kullanımı destekler

    while True:  # Sonsuz döngü - oyun sürekli yeniden başlayabilir
        restart = main_game()  # Oyunu başlat
        if not restart:  # Eğer main_game() False döndürdüyse (çıkış yapıldı)
            break  # Döngüden çık, program sonlansın