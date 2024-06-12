import time
import random
import string
import re
from faker import Faker
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
# options.add_argument("--disable-notifications")
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(5)
wait = WebDriverWait(driver, 5)

singleTask = {
    "name": "",
    "status": "",
    "priority": "",
    "phase": "",
    "time_estimation": ""
}

taskInfo = []
customSaveTaskInfo = []

driver.get("https://uat.app.worklenz.com/auth/login")
driver.maximize_window()


def main():
    login()
    go_to_projects_tab()


def login():
    wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Email']"))).send_keys(
        "testauto@1.com")
    wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Password']"))).send_keys(
        "ceyDigital#00")
    wait.until(EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='Log in']"))).click()


def go_to_projects_tab():
    driver.get("https://uat.app.worklenz.com/worklenz/projects")


def check_need_tasksList_fields_visible():
    show_fields = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "worklenz-task-list-columns-toggle")))
    show_fields_wait = WebDriverWait(show_fields, 10)
    show_fields_wait.until(EC.visibility_of_element_located((By.TAG_NAME, "button"))).click()
    drop_down_menu = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "cdk-overlay-connected-position-bounding-box")))
    drop_down_menu_wait = WebDriverWait(drop_down_menu, 10)
    drop_main = drop_down_menu_wait.until(EC.visibility_of_all_elements_located((By.TAG_NAME, "div")))[1]
    drop_main_wait = WebDriverWait(drop_main, 10)
    items = drop_main_wait.until(EC.visibility_of_all_elements_located((By.TAG_NAME, "li")))
    phase_field = items[-1].get_attribute("class")
    time_estimated_field = items[8].get_attribute("class")
    included_class_name = r'\bant-checkbox-wrapper-checked\b'
    check_phase_class_name = re.search(included_class_name, phase_field)
    check_estimated_class_name = re.search(included_class_name, time_estimated_field)

    if check_phase_class_name:
        print("Phase field already checked")

    else:
        items[-1].click()

    if check_estimated_class_name:
        print("Time estimated already checked")

    else:
        items[8].click()

    driver.find_element(By.XPATH, "//label[normalize-space()='Group by:']").click()
    time.sleep(2)


def create_project_tasks():
    fake = Faker()
    taskList = driver.find_element(By.CLASS_NAME, "tasks-wrapper")
    add_task_bts = taskList.find_elements(By.CLASS_NAME, "editable-row")
    for add_task_bt in add_task_bts:
        add_task_bt.click()
        time.sleep(1)
        random_task_name = fake.catch_phrase()
        driver.find_element(By.CSS_SELECTOR, "input[placeholder = 'Type your task and hit enter']").send_keys(
            random_task_name + Keys.ENTER)
        time.sleep(2)


def get_tasks_data():
    task_list = driver.find_element(By.CLASS_NAME, "tasks-wrapper")
    tasksRow = task_list.find_elements(By.TAG_NAME, "worklenz-task-list-row")
    for taskRow in tasksRow:
        task_name = taskRow.find_element(By.CLASS_NAME, "task-name-text")
        status_cell = taskRow.find_element(By.TAG_NAME, "worklenz-task-list-status")
        status = status_cell.find_element(By.TAG_NAME, "nz-select-item")
        priority_cell = taskRow.find_element(By.TAG_NAME, "worklenz-task-list-priority")
        priority = priority_cell.find_element(By.TAG_NAME, "nz-select-item")
        phases_cell = taskRow.find_element(By.TAG_NAME, "worklenz-task-list-phase")
        try:
            phase = phases_cell.find_element(By.TAG_NAME, "nz-select-item")
            phase_text = phase.text

        except NoSuchElementException:
            phase_text = ""

        estimated_time_cell = taskRow.find_element(By.CLASS_NAME, "task-estimation")
        estimated_time = estimated_time_cell.find_element(By.CLASS_NAME, "task-due-label")

        singleTask["name"] = task_name.text
        singleTask["status"] = status.text
        singleTask["priority"] = priority.text
        singleTask["phase"] = phase_text
        singleTask["time_estimation"] = estimated_time.text

        taskInfo.append(singleTask.copy())


def save_custom_template():
    fake = Faker()
    random_tem_name = fake.name()
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)
    header_bts = driver.find_element(By.TAG_NAME, "nz-page-header-extra")
    temp_save_btn = header_bts.find_elements(By.TAG_NAME, "button")[1]
    temp_save_btn.click()
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Enter template name"]').send_keys(Keys.ENTER)
    temp_name = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Enter template name"]')
    temp_name.send_keys(random_tem_name)
    entered_value = temp_name.get_attribute("value")
    time.sleep(1)
    save_btn = driver.find_element(By.CSS_SELECTOR,
                                   "div[class='ant-drawer ant-drawer-right ng-star-inserted ant-drawer-open'] button[class='ant-btn ant-btn-primary'] span[class='ng-star-inserted']")
    save_btn.click()
    time.sleep(5)
    return entered_value


