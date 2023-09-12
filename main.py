import socket
import time
import os
import random
import string
import datetime

# Global variables
valid_domains = []
taken_domains = []
domain_history = []
settings = {
    "require_https": False,
    "require_tld": False,
}

def write_to_log(domain_name, result, log_filename):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "Taken" if result else "Available"
    log_entry = f"[{timestamp}] Domain: {domain_name} - Status: {status}\n"

    with open(log_filename, "a") as log_file:
        log_file.write(log_entry)

def load_wordlist(filename):
    wordlist = []
    try:
        with open(filename, "r") as file:
            wordlist = file.read().splitlines()
    except FileNotFoundError:
        print(f"Wordlist '{filename}' is empty or not found. Please create it in the script's directory.")
    return wordlist

wordlist = load_wordlist("wordlist.txt")

# Add more TLDs here (make sure they are real)
tlds = [".com", ".net", ".org", ".io", ".app", ".dev", ".co", ".biz"]

def is_domain_taken(domain_name):
    try:
        if settings["require_https"] and not domain_name.startswith("https://"):
            return False

        if settings["require_tld"] and not any(domain_name.endswith(tld) for tld in tlds):
            return False

        socket.gethostbyname(domain_name)
        return True
    except socket.gaierror:
        return False

def generate_random_domain():
    tld = random.choice(tlds)
    random_string = ''.join(random.choice(string.ascii_lowercase) for _ in range(8))
    return f"{random_string}{tld}"

def generate_godaddy_claim_link(domain_name):
    return f"https://www.godaddy.com/domainsearch/find?checkAvail=1&domainToCheck={domain_name}"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu():
    while True:
        clear_screen()
        print("========================================")
        print("     Python Domain Checker Pro")
        print("         Made by WiiZARDD")
        print("========================================\n")
        print("\x1b[44m1\x1b[0m - Check a single domain")
        print("\x1b[44m2\x1b[0m - View domain search history")
        print("\x1b[44m3\x1b[0m - Bulk domain checking")
        print("\x1b[44m4\x1b[0m - Settings")
        print("\x1b[44m5\x1b[0m - Exit\n")

        choice = input("Enter your choice (1/2/3/4/5): ").strip()

        if choice == '1':
            domain_name = input("Enter a domain name to check: ").strip()
            check_domain(domain_name)

        elif choice == '2':
            display_history()

        elif choice == '3':
            bulk_domain_check()

        elif choice == '4':
            change_settings()

        elif choice == '5':
            break

def check_domain(domain_name):
    result = is_domain_taken(domain_name)
    domain_history.append((domain_name, result))

    if result:
        taken_domains.append(domain_name)
    else:
        valid_domains.append(domain_name)

    write_to_log(domain_name, result, "domain_history.log")

    clear_screen()
    print("========================================")
    print("     Python Domain Checker Pro")
    print("         Made by WiiZARDD")
    print("========================================\n")

    print("Checking availability for domain:")
    print("\x1b[36m{}\x1b[0m".format(domain_name))
    print("\nResult:")

    if result:
        print("\x1b[31mThis domain is taken.\x1b[0m")
    else:
        print("\x1b[32mThis domain is available.\x1b[0m")
        claim_link = generate_godaddy_claim_link(domain_name)
        print(f"Claim this domain on GoDaddy: \x1b[36m{claim_link}\x1b[0m")

    input("\nPress Enter to continue...")
    time.sleep(1)

def display_history():
    clear_screen()
    print("========================================")
    print("     Python Domain Checker Pro")
    print("         Made by WiiZARDD")
    print("========================================\n")

    print("Valid Domains:")
    for i, domain in enumerate(valid_domains, start=1):
        print("{:2d}. \x1b[32m{}\x1b[0m".format(i, domain))

    print("\nTaken Domains:")
    for i, domain in enumerate(taken_domains, start=1):
        print("{:2d}. \x1b[31m{}\x1b[0m".format(i, domain))

    input("\nPress Enter to continue...")

def bulk_domain_check():
    clear_screen()
    print("========================================")
    print("     Python Domain Checker Pro")
    print("         Made by WiiZARDD")
    print("========================================\n")

    input_text = input("Enter a list of domain names separated by commas:\n")
    domains = [domain.strip() for domain in input_text.split(",")]

    for i, domain in enumerate(domains):
        clear_screen()
        print("========================================")
        print("     Python Domain Checker Pro")
        print("         Made by WiiZARDD")
        print("========================================\n")

        print("Checking domain {}/{}:".format(i + 1, len(domains)))
        print("\x1b[36m{}\x1b[0m".format(domain))

        check_domain(domain)
        time.sleep(0.5)

    print("\nBulk checking completed.")
    input("\nPress Enter to continue...")

def change_settings():
    global settings
    while True:
        clear_screen()
        print("========================================")
        print("           Settings")
        print("========================================\n")

        print("1. Toggle 'https://' prefix requirement (Current: {})".format(settings["require_https"]))
        print("2. Toggle '.com' top-level domain requirement (Current: {})".format(settings["require_tld"]))
        print("3. Back to Main Menu\n")

        choice = input("Enter your choice (1/2/3): ").strip()

        if choice == '1':
            settings["require_https"] = not settings["require_https"]
        elif choice == '2':
            settings["require_tld"] = not settings["require_tld"]
        elif choice == '3':
            break

def main():
    display_menu()

if __name__ == "__main__":
    main()
