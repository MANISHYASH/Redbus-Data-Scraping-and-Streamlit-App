import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    driver.get('https://www.redbus.in/online-booking/ktcl/?utm_source=rtchometile')
    driver.execute_script("document.body.style.zoom='80%'")
    return driver

def collect_routes(driver):
    list_route = []
    elements = WebDriverWait(driver, 20).until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'a[class="route"]'))
    )
    for element in elements:
        link = element.get_attribute('href')
        list_route.append(link)
    return list_route

def go_to_page(driver, page_number):
    try:
        pagination_table = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div[4]/div[12]'))
        )
        page_buttons = pagination_table.find_elements(By.CLASS_NAME, 'DC_117_pageTabs')
        page_button = page_buttons[page_number - 1]
        driver.execute_script("arguments[0].scrollIntoView(true);", page_button)
        driver.execute_script("arguments[0].click();", page_button)
        return True
    except Exception as e:
        print(f"Failed to click on page {page_number} button: {e}")
        return False

def extract_bus_details(driver):
    wait = WebDriverWait(driver, 20)
    route_name_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'h1[class="D136_h1"]')))
    route_name = route_name_element.text
    route_link = driver.current_url

    bus_names_list = [bus_name.text for bus_name in wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="travels lh-24 f-bold d-color"]')))]
    bus_types_list = [bus_type.text for bus_type in wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="bus-type f-12 m-top-16 l-color evBus"]')))]
    departing_times_list = [departing_time.text for departing_time in wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="dp-time f-19 d-color f-bold"]')))]
    durations_list = [duration.text for duration in wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="dur l-color lh-24"]')))]
    reaching_times_list = [reaching_time.text for reaching_time in wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="bp-time f-19 d-color disp-Inline"]')))]
    star_ratings_list = [star_rating.text for star_rating in wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="rating-sec lh-24"]')))]
    prices_list = [price.text for price in wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="fare d-block"]')))]
    seats_available_list = [seats.text for seats in wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="seat-left m-top-30"]')))]

    min_length = min(len(bus_names_list), len(bus_types_list), len(departing_times_list), 
                     len(durations_list), len(reaching_times_list), len(star_ratings_list), len(prices_list), 
                     len(seats_available_list))

    bus_details = [
        {
            'Route Name': route_name,
            'Route Link': route_link,
            'Bus Name': bus_names_list[i],
            'Bus Type': bus_types_list[i],
            'Departing Time': departing_times_list[i],
            'Duration': durations_list[i],
            'Reaching Time': reaching_times_list[i],
            'Star Rating': star_ratings_list[i],
            'Price': prices_list[i],
            'Seats Available': seats_available_list[i]
        }
        for i in range(min_length)
    ]
    
    return bus_details

def scroll_and_extract(driver, retries=3):
    for attempt in range(retries):
        try:
            wait = WebDriverWait(driver, 20)

            # Check if the second element is present by attempting to find it
            try:
                ele_clc2 = driver.find_element(By.XPATH, '//*[@id="result-section"]/div[2]/div/div[2]/div/div[4]/div[2]')
                ele_clc2.click()
            except:
                pass

            # Wait for the first element to be clickable before clicking
            ele_clc1 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="result-section"]/div[1]/div/div[2]/div/div[4]/div[2]')))
            ele_clc1.click()

            # Scroll down to load more content
            while True:
                last_height = driver.execute_script("return document.body.scrollHeight")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)  # Adjust sleep time as needed
                
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            return extract_bus_details(driver)
        
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(2)  # Wait before retrying
    return []

def main():
    driver = setup_driver()

    all_routes = []
    page_number = 1

    while True:
        all_routes.extend(collect_routes(driver))
        page_number += 1
        if not go_to_page(driver, page_number):
            break
        time.sleep(2)  # Add a delay to allow the next page to load

    all_bus_details = []

    # To avoid duplicates, remove unnecessary last entries
    if len(all_routes) > 3:
        all_routes = all_routes[:-3]

    for link in all_routes:
        driver.get(link)
        bus_details = scroll_and_extract(driver)
        if bus_details:
            all_bus_details.extend(bus_details)

    # Write data to a CSV file with auto-incremented ID
    with open('KTCL.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['ID', 'Route Name', 'Route Link', 'Bus Name', 'Bus Type', 'Departing Time', 'Duration', 'Reaching Time', 'Star Rating', 'Price', 'Seats Available'])
        for i, bus_detail in enumerate(all_bus_details, start=1):
            csvwriter.writerow([i, bus_detail['Route Name'], bus_detail['Route Link'], bus_detail['Bus Name'], bus_detail['Bus Type'], bus_detail['Departing Time'], bus_detail['Duration'], bus_detail['Reaching Time'], bus_detail['Star Rating'], bus_detail['Price'], bus_detail['Seats Available']])

    driver.quit()

if __name__ == "__main__":
    main()
