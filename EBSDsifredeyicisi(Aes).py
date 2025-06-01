import zipfile
import subprocess
from multiprocessing import Pool, Manager
import sys
import time

# 7z.exe'nin tam yolu, kendi sistemine göre değiştir
SEVEN_ZIP_PATH = r"C:\Program Files\7-Zip\7z.exe"

def generate_passwords(charset, length):
    if length == 0:
        yield ''
    else:
        for pwd in generate_passwords(charset, length - 1):
            for c in charset:
                yield pwd + c

def try_password_zipfile(pwd, zip_file):
    try:
        with zipfile.ZipFile(zip_file) as zf:
            zf.extractall(pwd=pwd.encode())
        return pwd
    except:
        return None

def try_password_7z(pwd, zip_file):
    cmd = [SEVEN_ZIP_PATH, 't', f'-p{pwd}', zip_file]
    result = subprocess.run(cmd, capture_output=True)
    if b'Everything is Ok' in result.stdout:
        return pwd
    return None

def worker(args):
    pwd, zip_file, method, found_event, queue = args
    if found_event.is_set():
        return None

    # Anlık denenen şifreyi kuyruga gönder
    queue.put(pwd)

    if method == 'zipfile':
        result = try_password_zipfile(pwd, zip_file)
    else:
        result = try_password_7z(pwd, zip_file)

    if result:
        found_event.set()
        queue.put(f"FOUND:{result}")
        return result
    return None

def print_worker(queue, found_event):
    while not found_event.is_set():
        try:
            pwd = queue.get(timeout=0.1)
            if pwd.startswith("FOUND:"):
                print(f"\n[+] Password found: {pwd[6:]}")
                break
            else:
                print(f"Trying: {pwd}", end='\r', flush=True)
        except:
            pass
    # Kuyruktan temizle ve bitir
    while not queue.empty():
        queue.get()

def main():
    print("=== Zip Brute Force Script ===")
    zip_file = input("Zip dosyası adı (örnek: archive.zip): ").strip()

    print("Karakter seti seçenekleri:")
    print("1) Küçük harfler (a-z)")
    print("2) Büyük harfler (A-Z)")
    print("3) Sayılar (0-9)")
    print("4) Özel karakterler (!@#$...)")
    print("5) Küçük+Büyük harf + Sayılar")
    print("6) Tümü (harf + sayı + özel)")
    charset_choice = input("Karakter seti seç (1-6): ").strip()

    sets = {
        '1': 'abcdefghijklmnopqrstuvwxyz',
        '2': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
        '3': '0123456789',
        '4': '!@#$%^&*()-_=+[]{};:,.<>?',
        '5': 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
        '6': 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+[]{};:,.<>?'
    }
    charset = sets.get(charset_choice, '0123456789')

    min_len = int(input("Minimum şifre uzunluğu (en az 1): ").strip())
    max_len = int(input("Maksimum şifre uzunluğu (en az 1): ").strip())

    print("\nZip dosyası AES şifreli mi? (E/h): ", end='')
    aes_input = input().strip().lower()
    if aes_input == 'e' or aes_input == 'evet':
        method = '7z'
    else:
        method = 'zipfile'

    print(f"Using method: {method}\n")

    passwords = []
    for length in range(min_len, max_len + 1):
        for pwd in generate_passwords(charset, length):
            passwords.append(pwd)

    manager = Manager()
    found_event = manager.Event()
    queue = manager.Queue()

    pool = Pool()

    args = ((pwd, zip_file, method, found_event, queue) for pwd in passwords)

    import threading
    printer_thread = threading.Thread(target=print_worker, args=(queue, found_event))
    printer_thread.start()

    print(f"Trying passwords from length {min_len} to {max_len}...\n")

    for result in pool.imap_unordered(worker, args):
        if result:
            # Bulundu, döngü kırılıyor
            break

    pool.terminate()
    pool.join()

    found_event.set()
    printer_thread.join()

    if not result:
        print("\n[-] Password not found in given charset and length range.")

if __name__ == "__main__":
    main()
