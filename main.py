from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
import csv

# Specify the path to the ChromeDriver executable
chromedriver_path = 'C:/Users/user/Downloads/chromedriver_win32/chromedriver.exe'  # Update this with the correct path

# Create a Service object
service = Service(chromedriver_path)

# Initialize Chrome WebDriver
driver = webdriver.Chrome(service=service)

# Now you can use the driver to interact with the browser
# Open the TikTok Explore page for topics related to relationships
driver.get('https://www.tiktok.com/@rihanna')

# Scroll down to load more videos (adjust the number of scrolls based on the page design)
for _ in range(5):  # Scroll down 5 times
    driver.execute_script('window.scrollBy(0, window.innerHeight)')  # Scroll down by window height
    time.sleep(2)  # Wait for the page to load after scrolling

# Scrape information from videos
video_elements = driver.find_elements("css selector", "a.video-feed-item-wrapper")

# Create a list to store video details
video_details = []

for video_element in video_elements[:100]:  # Limit to scraping 100 videos
    try:
        video_link = video_element.get_attribute('href')
        follower_count_element = video_element.find_element("css selector", 'span.follower-count')
        follower_count = follower_count_element.text
        comments_count_element = video_element.find_element("css selector", 'span.comment-count')
        comments_count = comments_count_element.text
        shares_element = video_element.find_element("css selector", 'span.share-count')
        shares = shares_element.text
        likes_element = video_element.find_element("css selector", 'span.like-count')
        likes = likes_element.text
        name = video_element.find_element("css selector", 'p.author-uniqueId').text
        name_id = video_element.find_element("css selector", 'a.strong.author').get_attribute('href')
        video_caption = video_element.find_element("css selector", 'div.video-caption').text

        # Append video details to the list
        video_details.append([video_link, follower_count, comments_count, shares, likes, name, name_id, video_caption])
    except Exception as e:
        print("Error:", e)

# After scraping, you can close the WebDriver
driver.quit()

# Write video details to a CSV file
csv_filename = 'tiktok_relationships_videos.csv'
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(
        ['Video Link', 'Follower Count', 'Comments Count', 'Shares', 'Likes', 'Name', 'Name ID', 'Video Caption'])
    csv_writer.writerows(video_details)

print(f'{len(video_details)} video details saved to {csv_filename}')