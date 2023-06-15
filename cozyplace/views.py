from django.shortcuts import render

import kss
import numpy as np

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


def make_driver():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)

    return webdriver.Chrome(
        options=chrome_options, service=Service(ChromeDriverManager().install())
    )


def find_diff(driver, old_content, new_content):
    url = "https://www.diffchecker.com/"

    init_page_btn_selector = ".react-responsive-modal-closeButton"

    old_content_input_xpath = '//*[@id="__next"]/div/div/div[2]/div/div/div/div/div/div[2]/div/form/div[1]/div[1]/div[2]/div/div[2]/div[2]/div'
    new_content_input_xpath = '//*[@id="__next"]/div/div/div[2]/div/div/div/div/div/div[2]/div/form/div[1]/div[2]/div[2]/div/div[2]/div[2]/div'

    driver.get(url)
    driver.find_element(By.CSS_SELECTOR, init_page_btn_selector).click()

    old_content_input = driver.find_element(
        By.XPATH,
        old_content_input_xpath,
    )
    old_content_input.click()
    old_content_input.send_keys(old_content)

    new_content_input = driver.find_element(
        By.XPATH,
        new_content_input_xpath,
    )
    new_content_input.click()
    new_content_input.send_keys(new_content)

    diff_btn_selector = "#__next > div > div > div.jsx-1524633858.page_app__I2ou8 > div > div > div > div > div > div.jsx-1193114133.diff-checker > div > form > div.jsx-782972875.find-difference-button-container > button"
    diff_btn = driver.find_element(By.CSS_SELECTOR, diff_btn_selector)
    diff_btn.click()


def extract_data(driver):
    deleted_list = driver.find_elements(By.CSS_SELECTOR, ".diff-chunk-removed")
    inserted_list = driver.find_elements(By.CSS_SELECTOR, ".diff-chunk-inserted")
    deleted_texts = []
    inserted_texts = []
    for i in deleted_list:
        deleted_texts.append(i.text)
    for j in inserted_list:
        inserted_texts.append(j.text)
    old_and_new = []
    for old, new in zip(deleted_list, inserted_list):
        old_and_new.append({"old": old.text, "new": new.text})
    return [deleted_texts, inserted_texts, old_and_new]


def diff(old_content, new_content):
    driver = make_driver()
    find_diff(driver, old_content, new_content)
    elements = extract_data(driver)
    driver.quit()

    return elements


def check_spacing1(sentence):
    new_sentence = "타인을 아는 사람은 지혜롭다."
    return new_sentence


def check_spacing2(sentence):
    new_sentence = "반면 자신을 아는 사람은 현명하다."
    return new_sentence


def check_spacing3(sentence):
    new_sentence = "타인을 이기는 사람은 힘이 있다."
    return new_sentence


def check_spacing4(sentence):
    new_sentence = "반면 자신을 이기는 사람은 강하다."
    return new_sentence


def lets_split_sentences(paragraphs):
    sentences = []
    for i in paragraphs:
        sentences.extend(kss.split_sentences(i, backend="mecab"))
    return sentences


def split_paragraphs(old_content):
    paragraphs = old_content.split("\r\n")
    return paragraphs


def processing_for_result(old_content, old):
    span_content = old_content[:]

    start = 0
    for i in old:
        result = span_content.find(i, start)
        index = len(i)
        start = result + index + 13
        span = "<span>" + i + "</span>"
        span_content = span_content[:result] + span + span_content[(result + index) :]

    span_content = span_content.replace("\r\n", "<br />")
    return span_content


def index(request):
    if request.method == "POST":
        old_content = request.POST.get("notebook")  # 작성한 글 저장
        paragraphs = split_paragraphs(old_content)  # 작성한 글에서 문단 나누기
        new_paragraphs1 = []
        new_paragraphs2 = []
        # 문단 순회. 나중에 구현 예정

        ## 문장 분리 후 순회
        old_sentences1 = kss.split_sentences(paragraphs[0])
        ### 띄어쓰기 검사 진행 후 저장
        new_paragraphs1.append(check_spacing1(old_sentences1[0]))
        new_paragraphs1.append(check_spacing2(old_sentences1[1]))
        ## 새로운 문단으로 변경
        new_paragraphs1 = " ".join(new_paragraphs1)

        ## 문장 분리 후 순회
        old_sentences2 = kss.split_sentences(paragraphs[1])
        ### 띄어쓰기 검사 진행 후 저장
        new_paragraphs2.append(check_spacing3(old_sentences2[0]))
        new_paragraphs2.append(check_spacing4(old_sentences2[1]))
        ## 새로운 문단으로 변경
        new_paragraphs2 = " ".join(new_paragraphs2)

        new_content = new_paragraphs1 + "\n" + new_paragraphs2
        old, new, old_and_new = diff(old_content, new_content)
        print(old)
        print(new)
        span_content = processing_for_result(old_content, old)
        post_data = {
            "old": old,
            "new": new,
            "old_and_new": old_and_new,
            "span_content": span_content,
        }
        return render(request, "cozyplace/post.html", post_data)
    elif request.method == "GET":
        return render(request, "cozyplace/pre.html")


def result(request):
    return render(request, "cozyplace/post.html")


# Create your views here.
