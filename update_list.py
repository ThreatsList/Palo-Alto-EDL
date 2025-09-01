import requests

def fetch_and_clean_list(url):
    """
    Fetches a threat intelligence list from a URL, filters it to include only
    IP addresses with a count of 2 or more, and returns a clean string.
    
    :param url: The URL of the threat intelligence feed.
    :return: A string containing only the filtered IP addresses, each on a new line.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the list: {e}")
        return ""

    lines = response.text.splitlines()
    ip_addresses = []
    
    for line in lines:
        line = line.strip()
        # Skip comment lines and empty lines
        if line.startswith("#") or not line:
            continue
        
        parts = line.split()
        if len(parts) >= 2:
            ip = parts[0]
            try:
                count = int(parts[1])
                if count >= 2:
                    ip_addresses.append(ip)
            except ValueError:
                # Handle cases where the second part is not a number
                continue
                
    ips = "\n".join(ip_addresses)
    
    return ips

if __name__ == "__main__":
    url = "https://raw.githubusercontent.com/stamparm/ipsum/refs/heads/master/ipsum.txt"
    
    print("Fetching and cleaning the IP list...")
    try:
        cleaned_list = fetch_and_clean_list(url)
        with open("edl_list.txt", "w") as f:
            f.write(cleaned_list)
        print("Successfully updated edl_list.txt with filtered IPs.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
