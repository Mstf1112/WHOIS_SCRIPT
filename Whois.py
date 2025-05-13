import whois
import os
from datetime import datetime

# ANSI renk kodları
RED_BOLD = "\033[1;31m"
GREEN_BOLD = "\033[1;32m"
RESET = "\033[0m"

# TLD listesi
TLD_LIST = [
    ".com", ".net", ".org", ".io", ".biz", ".info", 
    ".co", ".com.tr", ".net.tr", ".org.tr"
]

def format_date(date_value):
    if isinstance(date_value, list):
        date_value = date_value[0]
    if isinstance(date_value, datetime):
        return date_value.strftime("%Y-%m-%d")
    return str(date_value)

# Domain kontrol fonksiyonu
def check_domain(domain_name):
    try:
        domain_info = whois.whois(domain_name)
        if domain_info.domain_name:
            created = format_date(domain_info.creation_date)
            updated = format_date(domain_info.updated_date)
            expires = format_date(domain_info.expiration_date)
            registrar = domain_info.registrar or "Bilinmiyor"
            registrant = domain_info.name or "Bilinmiyor"

            result = (
                f"[X] {domain_name} ALINMIŞ ✅\n"
                f"  - Kayıt Eden   : {registrant}\n"
                f"  - Kayıt Firması: {registrar}\n"
                f"  - Kayıt Tarihi : {created}\n"
                f"  - Bitiş Tarihi : {expires}\n"
                f"  - Güncelleme   : {updated}"
            )
            return result, "taken"
    except:
        pass
    return f"[✓] {domain_name} UYGUN 🔓", "available"

def main():
    try:
        with open("domains.txt", "r", encoding="utf-8") as f:
            base_domains = [line.strip().lower() for line in f if line.strip()]
    except FileNotFoundError:
        print("HATA: 'domains.txt' dosyası bulunamadı!")
        return

    today = datetime.now().strftime("%d-%m-%Y")
    history_dir = "History"
    os.makedirs(history_dir, exist_ok=True)
    log_file_path = os.path.join(history_dir, f"{today}.txt")

    with open(log_file_path, "w", encoding="utf-8") as log_file:
        for base in base_domains:
            header = f"\n--- {base} için kontrol ---\n"
            print(header)
            log_file.write(header)
            for tld in TLD_LIST:
                full_domain = base + tld
                result, status = check_domain(full_domain)
                if status == "taken":
                    print(f"{RED_BOLD}{result}{RESET}")
                else:
                    print(f"{GREEN_BOLD}{result}{RESET}")
                log_file.write(result + "\n")

    print(f"\n✅ Tüm sonuçlar '{log_file_path}' dosyasına kaydedildi.")

if __name__ == "__main__":
    main()
