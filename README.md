🗜️ Zip Brute Force Şifre Kırıcı

Bu Python scripti, **parolası bilinmeyen şifreli ZIP dosyalarının** şifresini brute force yöntemiyle kırmak için tasarlanmıştır.  
Şifre denemelerini çok çekirdekli işlemci desteğiyle **paralel olarak** yapar ve denenen şifreleri anlık olarak gösterir.

---

🚀 Özellikler

- Çoklu CPU çekirdeği desteği ile hızlı brute force denemeleri  
- Şifre denemelerini gerçek zamanlı terminal çıktısında gösterme  
- Kullanıcı tarafından seçilebilen karakter seti (küçük harf, büyük harf, sayı, özel karakter vs.)  
- Minimum ve maksimum şifre uzunluğu aralığı belirleyebilme  
- Kolay kullanımlı komut satırı arayüzü  

---

📋 Önemli Notlar

- **AES şifrelemesi (zip dosyalarının bazı modern şifreleme türleri) desteklenmez.**  
  Bu script sadece klasik ZIP şifreleme (ZipCrypto) ile korunan dosyalar için çalışır.  
- Çok büyük şifre uzunlukları ve geniş karakter setlerinde kırma süresi çok uzayabilir, sabırlı olun.  
- Script sadece şifreyi deneme amaçlıdır, etik ve yasal sınırlar içinde kullanınız.

---

🛠️ Kullanım

1. Python 3 yüklü olduğundan emin olun.

2. Scripti çalıştırın:

   python zip_bruteforce.py

3. Zip dosyasının ismini girin (örn: archive.zip).

4. Karakter setini seçin:  
   1) Küçük harfler (a-z)  
   2) Büyük harfler (A-Z)  
   3) Sayılar (0-9)  
   4) Özel karakterler (!@#$...)  
   5) Küçük + Büyük harf + Sayılar  
   6) Tümü (harf + sayı + özel karakterler)

5. Minimum ve maksimum şifre uzunluğunu belirleyin.

6. Script denemeye başlayacak ve anlık olarak hangi şifrenin denendiğini gösterecek.  
   Şifre bulunursa ekrana yazdırılır.

---

⚙️ Teknik Detaylar

- Şifreler, seçilen karakter setine göre **sayısal indeks** kullanılarak sıralı üretilir.  
- Paralel işlem için Python’un multiprocessing modülü kullanılır.  
- Zip dosyası zipfile modülü ile açılır ve şifre denenir.  
- Bulunan şifre stdout'a yazılır ve işlem durdurulur.

---

❌ Limitasyonlar

- AES veya diğer gelişmiş zip şifreleme yöntemleri desteklenmez.  
- Çok uzun ve karmaşık şifrelerde başarı garantisi yoktur.  
- Şifre tahmin süresi karakter seti büyüklüğüne ve uzunluğuna bağlıdır.

---

🤝 Katkıda Bulunma

Bu script üzerinde geliştirme yapmak veya iyileştirme önermek isterseniz, pull request veya issue açabilirsiniz.

---

📜 Lisans

Bu proje MIT Lisansı ile lisanslanmıştır. İstediğiniz gibi kullanabilir ve geliştirebilirsiniz.

---

İyi şanslar! 🍀

Not: Bu araç sadece yetkili olduğunuz dosyalar üzerinde kullanılmalıdır. İzinsiz erişim yasa dışıdır.
