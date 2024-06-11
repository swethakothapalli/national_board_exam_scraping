#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 12:22:11 2024

@author: swetha
"""

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, TimeoutException, StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager

# Setup WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.implicitly_wait(10)
driver.get("https://accr.natboard.edu.in/online_user/frontpage.php?v=4")
driver.maximize_window()

select_state = Select(driver.find_element(By.ID, "mystate"))
select_state.select_by_visible_text("All States")

select_hosp = Select(driver.find_element(By.ID, "hosp"))
select_hosp.select_by_visible_text("All Accredited Hospitals")

select_spec = Select(driver.find_element(By.ID, "specialty"))
select_spec.select_by_visible_text("All DNB, DrNB & FNB Specialties")

# Trigger search
driver.find_element(By.ID, "search").click()
time.sleep(5)

table = driver.find_element(By.ID, "table_width")
data= pd.read_html(table.get_attribute('outerHTML'))[0]

file_path = f"/Users/swetha/Documents/Work/NBE/All_states_NBE.xlsx"
data.to_excel(file_path, index=False)
driver.refresh()

driver.quit()