def go_to_saved_custom_template():
    wl_header = driver.find_element(By.TAG_NAME, "worklenz-header")
    left_header = wl_header.find_elements(By.TAG_NAME, "ul")[2]
    profile_icon = left_header.find_elements(By.TAG_NAME, "li")[-1]
    profile_icon.click()
    time.sleep(1)
    drop_down_menu = driver.find_element(By.CSS_SELECTOR,
                                         "ul[class='ant-menu ant-menu-root ant-menu-light ant-menu-vertical']")
    drop_down_menu.find_elements(By.TAG_NAME, "li")[1].click()
    time.sleep(5)
    settings_side_bar = driver.find_element(By.TAG_NAME, "nz-sider")
    project_temp_tab = settings_side_bar.find_elements(By.TAG_NAME, "li")[6]
    project_temp_tab.click()
    time.sleep(6)


def edit_saved_custom_template(temp_name: str):
    table = driver.find_element(By.TAG_NAME, "tbody")
    table_rows = table.find_elements(By.TAG_NAME, "tr")
    row_index = -1
    for index, table_row in enumerate(table_rows):
        saved_tem_name = table_row.find_elements(By.CLASS_NAME, "ant-table-cell")[0]
        if temp_name == saved_tem_name.text:
            row_index = index
            break
    if row_index > -1:
        edit_btn = table_rows[row_index].find_elements(By.TAG_NAME, "button")[0]
        edit_btn.click()

    else:
        print("saved template not found")
        pagination = driver.find_element(By.TAG_NAME, "nz-pagination")
        next_btn = pagination.find_element(By.CLASS_NAME, "ant-pagination-next")
        if next_btn.is_enabled():
            next_btn.click()
            time.sleep(2)
            edit_saved_custom_template(temp_name)
        else:
            print("not found")
            return


def get_saved_custom_project_data():
    table = driver.find_element(By.CLASS_NAME, "tasks-wrapper")
    tasks_rows = table.find_elements(By.TAG_NAME, "worklenz-pt-task-list-row")
    for task_row in tasks_rows:
        task_name = task_row.find_element(By.CLASS_NAME, "task-name-text")
        print(task_name.text)
        phase_cell = task_row.find_element(By.TAG_NAME, "worklenz-task-phase")
        try:
            phase = phase_cell.find_element(By.TAG_NAME, "nz-select-item")
            phase_text = phase.text

        except NoSuchElementException:
            phase_text = ""

        statues_cell = task_row.find_element(By.TAG_NAME, "worklenz-task-status")
        statues = statues_cell.find_element(By.TAG_NAME, "nz-select-item")
        print(statues.text)
        priority_cell = task_row.find_element(By.TAG_NAME, "worklenz-task-priority")
        priority = priority_cell.find_element(By.TAG_NAME, "nz-select-item")
        print(priority.text)
        time_estimated_cell = task_row.find_element(By.TAG_NAME, "worklenz-task-estimation")
        time_estimated = time_estimated_cell.find_element(By.TAG_NAME, "p")

        singleTask["name"] = task_name.text
        singleTask["status"] = statues.text
        singleTask["priority"] = priority.text
        singleTask["phase"] = phase_text
        singleTask["time_estimation"] = time_estimated.text

        customSaveTaskInfo.append(singleTask.copy())


def check_project_availability():
    project_tabel = driver.find_element(By.TAG_NAME, "table")
    table_body = project_tabel.find_element(By.TAG_NAME, "tbody")
    table_rows = table_body.find_elements(By.CLASS_NAME, "actions-row")
    if len(table_rows) > 0:
        table_rows[4].click()
        check_need_tasksList_fields_visible()
        create_project_tasks()
        get_tasks_data()
        saved_value = save_custom_template()
        go_to_saved_custom_template()
        edit_saved_custom_template(saved_value)
        get_saved_custom_project_data()

    else:
        wait.until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(),'Create Project')]"))).click()


main()
expected_URL = "https://uat.app.worklenz.com/worklenz/projects"
current_URL = driver.current_url
if expected_URL == current_URL:
    print("Projects tab page is loaded")
    check_project_availability()

    for task in taskInfo:
        # print(task)

        if task in customSaveTaskInfo:
            print(task["name"], "Task's information Saved successfully")

        else:
            print(task["name"], "Task's information Not saved successfully")

    time.sleep(10)
else:
    print("Projects tab page not loaded")

driver.quit()
