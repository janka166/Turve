import argparse
import time
import os
from bs4 import BeautifulSoup
import requests
UA = {"User-Agent": "Mozilla/5.0"}

def get_ip_info(ip):
    try:
        url = f'http://ip-api.com/json/{ip}'
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            status = data.get("status")
            if status == 'success':

                print('Match found:\n')

                result = f'''Country      : {data.get("country")}
Region       : {data.get("regionName")}
City         : {data.get("city")}
ISP Provider : {data.get("isp")}'''

                print(result)
                return result

            else:
                message = data.get("message")
                if message == 'reserved range':

                    try:
                        response = requests.get('https://api.ipify.org')
                        if response.status_code == 200:
                            ip = response.text
                            return get_ip_info(ip)

                        else:
                            print("Error: Unable to retrieve public IP address")
                    except Exception as e:
                        print(f"Error: {e}")

                else:
                    print(f'Unable to retrieve information : {message}')

        elif response.status_code == 404:
            print(f'Invalid Request {ip}')

        else:
            print(f'Unable to retrieve information. Server responded with {response.status_code}')
    except Exception as e:
        print(f'An error occurred: {str(e)}')


def get_user_info(username):
    github = f'https://www.github.com/{username}'
    youtube = f'https://www.youtube.com/@{username}'
    tumblr = f'https://www.tumblr.com/{username}'
    vimeo = f'https://vimeo.com/{username}'
    soundcloud = f'https://soundcloud.com/{username}'

    WEBSITES = [[github, 'Github    '], [youtube, 'YouTube   '], [tumblr, 'Tumblr    '], [vimeo, 'Vimeo     '],
                [soundcloud, 'SoundCloud']]

    result = ''
    for site in WEBSITES:
        r = requests.get(site[0])

        if r.status_code == 200:
            site_result = f'{site[1]} : User Found'
            print(site_result)
            result = result + f'{site_result}\n'

        else:
            site_result = f'{site[1]} : User Not found'
            print(site_result)
            result = result + f'{site_result}\n'

    return result

def getnameinfo(name):
    name_trim = name.strip()
    name_url = name_trim.replace(' ', '/')
    subDirs = []
    try:
        url = f'https://radaris.com/p/{name_url}/'
        response = requests.get(url, headers=UA, timeout=20)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            elementsArr = soup.find_all(
                lambda tag: tag.has_attr('data-href') and 'btn' in tag.get('class', []) and 'rounded-btn' in tag.get(
                    'class', []) and 'btn-primary' in tag.get('class', [])
            )
            for elem in elementsArr:
                href_value = elem.get('data-href')
                if href_value:
                    subDirs.append(href_value)

            data = getprofileinfo(subDirs)
            return data

        elif response.status_code == 404:
            print(f'No matches found for {name}')

        else:
            print(f'Unable to retrieve information. Server responded with {response.status_code}')

    except Exception as e:
        print(f'An error occurred: {str(e)}')


def getprofileinfo(subDirs):
    if len(subDirs) > 0:
        print(f'Found {len(subDirs)} matches:')
        result_parts = []
        for subDir in subDirs:
            matchUrl = f'https://radaris.com{subDir}'
            cardResponse = requests.get(matchUrl, headers=UA, timeout=20)

            if cardResponse.status_code == 200:
                profileSoup = BeautifulSoup(cardResponse.text, 'html.parser')

                person_info = {}
                name_el = profileSoup.find('span', {'class': 'nowrap'})
                person_info['name'] = name_el.get_text(strip=True) if name_el else 'No Info'

                profile_addr = profileSoup.find('a', {'class': 'addr_link'})
                profile_city = profileSoup.find('p', {'class': 'profile-city'})
                profile_phone = profileSoup.find('a', {'class': 'ph'})


                addr_txt = profile_addr.get_text(strip=True) if profile_addr else None
                city_txt = profile_city.get_text(strip=True) if profile_city else None
                if addr_txt or city_txt:

                    if addr_txt and city_txt:
                        person_info['address'] = f'{addr_txt},{city_txt}'
                    else:
                        person_info['address'] = addr_txt or city_txt
                else:
                    person_info['address'] = 'No Info'

                if profile_phone:
                    person_info['phone'] = profile_phone.get_text(strip=True)
                else:
                    person_info['phone'] = 'No Info'

                person_card = f'''Name         : {person_info["name"]}
Address      : {person_info["address"]}
Phone number : {person_info["phone"]}
------------------------------'''

                result_parts.append('\n' + person_card)
                print(person_card)

        return ''.join(result_parts)

    else:
        print('No matches found')


def main():
    parser = argparse.ArgumentParser(description="OSINT tool to search for information by IP address, full name, or username.")
    parser.add_argument("-fn", "--full-name", dest="full_name", help="Search with full name")
    parser.add_argument("-ip", "--ip-address", dest="ip_address", help="Search with IP address")
    parser.add_argument("-u", "--username", help="Search with username")
    args = parser.parse_args()

    actions = [
        (args.ip_address,  "ip address", get_ip_info,  False),
        (args.full_name,   "full name",  getnameinfo,  True),
        (args.username,    "username",   get_user_info,False),
    ]

    for value, label, func, echo in actions:
        if value:
            print(f'\nSeaching for {label}: {value}\n')
            time.sleep(0.5)
            data = func(value)
            if data:
                if echo:
                    print(data)
                save_data(data)
            break
    else:
        print("Please provide an option. Use -h or --help for usage information.")

def save_data(data):
    n, filename = 0, "result.txt"
    while os.path.exists(filename):
        n += 1
        filename = f"result{n}.txt"
    with open(filename, "w") as f:
        f.write(data)
    print(f'\nData saved in {filename}')

if __name__ == "__main__":
    main()