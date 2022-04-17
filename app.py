from flask import Flask, request, render_template
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)


app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def my_form_post():
    keywords = request.form['keywords']

    location = request.form['location']

    PATH = "/Users/williamli/Documents/GitHub/grand-and-toy/chromedriver-2"
    driver = webdriver.Chrome(PATH)

    driver.get("https://www.google.ca/")

    search = driver.find_element(by=By.CLASS_NAME, value="gLFyf")
    search_string = "\"Location * {}\" \"{}\" site:linkedin.com/in OR site:linkedin.com/pub -intitle:profiles".format(location, keywords)
    search.send_keys(search_string) 
    search.send_keys(Keys.RETURN)

    driver.implicitly_wait(30)

    result = {}

    for page in range(10):

        list_elements = driver.find_elements_by_class_name("jtfYYd")

        for item in list_elements:
            title = item.find_element_by_class_name("LC20lb").text
            desc = item.find_element_by_class_name("VwiC3b").text
            result[title] = desc
        #descs = [descriptions.append(element.find_element_by_class_name("VwiC3b").text) for element in list_elements]
        #descriptions.append(descs)
        try:
            link = driver.find_element_by_link_text("Next")
            link.click()
        except:
            break


    return render_template("results.html", result=result)

app.run(debug=True, host='0.0.0.0', port=8000)