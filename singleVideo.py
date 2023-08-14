from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Specify the path to ChromeDriver executable
chromedriver_path = 'C:/Users/user/Downloads/chromedriver_win32/chromedriver.exe'  # Update this with the correct path

# Create a Service object
service = Service(chromedriver_path)

# Initialize Chrome WebDriver
driver = webdriver.Chrome(service=service)

# Open a specific TikTok video using its URL
video_url = 'https://www.tiktok.com/@rihanna/video/7266148302045973790'  # Replace with the actual video URL
driver.get(video_url)

# Wait for the video page to load (you can adjust the sleep duration as needed)
time.sleep(5)

try:
    # Wait for the follower count element to be present
    follower_count_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'span.follower-count'))
    )

    # Scrape information from the video
    follower_count = follower_count_element.text

    # Use similar explicit waits for other elements
    # For example:
    # likes_element = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.CSS_SELECTOR, 'span.like-count'))
    # )

    # Continue scraping other details...

    # Print the scraped details
    print("Video URL:", video_url)
    print("Follower Count:", follower_count)
    # Print other details...

except Exception as e:
    print("Error:", e)

# After scraping, you can close the WebDriver
driver.quit()
