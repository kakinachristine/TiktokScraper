import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time


# Specify the path to the ChromeDriver executable
chromedriver_path = 'C:/Users/user/Downloads/chromedriver_win32/chromedriver.exe'  # Update this with the correct path
# Create a Service object
service = Service(chromedriver_path)

# Initialize Chrome WebDriver
driver = webdriver.Chrome(service=service)

# Open the TikTok Explore page for the "relationships" tag
driver.get('https://www.tiktok.com/tag/relationships')

# Wait for the page to load (you can adjust the sleep duration as needed)
time.sleep(5)

# Scroll down to load more videos (adjust the number of scrolls based on the page design)
for _ in range(5):  # Scroll down 5 times
    driver.execute_script('window.scrollBy(0, window.innerHeight)')  # Scroll down by window height
    time.sleep(2)  # Wait for the page to load after scrolling

# Scrape information from videos
video_elements = driver.find_elements(By.XPATH, "//a[contains(@class, 'video-feed-item-wrapper')]")

# Create a list to store video details
video_details = []

# Create a dictionary to keep track of video counts per user
user_video_counts = {}

for video_element in video_elements:
    try:
        name = video_element.find_element(By.CSS_SELECTOR, 'p.author-uniqueId').text
        if name not in user_video_counts:
            user_video_counts[name] = 0

        if user_video_counts[name] < 2:  # Limit to scraping 2 videos from each user
            user_video_counts[name] += 1
            video_link = video_element.get_attribute('href')
            follower_count_element = video_element.find_element(By.CSS_SELECTOR, 'span.follower-count')
            follower_count = follower_count_element.text
            likes_element = video_element.find_element(By.CSS_SELECTOR, 'span.like-count')
            likes = likes_element.text
            user_bio_element = video_element.find_element(By.CSS_SELECTOR, 'p.author-uniqueId ~ p.subtitle')
            user_bio = user_bio_element.text
            video_title_element = video_element.find_element(By.CSS_SELECTOR, 'h2.video-feed-item-title')
            video_title = video_title_element.text

            # Append video details to the list
            video_details.append([video_link, name, user_bio, video_title, follower_count, likes])
    except Exception as e:
        print("Error:", e)

# After scraping, you can close the WebDriver
driver.quit()

# Write video details to a CSV file
csv_filename = 'tiktok_relationships_videos.csv'
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Video Link', 'User ID', 'User Bio', 'Video Title', 'Follower Count', 'Likes'])
    csv_writer.writerows(video_details)

print(f'{len(video_details)} video details saved to {csv_filename}')