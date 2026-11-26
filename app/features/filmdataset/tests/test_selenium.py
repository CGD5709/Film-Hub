"""End-to-end browser tests for the filmdataset feature.

Driven by the selenium grid started by::

    docker compose -f docker/docker-compose.dev.yml up

Run with::

    rosemary test filmdataset --e2e

These tests run against the live application and the seeded development
database, not the test database.
"""

import uuid

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.file_detector import LocalFileDetector
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from tests.selenium_support import close_driver, get_host_for_selenium_testing, initialize_driver

pytestmark = pytest.mark.e2e


def _configure_file_detector(driver):
    if isinstance(driver, webdriver.Remote):
        driver.file_detector = LocalFileDetector()


def _scroll_and_click(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'instant'});", element)
    element.click()


def _log_in(driver, host, email="user1@example.com", password="1234"):
    driver.get(f"{host}/login")
    driver.find_element(By.NAME, "email").send_keys(email)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.ID, "submit").click()
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="/logout"]')))


def _sign_up_fresh_user(driver, host):
    unique_email = f"selenium_film_{uuid.uuid4().hex[:8]}@example.com"
    driver.get(f"{host}/signup/")
    driver.find_element(By.NAME, "name").send_keys("Selenium")
    driver.find_element(By.NAME, "surname").send_keys("Tester")
    driver.find_element(By.NAME, "email").send_keys(unique_email)
    driver.find_element(By.NAME, "password").send_keys("1234")
    driver.find_element(By.ID, "submit").click()
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="/logout"]')))


def test_filmdataset_index():
    driver = initialize_driver()
    try:
        host = get_host_for_selenium_testing()
        driver.get(f"{host}/filmdataset")
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1")))

        assert "Page not found" not in driver.title
        assert "Film-Hub" in driver.find_element(By.CSS_SELECTOR, "h1").text
    finally:
        close_driver(driver)


def test_filmdataset_upload_redirects_anonymous_to_login():
    driver = initialize_driver()
    try:
        host = get_host_for_selenium_testing()
        driver.get(f"{host}/filmdataset/upload")

        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, "password")))
        assert "/login" in driver.current_url
    finally:
        close_driver(driver)


def test_filmdataset_upload_invalid_csv_shows_validation_error(tmp_path):
    bad_csv = tmp_path / "invalid_movies.csv"
    bad_csv.write_text("title,year\nInception,2010\n", encoding="utf-8")

    driver = initialize_driver()
    try:
        _configure_file_detector(driver)
        host = get_host_for_selenium_testing()
        _log_in(driver, host)
        driver.get(f"{host}/filmdataset/upload")

        file_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input.dz-hidden-input"))
        )
        file_input.send_keys(str(bad_csv))

        error_box = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, "film_csv_errors")))
        assert "genre" in error_box.text.lower()
        assert not driver.find_element(By.ID, "film_upload_dataset").is_displayed()
    finally:
        close_driver(driver)


def test_filmdataset_upload_valid_csv_and_paginated_preview(tmp_path):
    rows = ["title,year,genre,rating,duration"]
    for idx in range(1, 13):
        year = 2000 + idx
        genre = "Drama" if idx <= 8 else "Sci-Fi"
        rows.append(f"Movie {idx},{year},{genre},8.5,{100 + idx}")
    valid_csv = tmp_path / "selenium_movies.csv"
    valid_csv.write_text("\n".join(rows) + "\n", encoding="utf-8")

    driver = initialize_driver()
    try:
        _configure_file_detector(driver)
        host = get_host_for_selenium_testing()
        _sign_up_fresh_user(driver, host)
        driver.get(f"{host}/filmdataset/upload")

        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "film_title"))).send_keys(
            "Selenium Film Catalog"
        )
        driver.find_element(By.ID, "film_desc").send_keys("Uploaded via Selenium E2E test")
        driver.find_element(By.ID, "film_tags").send_keys("cinema,selenium")

        file_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input.dz-hidden-input"))
        )
        file_input.send_keys(str(valid_csv))

        WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, "film_csv_summary")))
        WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, "film_upload_dataset")))

        _scroll_and_click(driver, driver.find_element(By.ID, "film_agree_checkbox"))
        upload_btn = driver.find_element(By.ID, "film_upload_button")
        WebDriverWait(driver, 10).until(lambda d: upload_btn.is_enabled())
        _scroll_and_click(driver, upload_btn)

        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "film-metrics-cards")))
        assert driver.find_element(By.ID, "metric-total-movies").text.strip() == "12"
        assert driver.find_element(By.ID, "metric-year-range").text.strip() == "2001 - 2012"
        assert driver.find_element(By.ID, "metric-primary-genre").text.strip() == "Drama"
        assert "8.50" in driver.find_element(By.ID, "metric-avg-rating").text.strip()

        WebDriverWait(driver, 15).until(lambda d: len(d.find_elements(By.CSS_SELECTOR, "#film-preview-tbody tr")) == 10)
        assert "Page 1 of 2" in driver.find_element(By.ID, "film-preview-page-info").text

        _scroll_and_click(driver, driver.find_element(By.ID, "film-preview-next"))
        WebDriverWait(driver, 15).until(lambda d: len(d.find_elements(By.CSS_SELECTOR, "#film-preview-tbody tr")) == 2)
        assert "Page 2 of 2" in driver.find_element(By.ID, "film-preview-page-info").text
        assert "Movie 11" in driver.find_element(By.ID, "film-preview-tbody").text
    finally:
        close_driver(driver)
