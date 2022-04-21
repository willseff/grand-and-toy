from flask import Flask, request, render_template
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time
import os
import numpy as np
import pandas as pd



app = Flask(__name__)

@app.route('/')
def my_form():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)

    return render_template('index.html')

@app.route('/', methods=['POST'])
def my_form_post():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)
    
    keywords = request.form['keywords']

    location = request.form['location']

    driver.get("https://www.google.ca/")

    search = driver.find_element(by=By.CLASS_NAME, value="gLFyf")
    search_string = "\"Location * {}\" \"{}\" site:linkedin.com/in OR site:linkedin.com/pub -intitle:profiles".format(location, keywords)
    search.send_keys(search_string) 
    search.send_keys(Keys.RETURN)

    result = {}

    for page in range(10):

        list_elements = driver.find_elements_by_class_name("jtfYYd")

        for item in list_elements:
            title = item.find_element_by_class_name("LC20lb").text
            desc = item.find_element_by_class_name("VwiC3b").text
            result[title] = desc
        try:
            link = driver.find_element_by_link_text("Next")
            link.click()
        except:
            break

    df = pd.DataFrame(result.items(), columns=['Name', 'Description'])

    # randomly generated prediction values
    randoms = np.random.randint(10000, size=len(df))/10000
    df['Target'] = randoms

    df = df.sort_values(by="Target",ascending=False)


    return render_template('results.html',  tables=[df.to_html(classes="content-table", index_names=False, justify="left")])


def main():
    app.run(host='127.0.0.1', debug=True, port=8080, threaded=True)


if __name__ == '__main__':
    main()



