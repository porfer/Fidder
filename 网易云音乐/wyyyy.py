import time
from urllib.request import urlretrieve
import requests
from lxml import etree

def get_page(url):
    headers = {
        'Host': 'music.163.com',
        'Referer': 'https://music.163.com/',
        'User-Agent': 'Mozilla/5.0(Windows NT 10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/67.0.3396.99Safari/537.36'
    }
    res = requests.get(url, headers=headers).text
    with open('yinyue.html','w',encoding='utf-8') as fw:
        fw.write(res)
    tree = etree.HTML(res)
    music_dict = {}

    a_list = tree.xpath('//div[@id="song-list-pre-cache"]/ul[@class="f-hide"]/li/a')
    for a in a_list:
        music_id = a.xpath('.//@href')[0].strip("/song?id=")
        music_name = a.xpath('./text()')[0]
        music_dict[music_id] = music_name
    return music_dict

def download_song(music_dict):
    for song_id in music_dict:
        song_url = "http://music.163.com/song/media/outer/url?id=%s.mp3" % song_id
        path = "./音乐/%s.mp3" % music_dict[song_id]
        urlretrieve(song_url, path)
        time.sleep(1)
        print("正在下载%s" % music_dict[song_id])

def main():
    id = int(input('请输入歌单id：'))
    url = 'https://music.163.com/playlist?id={}'.format(id)
    music_dict = get_page(url)
    download_song(music_dict)

if __name__ == '__main__':
    main()
