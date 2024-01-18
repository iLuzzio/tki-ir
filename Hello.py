import streamlit
from newspaper import Article
import requests

streamlit.set_page_config(page_title='KASIH NAMA WEB')

apiKey = 'd9addde433a74562aa80be87342bb984'

#Berita teratas indonesia
def berita_teratas():
    url = 'https://newsapi.org/v2/top-headlines'
    params = {
        'country': 'id',
        'apiKey': apiKey,
        'pageSize': 25,
        'sortBy' : 'relevancy'
    }
    response = requests.get(url, params=params)
    news_list = response.json().get('articles', [])
    return news_list
#Mencari berita
def cari_berita(topic):
    url = 'https://newsapi.org/v2/everything'
    params = {
        'q': topic,
        'language': 'id',
        'apiKey': apiKey,
        'pageSize': 25
    }
    response = requests.get(url, params=params)
    news_list = response.json().get('articles', [])
    return news_list

def display_news(news_list, articles_per_page):
    c = 0
    for news in news_list:
        c += 1
        streamlit.write('**({}) {}**'.format(c, news['title']))
        news_data = Article(news['url'])
        try:
            news_data.download()
            news_data.parse()
            news_data.nlp()
        except Exception as e:
            print(e)
        with streamlit.expander(news['title']):
            if news['author']:
                streamlit.write(news['author'])
            streamlit.markdown(
                '''<h6 style="text-align: justify;">{}</h6>'''.format(news['description']),
                unsafe_allow_html=True
            )
            if news['urlToImage']:
                streamlit.image(news['urlToImage'])
            streamlit.markdown("[Baca Selengkapnya {}...]({})".format(news['source']['name'], news['url']))
        streamlit.success("Tanggal Terbit: " + news['publishedAt'])
        if c >= articles_per_page:
            break

def run():
    streamlit.title("KASIH NAMA WEB")
    category = ['Pilihan Kategori', 'Artikel Teratas', 'Cari Artikel']
    category_options = streamlit.selectbox('Pilih Kategori', category)

    if category_options == category[0]:
        streamlit.warning('Untuk mendapatkan Artikel pilih salah satu kategori')

    elif category_options == category[1]:
        streamlit.subheader(" Berikut merupakan beberapa artikel teratas ")
        articles_per_page = streamlit.slider("Jumlah artikel yang ditampilkan", min_value=5, max_value=25, step=5)
        news_list = berita_teratas()
        display_news(news_list, articles_per_page)

    elif category_options == category[2]:
        user_topic = streamlit.text_input("Cari Artikel")
        articles_per_page = streamlit.slider("Jumlah artikel yang ditampilkan", min_value=5, max_value=25, step=5)
        
        if streamlit.button("Cari") and user_topic != '':
            news_list = cari_berita(topic=user_topic)
            if news_list:
                streamlit.subheader(f"Berikut artikel yang berkaitan dengan {user_topic.capitalize()}")
                display_news(news_list, articles_per_page)
            else:
                streamlit.error(f"Artikel TIDAK Ditemukan: {user_topic}")
        else:
            streamlit.warning("Ketikan artikel yang ingin dicari!")

if __name__ == "__main__":
    run()
