from selenium import webdriver
from bs4 import BeautifulSoup
import time
import os

def fetch_html(url):

        browser = webdriver.Chrome()
        browser.get(url)

        # Scroll down to bottom of page
        src_updated = browser.page_source
        src = ""
        while src != src_updated:
            time.sleep(1)
            src = src_updated
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            src_updated = browser.page_source
        html_source = browser.page_source
        browser.quit()

        return html_source

def crawlQuestionsFromTopic(topic_urls):

    question_urls = []
    question_strings = []

    for url in topic_urls:

        html = fetch_html(url)

        # Parse html for questions
        soup = BeautifulSoup(html, 'html.parser')
        question_links = soup.find_all('a', class_='question_link')
        question_strings += [q.find('span', class_='ui_qtext_rendered_qtext').text for q in question_links]
        question_urls += [url+q['href'] for q in question_links]

        print(url, len(question_urls), "questions.")

    return question_urls, question_strings

# Crawl a question URL and save data into a csv file
def crawlQuestionData(question_urls):

    for url in question_urls:

        html = fetch_html(url)

        # Parse html for question data
        #TODO

def main():

    ## Add more topic pages to crawl
    topics =    ['https://www.quora.com/topic/Image-Recognition', 
                'https://www.quora.com/topic/Deep-Learning', 
                'https://www.quora.com/topic/Computer-Vision']

    questions = crawlQuestionsFromTopic(topics)
    print("Collected a question total of", len(questions))

if __name__ == "__main__": main()
