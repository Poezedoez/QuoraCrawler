from selenium import webdriver
from bs4 import BeautifulSoup
import time
import os
import pandas as pd
from collections import defaultdict

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

    questions = {'question_urls':[], 'question_strings':[]}

    for topic_url in topic_urls:

        html = fetch_html(topic_url)

        # Parse html for questions
        soup = BeautifulSoup(html, 'html.parser')
        question_blocks = soup.find_all('div', {'class': 'main_feed singleton_bundle'})
        questions['question_strings'] += [q.find('span', class_='ui_qtext_rendered_qtext').text for q in question_blocks]
        questions['question_urls'] += [topic_url + q.find('a', class_='question_link')['href'] for q in question_blocks]

    return questions

def crawlQuestionData(question_urls):

    for url in question_urls:

        html = fetch_html(url)

        # Parse html for question data, e.g. answer string, users voted etc.
        #TODO

def remove_duplicates(dataframe, column='question_strings'):
    '''remove duplicate rows in the data by finding duplicates
    in the given column of unique values'''

    duplicate_entries = []
    duplicates = set()
    for i, value in enumerate(dataframe[column]):
        if value in duplicates:
            duplicate_entries.append(i)
        duplicates.add(value)

    return dataframe.drop(duplicate_entries)


def main():

    ## Add more topic pages to crawl
    topics =    ['https://www.quora.com/topic/Image-Recognition', 
                'https://www.quora.com/topic/Deep-Learning', 
                'https://www.quora.com/topic/Computer-Vision',
                'https://www.quora.com/topic/Artificial-Neural-Networks',
                'https://www.quora.com/topic/Convolutional-Neural-Networks-CNN',
                'https://www.quora.com/topic/Long-Short-term-Memory',
                'https://www.quora.com/topic/Classification-machine-learning',
                'https://www.quora.com/topic/Naive-Bayes',
                'https://www.quora.com/topic/Bayesian-Inference',
                'https://www.quora.com/topic/Probabilistic-Graphical-Models',
                'https://www.quora.com/topic/Convex-Optimization']

    questions = crawlQuestionsFromTopic(topics)
    questions_df = pd.DataFrame(questions)
    questions_df = remove_duplicates(questions_df)
    questions_df.to_csv('questions.csv')
    print("Crawled {0} questions from {1} different topic pages.".format(questions_df.shape[0], len(topics)))



if __name__ == "__main__": main()
