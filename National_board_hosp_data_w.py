#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 14:23:35 2024

@author: swetha
"""

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# Setup WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.implicitly_wait(10)
driver.get("https://accr.natboard.edu.in/online_user/frontpage.php?v=4")
driver.maximize_window()

def select_options():
    select_state = Select(driver.find_element(By.ID, "mystate"))
    select_state.select_by_visible_text("All States")

    select_hosp = Select(driver.find_element(By.ID, "hosp"))
    select_hosp.select_by_visible_text("All Accredited Hospitals")

    select_spec = Select(driver.find_element(By.ID, "specialty"))
    select_spec.select_by_visible_text("All DNB, DrNB & FNB Specialties")

def save_data_to_excel(hosp_name, management, comp_name, address, website, total_beds):
    data = {
        "Hospital Name": hosp_name,
        "Management": management,
        "Company Name": comp_name,
        "Address": address,
        "Website_link": website,
        "Total Beds": total_beds
    }
    df = pd.DataFrame(data)
    df.to_excel(r'/Users/swetha/Documents/Work/NBE/NBE_hospital_data.xlsx', index=False)

# Initial selection
select_options()

# Trigger search
driver.find_element(By.ID, "search").click()
time.sleep(5)

# Find all hospital links
hospital_elements = driver.find_elements(By.XPATH, "//td[1]/a[contains(@target, '_blank')]")

# List to store unique links
partial_links = []

# Collect unique links
for elem in hospital_elements:
    full_text = elem.get_attribute("innerHTML")
    dynamic_text = full_text.split('<br>')[0].strip()
    partial_links.append(dynamic_text)

hosp_name, management, comp_name, address, website, total_beds = [], [], [], [], [], []

# Iterate through each hospital link
for link_text ,link_name in hospital_elements[1:], partial_links[1:]:
    try:
        # # Get the hospital link
        # hosp_element = WebDriverWait(driver, 10).until(
        #     EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, link_text))
        # )
        hosp_url = link_text.get_attribute('href')
        name = link_name
        print(name)
        # Open link in a new tab
        driver.execute_script("window.open(arguments[0]);", hosp_url)
        driver.switch_to.window(driver.window_handles[1])
        
        # Scrape hospital data
        hos_name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@align = 'center']/tbody/tr[2]/td[3]"))
        ).text
        manage = driver.find_element(By.XPATH, "//*[@align = 'center']/tbody/tr[3]/td[3]").text
        co_name = driver.find_element(By.XPATH, "//*[@align = 'center']/tbody/tr[4]/td[3]").text
        add = driver.find_element(By.XPATH, "//*[@align = 'center']/tbody/tr[6]/td[3]").text
        elem = driver.find_elements(By.XPATH, "//*[@align = 'center']/tbody/tr[7]/td[3]/a")
        web = elem[0].text if elem else 'N/A'
        tot_bed = driver.find_element(By.XPATH, "//*[@align = 'center']/tbody/tr[9]/td[3]").text
        
        hosp_name.append(hos_name)
        management.append(manage)
        comp_name.append(co_name)
        address.append(add)
        website.append(web)
        total_beds.append(tot_bed)
        
        # Close the current tab and switch back to the main tab
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        
    except Exception as e:
        print(f"An error occurred with {link_text}: {str(e)}", 'LINK:' ,hosp_url,name)
        save_data_to_excel(hosp_name, management, comp_name, address, website, total_beds)
        
        # Close the current tab and switch back to the main tab if not already done
        if len(driver.window_handles) > 1:
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        continue  # Move to the next link

# Final save of data
save_data_to_excel(hosp_name, management, comp_name, address, website, total_beds)

# Close the browser
driver.quit()

print("Data scraping completed and saved to hospitals_data.xlsx.")
