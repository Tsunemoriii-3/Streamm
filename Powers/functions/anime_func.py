import calendar
from traceback import format_exc
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup
from lxml import html

from Powers import LOGGER
from Powers.utils.strings import ani_info_string, char_info_string

HEADERS = (
    {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \ (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
        'Accept-Language': 'en-US, en;q=0.5'
    }
)


anime_query = """query ($id: Int,$search: String) {
    Page (perPage: 10) {
        media (id: $id, type: ANIME,search: $search) {
            id
            title {
                romaji
                english
                native
            }
            type
            format
            status
            description (asHtml: false)
            episodes
            duration
            countryOfOrigin
            source            
            trailer{
                id
                site
            }
            genres
            tags {
                name
            }
            isAdult
            averageScore
            studios (isMain: true){
                nodes{
                    name
                }
            }
            nextAiringEpisode{
                episode
            }
            siteUrl
        }
    }
}"""


anime_query_id = """query ($id: Int) {
    Page (perPage: 10) {
        media (id: $id, type: ANIME) {
            id
            title {
                romaji
                english
                native
            }
            type
            format
            status
            description (asHtml: false)
            episodes
            duration
            countryOfOrigin
            source
            trailer{
                id
                site
            }
            genres
            tags {
                name
            }
            isAdult
            averageScore
            studios (isMain: true){
                nodes{
                    name
                }
            }
            nextAiringEpisode{
                episode
            }
            siteUrl
        }
    }
}"""

anime_char_query = """query ($id: Int, $search: String) {
    Page (perPage: 10) {
        media (id: $id, type: ANIME,search: $search) {
            id
            title {
                romaji
                english
                native
            }
            characters(sort: ID){
                edges{
                    node{
                        name{
                            first
                            middle
                            last
                        }
                    }
                    role
                }
            }
        }
    }
}"""

anime_char_query_id = """query ($id: Int) {
    Page (perPage: 10) {
        media (id: $id, type: ANIME) {
            id
            title {
                romaji
                english
                native
            }
            characters(sort: ID){
                edges{
                    node{
                        name{
                            first
                            middle
                            last
                        }
                    }
                    role
                }
            }
        }
    }
}"""


character_query = """query ($id: Int, $search: String) {
  	Page {
	    characters (id: $id, search: $search) {
            id
            name {
                full
        	    native
      	    }
          	image {
                large
            }
      	    description
            gender
            dateOfBirth {
                year
                month
                day
            }
            age
            bloodType
      	    siteUrl
            favourites
            media {
                nodes {
                    title {
                        romaji
                        english
                        native
                    }
                    type
                    format
                    siteUrl
                }
            }
        }
    }
}"""


def get_anime_results(query, page: int = 1, with_img: bool = False, top: bool = False):
    query, _id = get_anime_info(query, True)
    name = _id
    query = quote(query)
    to_return = {}

    xpath = "//*[@id='wrapper_bg']/section/section[1]/div/div[2]/ul"

    if not page or page == 1:
        url = f"https://anitaku.pe/search.html?keyword={query}"
    else:
        url = f"https://anitaku.pe/search.html?keyword={query}&page={page}"

    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        LOGGER.info(f"requests.get returned {response.status_code} while searching for anime")
        return to_return
    to_lxml = html.fromstring(response.content)

    try: 
        search_results = list(to_lxml.xpath(xpath)[0])
        num = 1
        if top:
            id_ = search_results[0].xpath(".//a/@href")[0].split("/")[-1]
            return id_
        total_page = list(to_lxml.xpath("//*[@id='wrapper_bg']/section/section[1]/div/div[1]/div/div/ul"))
        if not total_page:
            total_page = 1
        else:
            total_page = len(total_page[0])
        if not (search_results or total_page):
            return {}

        for result in search_results:
            if with_img:
                to_return[num] = {"title":result.xpath(".//a/@title")[0], "id":result.xpath(".//a/@href")[0].split("/")[-1], "image": result.xpath(".//img/@src")[0]}
            else:
                to_return[num] = {"title":result.xpath(".//a/@title")[0], "id":result.xpath(".//a/@href")[0].split("/")[-1], "totalPage": total_page, "query": name}
            num += 1

        return to_return
    except Exception as e:
        LOGGER.error(e)
        LOGGER.error(format_exc())
        return {}


def get_char_anime(query):
    url = "https://graphql.anilist.co"
    query = str(query)
    if query.strip().isnumeric():
        query = int(query.strip())
        variables = {"id": query}
        search = anime_char_query_id
    else:
        variables = {"search": query}
        search = anime_char_query
    response = requests.post(url, json={"query": search, "variables": variables})
    if response.status_code != 200:
        return None, None
    
    data = response.json()

    data = data["data"]["Page"]["media"][0]

    english_title = data["title"]["english"]
    if not english_title:
        english_title = data["title"]["romaji"]

    to_return = {}

    anime_name = english_title

    to_return["anime_name"] = anime_name
    num = 1
    for i in data["characters"]["edges"]:
        ndata = i["node"]["name"]
        full = ""
        if bool(ndata["last"]):
            full += ndata["last"]
            if bool(ndata["middle"]):
                full += f" {ndata['middle']}"
            if bool(ndata["first"]):
                full += f" {ndata['first']}"
        elif bool(ndata["first"]):
            full += ndata["first"]
            if bool(ndata["middle"]):
                full += f" {ndata['middle']}"
        
        role = i["role"]

        to_return[num] = {"name": full, "role": role}
        
        if num == 15:
            break
        num += 1

    return to_return

def get_trending_anime(page: int = 1, number: int = 10):
    url = f"https://anilist.co/search/anime/trending?page={page}&perPage={number}"
    
    res = requests.get(url)

    if res.status_code != 200:
        return None
    to_lxml = html.fromstring(res.content)
    
    xpath = "//*[@id='app']/div[3]/div/div/div[5]"
    
    data = list(list(to_lxml.xpath(xpath)[0]))

    txt = "Here are top 10 trending animes"

    to_return = {}
    num = 1
    for i in data:
        name = i.xpath("./a[2]/text()")
        id_ = i.xpath("./a[1]/@href")[0].split("/")[2]
        
        to_return[num] = {"id": id_, "name": name[0]}
        num += 1

    return to_return

def get_alltime_popular(page: int = 1, number: int = 10):
    url = f"https://anilist.co/search/anime/popular?page={page}&perPage={number}"
    
    res = requests.get(url)

    if res.status_code != 200:
        return None
    to_lxml = html.fromstring(res.content)
    
    xpath = "//*[@id='app']/div[3]/div/div/div[5]"
    
    data = list(list(to_lxml.xpath(xpath)[0]))

    txt = "Here are top 10 trending animes"


    to_return = {}
    num = 1
    for i in data:
        name = i.xpath("./a[2]/text()")
        id_ = i.xpath("./a[1]/@href")[0].split("/")[2]
        
        to_return[num] = {"id": id_, "name": name[0]}
        num += 1

    return to_return


def get_last_ep(anime_id):
    url = f"https://anitaku.pe/category/{anime_id}"
    xpath = "//*[@id='episode_page']"

    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        return "N/A"

    try:
        to_lxml = html.fromstring(response.content)

        last_ep = list(list(to_lxml.xpath(xpath))[0])[-1].xpath("./a/@ep_end")
        if last_ep:
            return int(last_ep[0])
        else:
            return "N/A"
    except:
        return "N/A"


def get_anilist_id(name):
    url = "https://graphql.anilist.co"
    variables = {"search": name}
    search_query = """query ($id: Int,$search: String) {
        Page (perPage: 1) {
            media (id: $id, type: ANIME,search: $search) {
                id
            }
        }
    }"""
    response = requests.post(url, json={"query": search_query, "variables": variables})
    if response.status_code != 200:
        return
    
    data = response.json()
    try:
        data = data["data"]["Page"]["media"][0]
        return data["id"]
    except:
        return

def get_country_flag(country: str) -> str:
    base = ord('🇦')
    emoji_flag = "".join(chr(base + ord(letter) - ord("A")) for letter in country)
    return emoji_flag

def get_anime_info(query, only_name: bool = False, only_description: bool = False):
    url = "https://graphql.anilist.co"
    query = str(query)
    if query.strip().isnumeric():
        query = int(query.strip())
        variables = {"id": query}
        search_query = anime_query_id
    else:
        variables = {"search": query}
        search_query = anime_query
    response = requests.post(url, json={"query": search_query, "variables": variables})
    if response.status_code != 200:
        return None, None
    
    data = response.json()
    try:
        data = data["data"]["Page"]["media"][0]
    except:
        return None, None
    english_title = data["title"]["english"]
    native_title = data["title"]["native"]
    if not english_title:
        english_title = data["title"]["romaji"]

    if only_name:
        return english_title, data["id"]

    synopsis = data["description"]

    if only_description:
        return synopsis[0:1020]

    flag = get_country_flag(data["countryOfOrigin"])
    name = f"**[{flag}] {english_title} ({native_title})**"

    anime_id = data["id"]
    score = data["averageScore"] if data["averageScore"] else "N/A"
    source = str(data["source"]).title() if data["source"] else "N/A"
    mtype = str(data["type"]).title() if data["type"] else "N/A"
    

    episodes = data["episodes"]
    if not episodes:
        try:
            episodes = data["nextAiringEpisode"]["episode"] - 1
        except:
            episodes = "N/A"

    duration = data["duration"] if data["duration"] else "N/A"
    status = str(data["status"]).title() if data["status"] else "N/A"
    format = str(data["format"]).title() if data["format"] else "N/A"
    genre = ", ".join(data["genres"]) if data["genres"] else "N/A"
    tags = ", ".join([i["name"] for i in data["tags"][:5]]) if data["tags"] else "N/A"
    studio = data["studios"]["nodes"][0]["name"] if data["studios"]["nodes"] else "N/A"
    siteurl = f"[Anilist Website]({data['siteUrl']})" if data["siteUrl"] else "N/A"
    isAdult = data["isAdult"]

    trailer = "N/A"
    if data["trailer"] and data["trailer"]["site"] == "youtube":
        trailer = f"[Youtube](https://youtu.be/{data['trailer']['id']})"

    response = requests.get(f"https://img.anili.st/media/{anime_id}").content
    banner = f"anime_{anime_id}.jpg"
    with open(banner, "wb") as f:
        f.write(response)

    info = ani_info_string.format(
        name=name,
        score=score,
        source=source,
        mtype=mtype,
        episodes=episodes,
        duration=duration,
        status=status,
        format=format,
        genre=genre,
        studio=studio,
        trailer=trailer,
        siteurl=siteurl,
        tags=tags,
        isAdult=isAdult,
    )

    return info, banner
    


def get_ep_fromat(anime_id, ep_number, is_dub: bool = False):
    if is_dub:
        formatted = f"{anime_id}-dub-episode-{ep_number}"
    else:
        formatted = f"{anime_id}-episode-{ep_number}"
    return formatted

def get_download_links(anime_id):
    auth_gogo = "PNyzv3XxTcIfmasWdA%2FIje%2FukCQ7dy4R9efTbnl0GXsF0AM5%2BkV6KmYC59zH229D3O2Bntyp2CpIJyM5Uc1D8Q%3D%3D"

    to_return = []
    try:
        ani_link = f"https://anitaku.pe/{anime_id}"
        animelink = requests.get(ani_link, cookies=dict(auth=auth_gogo))

        soup = BeautifulSoup(animelink.content, "html.parser")
        source_url = soup.find("div", {'class': 'cf-download'}).findAll('a')

        for i in source_url:
            to_return.append({"quality": f"{i.text.strip().split('x')[1]}p", "link": i['href']})

        return to_return
    except:
        return []

def is_dub_available(anime_id, ep_number):
    link = f"https://anitaku.pe/{anime_id}-dub-episode-{ep_number}"
    try:
        response = requests.get(link, headers=HEADERS)
        if response.status_code == 200:
            return True
        else:
            return False
    except:
        return False

def get_download_stream_links(name, ep_number, dub: bool = False):
    episode_format = get_ep_fromat(name, ep_number, dub)
    url = f"https://anitaku.pe/{episode_format}"

    to_return = {}

    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        return to_return
    to_lxml = html.fromstring(response.content)

    stream_xpath = "//*[@id='load_anime']/div/div/iframe/@src"

    download_xpath = "//*[@id='wrapper_bg']/section/section[1]/div[1]/div[2]/div[1]/div[4]/ul/li[1]/a/@href"
    down = get_download_links(episode_format)
    if not down:
        down = to_lxml.xpath(download_xpath)[0]

    to_return["stream"] = to_lxml.xpath(stream_xpath)[0]

    to_return["download"] = down

    return to_return

def get_date(data: dict) -> str:
    try:
        year = data["year"] or ""
        if not year and not data["month"]:
            return "N/A"
        day = data["day"]
        if 10 <= day % 100 <= 20:
            day = f"{day}th"
        else:
            day_dict = {1: "st", 2: "nd", 3: "rd"}
            day = f"{day}{day_dict.get(day % 10, 'th')}"

        month_name = calendar.month_name[int(data["month"])]
        return f"{day} {month_name} {year}"
    except:
        return "N/A"

def get_character_info(query, only_description: bool = False, pic_required: bool = True):
    url = "https://graphql.anilist.co"
    variables = {"search": query}
    response = requests.post(url, json={"query": character_query, "variables": variables})
    if response.status_code != 200:
        return None, None
    
    data = response.json()
    try:
        data = data["data"]["Page"]["characters"][0]
    except:
        return None, None
    description = data["description"].split("\n\n", 1)[0]
    if only_description:
        return description[0:1020]
    name = f"**{data['name']['full']} ({data['name']['native']})**"
    char_id = data["id"]

    gender = data["gender"] if data["gender"] else "N/A"
    date_of_birth = get_date(data["dateOfBirth"])
    age = data["age"] if data["age"] else "N/A"
    blood_type = data["bloodType"] if data["bloodType"] else "N/A"
    siteurl = f"[Anilist Website]({data['siteUrl']})" if data["siteUrl"] else "N/A"
    favorites = data["favourites"] if data["favourites"] else "N/A"

    cameo = data["media"]["nodes"][0] if data["media"]["nodes"] else {}
    if cameo:
        role_in = f"\n╰➢ **𝖱𝗈𝗅𝖾 𝖨𝗇:** [{cameo['title']['romaji']}]({cameo['siteUrl']})"
    else:
        role_in = ""

    if pic_required:
        response = requests.get(data["image"]["large"]).content
        banner = f"character_{char_id}.jpg"
        with open(banner, "wb") as f:
            f.write(response)

    info = char_info_string.format(
        name=name,
        gender=gender,
        date_of_birth=date_of_birth,
        age=age,
        blood_type=blood_type,
        favorites=favorites,
        siteurl=siteurl,
        role_in=role_in,
    )

    if not pic_required:
        return info
    return info, banner,