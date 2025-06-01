import zipfile
import string
import time
from multiprocessing import Pool, cpu_count, Manager, Event

def get_charset(choice):
    sets = {
        '1': string.ascii_lowercase,
        '2': string.ascii_uppercase,
        '3': string.digits,
        '4': string.punctuation,
        '5': string.ascii_letters + string.digits,
        '6': string.ascii_letters + string.digits + string.punctuation
    }
    return sets.get(choice, string.ascii_lowercase)

def index_to_password(index, length, charset):
    base = len(charset)
    pwd = []
    for _ in range(length):
        pwd.append(charset[index % base])
        index //= base
    return ''.join(reversed(pwd))

def try_password(args):
    zip_file, length, start, end, charset, found_event, queue = args
    with zipfile.ZipFile(zip_file) as zf:
        for idx in range(start, end):
            if found_event.is_set():
                return None
            pwd = index_to_password(idx, length, charset)
            queue.put(pwd)  # Anlık denenen şifreyi gönder
            try:
                zf.extractall(pwd=pwd.encode('utf-8'))
                found_event.set()
                return pwd
            except:
                continue
    return None

def estimate_crack_time(charset_len, length, cpu_cores):
    total_combinations = charset_len ** length
    print(f"Toplam kombinasyon sayısı: {total_combinations}")

    # Ortalama deneme süresini kabaca ölçmek için örnekleme
    sample_size = 1000
    charset = string.ascii_lowercase  # Basit örnek charset, sadece zaman ölçümü için
    start_time = time.time()
    for i in range(sample_size):
        _ = index_to_password(i, length, charset)
    elapsed = time.time() - start_time
    avg_time_per_attempt = elapsed / sample_size
    print(f"Ortalama deneme süresi (şifre üretimi için, tahmini): {avg_time_per_attempt:.8f} saniye")

    # Tahmini süre (şifre üretme için) - ZIP şifre denemesi değil, gerçek denemeler daha yavaş olabilir
    estimated_seconds = total_combinations * avg_time_per_attempt / cpu_cores

    def sec_to_str(sec):
        if sec < 60:
            return f"{sec:.2f} saniye"
        elif sec < 3600:
            return f"{sec/60:.2f} dakika"
        elif sec < 86400:
            return f"{sec/3600:.2f} saat"
        else:
            return f"{sec/86400:.2f} gün"

    return sec_to_str(estimated_seconds)

def brute_force(zip_file, charset, min_len, max_len):
    cpu_cores = cpu_count()
    manager = Manager()
    found_event = manager.Event()
    queue = manager.Queue()

    for length in range(min_len, max_len + 1):
        print(f'Trying passwords of length {length}...')

        # Tahmini süreyi yazdır (her uzunluk için ayrı ayrı)
        estimation = estimate_crack_time(len(charset), length, cpu_cores)
        print(f"Tahmini kırma süresi (şifre uzunluğu {length}): {estimation}")

        total = len(charset) ** length
        chunk_size = total // cpu_cores + 1

        with Pool(cpu_cores) as pool:
            args = []
            for i in range(cpu_cores):
                start = i * chunk_size
                end = min((i + 1) * chunk_size, total)
                args.append((zip_file, length, start, end, charset, found_event, queue))

            result = pool.map_async(try_password, args)

            # Anlık denenen şifreleri ekrana yazdır
            while not result.ready():
                while not queue.empty():
                    pwd = queue.get()
                    print(f"Trying: {pwd}", end='\r', flush=True)
                if found_event.is_set():
                    break
                time.sleep(0.1)

            passwords = result.get()
            for pwd in passwords:
                if pwd:
                    print(f"\n[+] Password found: {pwd}")
                    return pwd
    print("\n[-] Password not found in given charset and length range.")
    return None

def get_positive_int(prompt, min_value=1):
    while True:
        try:
            val = int(input(prompt))
            if val < min_value:
                print(f"Lütfen en az {min_value} veya daha büyük bir sayı girin.")
                continue
            return val
        except ValueError:
            print("Lütfen geçerli bir sayı girin.")

if __name__ == '__main__':
    print("=== Zip Brute Force Script ===")
    zip_file = input("Zip dosyası adı (örnek: archive.zip): ").strip()

    print("Karakter seti seçenekleri:")
    print("1) Küçük harfler (a-z)")
    print("2) Büyük harfler (A-Z)")
    print("3) Sayılar (0-9)")
    print("4) Özel karakterler (!@#$...)")
    print("5) Küçük+Büyük harf + Sayılar")
    print("6) Tümü (harf + sayı + özel)")

    while True:
        charset_choice = input("Karakter seti seç (1-6): ").strip()
        if charset_choice in {'1','2','3','4','5','6'}:
            break
        print("Lütfen 1 ile 6 arasında geçerli bir seçim yapın.")

    charset = get_charset(charset_choice)

    min_len = get_positive_int("Minimum şifre uzunluğu (en az 1): ", 1)
    max_len = get_positive_int(f"Maksimum şifre uzunluğu (en az {min_len}): ", min_len)

    brute_force(zip_file, charset, min_len, max_len)
