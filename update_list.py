import requests

def fetch_and_clean_list(url):
    response = requests.get(url)
    response.raise_for_status()

    lines = response.text.splitlines()
    
    comments = []
    ip_addresses = []
    
    for line in lines:
        line = line.strip()
        if not line:
            comments.append("")
        elif line.startswith("#"):
            comments.append(line)
        else:
            parts = line.split()
            if len(parts) >= 2:
                ip = parts[0]
                count = int(parts[1])
                if count >= 2:
                    ip_addresses.append(ip)
                
    header = "\n".join(comments)
    ips = "\n".join(ip_addresses)
    
    return f"{header}\n{ips}"

if __name__ == "__main__":
    url = "https://raw.githubusercontent.com/stamparm/ipsum/refs/heads/master/ipsum.txt"
    
    print("Fetching and cleaning the IP list...")
    try:
        cleaned_list = fetch_and_clean_list(url)
        with open("edl_list.txt", "w") as f:
            f.write(cleaned_list)
        print("Successfully updated edl_list.txt with header comments and filtered IPs.")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the list: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")