# ■wikimediaからのレスポンスを可読性のある文章に整形するコード
# 1. リクエストしたい単語を引数に指定
# 2. リクエストをする
# 3. 整形する(printをする)
import sys
from bs4 import BeautifulSoup
from urllib import request
import urllib.parse  # URLエンコード用ライブラリ
import xml.etree.ElementTree as ET
import re
import regex

def GetResponse(word):
    url = 'https://ja.wikipedia.org/w/api.php?format=xml&action=query&prop=revisions&titles={}&rvprop=content'
    # URLエンコードされた検索語
    wordencoded = urllib.parse.quote(word)
    # URLエンコードをした検索語をURLの中に組み込む
    url = url.format(wordencoded)
    # print(url)
    response = request.urlopen(url)
    soup = BeautifulSoup(response)
    # 流石にrevタグは複数ヒットしないだろうという予想のもと...
    meaning = soup.find('rev').contents[0]
    return meaning


def sharping(meaning):
    returntext = ''
    # 漢字の正規表現を含む(https://note.nkmk.me/python-re-regex-character-type/)
    sectionexp = r'==\s(\p{Script=Han}+)+・*(\p{Script=Han}+)*\s=='
    htmltagexp = r'<("[^"]*"\|\'[^\']*\'|[^\'">])*>'
    # # 太文字表現(カタカナ)
    # boldkatakanaexp = r'\'\'\'[\u30A1-\u30FF]+\'\'\''
    # # 太文字表現(ひらがな)
    # boldhiraganaexp = r'\'\'\'[\u3041-\u309F]+\'\'\''
    # # 太文字表現(漢字)
    # boldkanjiexp = r'\'\'\'(\p{Script=Han}+)+・*(\p{Script=Han}+)*\'\'\''
    # =*=*=*=*=*=*整形=*=*=*=*=*=*
    # ひとまず改行を全て無くす
    meaning = str(meaning)
    meaning = meaning.replace('\r', '').replace('\n', '').replace('\r\n', '')
    #「 == 概要 ==」みたいのを消す
    meaning = regex.sub(sectionexp, '', meaning)
    # htmlタグが含まれているので削除する
    meaning = regex.sub(htmltagexp, '', meaning)
    # シングルクオーテーションを削除
    meaning = meaning.replace('\'', '')
    # # 太文字表現(カタカナ)
    # meaning = regex.sub(boldkatakanaexp, '', meaning)
    # # 太文字表現(ひらがな)
    # meaning = regex.sub(boldhiraganaexp, '', meaning)
    # # 太文字表現(漢字)
    # meaning = regex.sub(boldkanjiexp, '', meaning)

    # =*=*=*=*=*=*整形終了=*=*=*=*=*=*
    lines = meaning.split('。')
    # 最初の３行分のみ返却する(多分最初の３行でなんとく意味わかるでしょ、という目論見のもとw)
    returntext = lines[0] + '\n' + lines[1] + '\n' + lines[2]
    return returntext


if __name__  == '__main__':
    shapedwordmeaning = ''
    print('注意!!引数に調べたい単語を指定!!')
    word = sys.argv[1]
    meaning = GetResponse(word)
    shapedwordmeaning = sharping(meaning)
    print(shapedwordmeaning)
