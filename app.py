import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Change these paths as necessary
SCREENSHOTS_FOLDER = r"C:\Users\KAUSHAL KUMAR\Pictures\Screenshots"
CHROME_DRIVER_PATH = r'C:\Users\KAUSHAL KUMAR\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe'

class NewPhotoHandler(FileSystemEventHandler):
    def __init__(self, driver):
        self.driver = driver
        self.last_file = None
    
    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            new_file = event.src_path
            if new_file != self.last_file:
                self.last_file = new_file
                self.share_photo(new_file)

    def share_photo(self, file_path):
        try:
            wait = WebDriverWait(self.driver, 30)
            
            # Click the new attachment button with the updated selector
            attach_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'span[data-icon="attach-menu-plus"]')))
            attach_btn.click()
            time.sleep(1)
            print("Attachment button found and clicked")

            # Click the Photos & Videos button
            photos_videos_btn = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')))
            photos_videos_btn.send_keys(file_path)
            time.sleep(2)
            print("Photos & Videos input found and file path sent")

            # Send the photo
            send_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'span[data-icon="send"]')))
            send_btn.click()
            time.sleep(1)
            print("Send button found and clicked")

            print(f"Shared photo: {file_path}")
        except Exception as e:
            print(f"Failed to share photo: {file_path}. Error: {e}")

def main():
    # Set up Selenium WebDriver
    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service)
    driver.get('https://web.whatsapp.com')
    time.sleep(15)  # Time to scan the QR code

    event_handler = NewPhotoHandler(driver)
    observer = Observer()
    observer.schedule(event_handler, SCREENSHOTS_FOLDER, recursive=False)
    observer.start()

    print("Monitoring folder for new photos...")
    try:
        while True:
            time.sleep(5)  # Check every 5 seconds
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    driver.quit()

if __name__ == "__main__":
    main()
