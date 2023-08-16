import random

# global değişkenler
desteler = ('Kupa', 'Karo', 'Maça', 'Sinek')
rakamlar = ('İki', 'Üç', 'Dört', 'Beş', 'Altı', 'Yedi', 'Sekiz', 'Dokuz', 'On', 'Vale', 'Kız', 'Papaz', 'As')
değerler = {
    'İki': 2,
    'Üç': 3,
    'Dört': 4,
    'Beş': 5,
    'Altı': 6,
    'Yedi': 7,
    'Sekiz': 8,
    'Dokuz': 9,
    'On': 10,
    'Vale': 10,
    'Kız': 10,
    'Papaz': 10,
    'As': 11
}
oynaniyor = True

# Kart sınıfı oluşturma
class Kart():
    def __init__(self, deste, rakam):
        self.deste = deste
        self.rakam = rakam
        
    def __str__(self):
        return self.deste + "  " + self.rakam

# Destee sınıfı oluşturma
class Destee():
    def __init__(self):
        self.destee = []
        for deste in desteler:
            for rakam in rakamlar:
                self.destee.append(Kart(deste, rakam))

    def __str__(self):
        desteeKompozisyonu = ''
        for kart in self.destee:
            desteeKompozisyonu += '\n' + kart.__str__()
        return "Destede şunlar var: " + desteeKompozisyonu

    def karistir(self):
        random.shuffle(self.destee)

    def dagit(self):
        tekKart = self.destee.pop()
        return tekKart

# Oyun tahtası oluşturma
class El():
    def __init__(self):
        self.kartlar = []
        self.değer = 0
        self.aslar = 0

    def kartEkle(self, kart):
        self.kartlar.append(kart)
        self.değer += değerler[kart.rakam]

        if kart.rakam == 'As':
            self.aslar += 1

    def asKontrol(self):
        while self.değer > 21 and self.aslar:
            self.değer -= 10
            self.aslar -= 1

# Oyuncu cips sınıfı
class Cips():
    def __init__(self, toplam=1000):
        self.toplam = toplam
        self.bahis = 0

    def bahisKazan(self):
        self.toplam += self.bahis

    def bahisKaybet(self):
        self.toplam -= self.bahis

# Bahis alma fonksiyonu
def bahisAl(cips):
    while True:
        try:
            cips.bahis = int(input("\nLütfen oynamak istediğiniz bahis tutarını giriniz !!! :"))
        except ValueError:
            print('Üzgünüm, bahis miktarı bir sayı olmalı!')
        else:
            if cips.bahis > cips.toplam:
                print("\nÜzgünüm, bahisiniz toplam çip miktarını aşamaz, sadece {} çipiniz var." .format(cips.toplam))
            else:
                break

# Kart çekme fonksiyonu
def çek(deste, el):
    el.kartEkle(deste.dagit())
    el.asKontrol()

# Oyuncunun kart çekip çekmeyeceğini sorma fonksiyonu
def kartÇekVeyaDur(deste, el):
    global oynaniyor

    while True:
        x = input("\nKart çekmek mi istersiniz, yoksa durmak mı? 'ç' veya 'd' girin: ")

        if x[0].lower() == 'ç':
            çek(deste, el)
        elif x[0].lower() == 'd':
            print("Oyuncu durdu. Dağıtıcı oynuyor.")
            oynaniyor = False
        else:
            print("Üzgünüm, yanlış giriş yaptınız!")
            continue

        break

# Kartları gösterme fonksiyonu
def kartlariGoster(oyuncu, dağıtıcı):
    print("\nDağıtıcının Sırası: ")
    print("<gizli kart>")
    print('', dağıtıcı.kartlar[1])
    print((50*'*'))
    print("\nOyuncunun Sırası:", *oyuncu.kartlar, sep='\n ')
    print((50*'*'))

def tümKartlarıGoster(oyuncu, dağıtıcı):
    print("\nDağıtıcının Sırası:", *dağıtıcı.kartlar, sep='\n ')
    print("Dağıtıcının Toplam Değeri =", dağıtıcı.değer)
    print(50 * '*')
    print("\nOyuncunun Sırası:", *oyuncu.kartlar, sep='\n ')
    print("\nOyuncunun Toplam Değeri =", oyuncu.değer)

# Oyun sonu senaryoları için fonksiyonlaru
def oyuncuPatladi(oyuncu, dağıtıcı, cips):
    print("Oyuncu patladı!")
    cips.bahisKaybet()

def oyuncuKazandi(oyuncu, dağıtıcı, cips):
    print("Oyuncu kazandı!")
    print(50 * '*')
    cips.bahisKazan()

def dağıtıcıPatladi(oyuncu, dağıtıcı, cips):
    print("Dağıtıcı patladı!")
    cips.bahisKazan()

def dağıtıcıKazandi(oyuncu, dağıtıcı, cips):
    print("Dağıtıcı kazandı!")
    print(50 * '*')
    cips.bahisKaybet()

def berabere(oyuncu, dağıtıcı):
    print("Vay be! Berabere.")

# Oyun mantığı
while True:
    print("\n")
    print("Blackjack'e hoş geldiniz".center(50,'*'))
    print("\nElinizde 1000 tl değerinde çip bulunmaktadır.")
    # Kartları karıştır ve her oyuncuya iki kart dağıt
    deste = Destee()
    deste.karistir()

    oyuncuEl = El()
    oyuncuEl.kartEkle(deste.dagit())
    oyuncuEl.kartEkle(deste.dagit())

    dağıtıcıEl = El()
    dağıtıcıEl.kartEkle(deste.dagit())
    dağıtıcıEl.kartEkle(deste.dagit())

    oyuncuCips = Cips()
    bahisAl(oyuncuCips)

    kartlariGoster(oyuncuEl, dağıtıcıEl)

    while oynaniyor:
        kartÇekVeyaDur(deste, oyuncuEl)

        kartlariGoster(oyuncuEl, dağıtıcıEl)

        if oyuncuEl.değer > 21:
            oyuncuPatladi(oyuncuEl, dağıtıcıEl, oyuncuCips)
            break

    if oyuncuEl.değer <= 21:
        while dağıtıcıEl.değer < 17:
            çek(deste, dağıtıcıEl)

        tümKartlarıGoster(oyuncuEl, dağıtıcıEl)

        if dağıtıcıEl.değer > 21:
            dağıtıcıPatladi(oyuncuEl, dağıtıcıEl, oyuncuCips)
        elif dağıtıcıEl.değer > oyuncuEl.değer:
            dağıtıcıKazandi(oyuncuEl, dağıtıcıEl, oyuncuCips)
        elif dağıtıcıEl.değer < oyuncuEl.değer:
            oyuncuKazandi(oyuncuEl, dağıtıcıEl, oyuncuCips)
        else:
            berabere(oyuncuEl, dağıtıcıEl)

    print("\nOyuncunun toplam çip miktarı: {}".format(oyuncuCips.toplam))

    tekrarOyna = input("\nTekrar oynamak ister misiniz? e/h: ")

    if tekrarOyna[0].lower() == 'e':
        oynaniyor = True
        continue
    else:
        print(50*'*')
        print("\nBlackjack oynadığınız için teşekkür ederiz! Tekrar görüşmek üzere.".center(20,'*'))
        break

