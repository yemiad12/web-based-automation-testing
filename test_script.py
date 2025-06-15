import os
def test_script(scenario):
    import time
    from datetime import datetime
    from selenium import webdriver
    from selenium.common.exceptions import NoSuchElementException
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.select import Select
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    import time
    import datetime

    # BASE_PATH = "https://app.3gisltd.com"
    BASE_PATH = "https://app.staging.3gisltd.com"
    # BASE_PATH = "https://apptest.3gisltd.com"
    AT_SELLER_PATH = f"{BASE_PATH}/#/login/seller"
    AT_BUYER_PATH = f"{BASE_PATH}/#/login/buyer"
    AT_SELLER_EMAIL = os.environ.get("AT_SELLER_EMAIL")
    AT_SELLER_NO = os.environ.get("AT_SELLER_NO")
    NEW_SELLER_EMAIL = os.environ.get("NEW_SELLER_EMAIL")
    NEW_SELLER_NO = os.environ.get("NEW_SELLER_NO")
    AT_BUYER_NO = os.environ.get("AT_BUYER_NO")
    NEW_BUYER_NO = os.environ.get("NEW_BUYER_NO")
    NEW_BUYER_EMAIL = os.environ.get("NEW_BUYER_EMAIL")
    AT_PASSWORD = os.environ.get("AT_PASSWORD")

    # Generate a unique directory name
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    user_data_dir = f"/tmp/selenium_user_data_{timestamp}"

    # chrome_options = webdriver.ChromeOptions()
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
    # chrome_options.add_argument("--user-data-dir=/tmp/chrome-user-data")
    chrome_options.add_argument("--headless")  # Runs browser without GUI (LIVE)
    # chrome_options.add_argument("--disable-gpu")  # Disables GPU acceleration
    # chrome_options.add_argument("--no-sandbox")  # Necessary for environments like containers
    # chrome_options.add_argument("--disable-dev-shm-usage")  # Addresses shared memory issues
    # If you need a specific window size:
    chrome_options.add_argument("--window-size=1920,1080") #LIVE

    test_scope = scenario
    print(test_scope)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(options=chrome_options, service=service)
    # driver.maximize_window() # TEST
    time.sleep(5)


    # ######## LOGIN TO SELLER ACCOUNT
    def seller_login():
        driver.get(AT_SELLER_PATH)
        driver.execute_script("location.reload(true);")
        time.sleep(5)

        input_email = driver.find_element(By.XPATH, '//*[@id="buyer_email"]')
        input_email.send_keys(AT_SELLER_EMAIL)

        input_pwd = driver.find_element(By.XPATH, '//*[@id="buyer_password"]')
        input_pwd.send_keys(AT_PASSWORD)

        login_btn = driver.find_element(By.XPATH, '//*[@id="seller"]/form/div[3]/button')
        login_btn.click()
        time.sleep(10)
        try:
            ok_btn = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[4]/div/button')
            driver.execute_script("arguments[0].scrollIntoView();", ok_btn)
            ok_btn.click()
            time.sleep(5)
        except NoSuchElementException:
            ok_btn = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[4]/div/button')
            driver.execute_script("arguments[0].scrollIntoView();", ok_btn)
            ok_btn.click()
            time.sleep(5)


    ##### SELLER CREATES P2P TRANSACTION
    def seller_creates_p2p():
        create_btn = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/nav/ul[2]/li/a')
        create_btn.click()
        time.sleep(2)

        continue_btn = driver.find_element(By.XPATH,
                                           '//*[@id="root"]/div/div/div[2]/section/div/div[2]/div[1]/div[3]/button')
        continue_btn.click()
        time.sleep(2)

        input_title = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/section/div/div[2]/div[1]/input')
        input_title.send_keys("Purchase of a pair of boots")

        # find category option
        category = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/section/div/div[3]/div[1]/select')
        drop_cat = Select(category)

        # select by visible text
        drop_cat.select_by_visible_text("General Transaction")
        time.sleep(2)

        if test_scope == "seller creates p2p with new buyer":
            input_buyer_no = driver.find_element(By.XPATH,
                                                 '/html/body/div[1]/div/div/div[2]/section/div/div[4]/div[1]/div[1]/input')
            input_buyer_no.send_keys(NEW_BUYER_NO)

            input_buyer_email = driver.find_element(By.XPATH,
                                                    '/html/body/div[1]/div/div/div[2]/section/div/div[5]/div[1]/input')
            input_buyer_email.send_keys(NEW_BUYER_EMAIL)
            time.sleep(5)

        else:
            input_buyer_no = driver.find_element(By.XPATH,
                                                 '/html/body/div[1]/div/div/div[2]/section/div/div[4]/div[1]/div[1]/input')
            input_buyer_no.send_keys("8324955157")
            time.sleep(5)

        try:
            input_ngn_price = driver.find_element(By.XPATH,
                                                  '/html/body/div[1]/div/div/div[2]/section/div/div[5]/div[1]/div/div/div/input')
            driver.execute_script("arguments[0].scrollIntoView();", input_ngn_price)
            input_ngn_price.clear()
            input_ngn_price.send_keys("10000")
        except NoSuchElementException:
            input_ngn_price = driver.find_element(By.XPATH,
                                                  '/html/body/div[1]/div/div/div[2]/section/div/div[6]/div[1]/div/div/div/input')
            driver.execute_script("arguments[0].scrollIntoView();", input_ngn_price)
            input_ngn_price.clear()
            input_ngn_price.send_keys("10000")

        try:
            input_qty = driver.find_element(By.XPATH,
                                            '/html/body/div[1]/div/div/div[2]/section/div/div[6]/div/div[1]/input')
            input_qty.clear()
            input_qty.send_keys("1")
            time.sleep(10)
        except NoSuchElementException:
            input_qty = driver.find_element(By.XPATH,
                                            '/html/body/div[1]/div/div/div[2]/section/div/div[7]/div/div[1]/input')
            input_qty.clear()
            input_qty.send_keys("1")
            time.sleep(10)

        try:

            escrow_buyer_radio_btn = driver.find_element(By.XPATH,
                                                         '/html/body/div[1]/div/div/div[2]/section/div/div[8]/div[1]/div[1]/input')
            # escrow_buyer_radio_btn = driver.find_element(By.XPATH,
            #                                   '/html/body/div[1]/div/div/div[2]/section/div/div[8]/div[1]/div[1]/input')
            escrow_buyer_radio_btn.click()
            time.sleep(5)
        except NoSuchElementException:

            escrow_buyer_radio_btn = driver.find_element(By.XPATH,
                                                         '/html/body/div[1]/div/div/div[2]/section/div/div[7]/div[1]/div[1]/input')
            escrow_buyer_radio_btn.click()
            time.sleep(5)

        try:
            no_ship_radio_btn = driver.find_element(By.XPATH,
                                                    '/html/body/div[1]/div/div/div[2]/section/div/div[8]/div/div[1]/div[1]/input')
            no_ship_radio_btn.click()
            time.sleep(5)
        except NoSuchElementException:
            no_ship_radio_btn = driver.find_element(By.XPATH,
                                                    '/html/body/div[1]/div/div/div[2]/section/div/div[9]/div/div[1]/div[1]/input')
            no_ship_radio_btn.click()
            time.sleep(5)

        try:
            input_address = driver.find_element(By.XPATH,
                                                '//*[@id="root"]/div/div/div[2]/section/div/div[9]/div/div[1]/textarea')
            driver.execute_script("arguments[0].scrollIntoView();", input_address)
            input_address.send_keys("3a, Oroke Drike, Ikoyi, Lagos. Nigeria.")
        except NoSuchElementException:
            input_address = driver.find_element(By.XPATH,
                                                '//*[@id="root"]/div/div/div[2]/section/div/div[10]/div/div[1]/textarea')
            driver.execute_script("arguments[0].scrollIntoView();", input_address)
            input_address.send_keys("3a, Oroke Drike, Ikoyi, Lagos. Nigeria.")

        try:
            input_description = driver.find_element(By.XPATH,
                                                    '//*[@id="root"]/div/div/div[2]/section/div/div[11]/div[1]/textarea')
            driver.execute_script("arguments[0].scrollIntoView();", input_description)
            input_description.send_keys("Expensive designer boots for my daughter.")
        except NoSuchElementException:
            input_description = driver.find_element(By.XPATH,
                                                    '//*[@id="root"]/div/div/div[2]/section/div/div[12]/div[1]/textarea')
            driver.execute_script("arguments[0].scrollIntoView();", input_description)
            input_description.send_keys("Expensive designer boots for my daughter.")

        # find payment option
        try:
            payment_btn = driver.find_element(By.XPATH,
                                              '//*[@id="root"]/div/div/div[2]/section/div/div[12]/div[1]/select')
            driver.execute_script("arguments[0].scrollIntoView();", payment_btn)
            drop_payment = Select(payment_btn)
        except NoSuchElementException:
            payment_btn = driver.find_element(By.XPATH,
                                              '//*[@id="root"]/div/div/div[2]/section/div/div[13]/div[1]/select')
            driver.execute_script("arguments[0].scrollIntoView();", payment_btn)
            drop_payment = Select(payment_btn)

        # select by visible text
        drop_payment.select_by_visible_text("Paystack (NGN Debit and Credit Payment)")
        time.sleep(2)

        try:
            start_btn = driver.find_element(By.XPATH,
                                            '//*[@id="root"]/div/div/div[2]/section/div/div[13]/div/button[2]')
            driver.execute_script("arguments[0].scrollIntoView();", start_btn)
            start_btn.click()
            time.sleep(25)
        except NoSuchElementException:
            start_btn = driver.find_element(By.XPATH,
                                            '//*[@id="root"]/div/div/div[2]/section/div/div[14]/div/button[2]')
            driver.execute_script("arguments[0].scrollIntoView();", start_btn)
            start_btn.click()
            time.sleep(25)

        try:
            ok_btn = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[4]/div/button')
            driver.execute_script("arguments[0].scrollIntoView();", ok_btn)
            ok_btn.click()
            time.sleep(5)
        except NoSuchElementException:
            ok_btn = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[4]/div/button')
            driver.execute_script("arguments[0].scrollIntoView();", ok_btn)
            ok_btn.click()
            time.sleep(5)

        dash_btn = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/aside/div/nav/ul/li[1]/a')
        dash_btn.click()
        time.sleep(5)


    ######## LOGOUT OF SELLER ACCOUNT
    def seller_logout():
        # find human icon option
        human_btn = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/nav/ul[2]/div/ul/a')
        driver.execute_script("arguments[0].scrollIntoView();", human_btn)
        human_btn.click()
        time.sleep(2)

        # select by visible text
        logout_option = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/nav/ul[2]/div/ul/div/li[3]')
        logout_option.click()
        time.sleep(10)


    ######## LOGIN TO BUYER ACCOUNT
    def buyer_login():
        driver.get(AT_BUYER_PATH)
        driver.execute_script("location.reload(true);")
        time.sleep(5)

        input_no = driver.find_element(By.XPATH, '//*[@id="buyer"]/form/div[1]/div/div/input')
        input_no.send_keys(AT_BUYER_NO)

        try:
            login_btn = driver.find_element(By.XPATH, '//*[@id="buyer"]/form/div[2]/button')
            driver.execute_script("arguments[0].scrollIntoView();", login_btn)
            login_btn.click()
            time.sleep(10)

        except NoSuchElementException:
            login_btn = driver.find_element(By.XPATH, '//*[@id="buyer"]/form/div[4]/button')
            driver.execute_script("arguments[0].scrollIntoView();", login_btn)
            login_btn.click()
            time.sleep(10)

        input_pwd = driver.find_element(By.XPATH, '//*[@id="buyer_password"]')
        input_pwd.send_keys(AT_PASSWORD)

        login_btn = driver.find_element(By.XPATH, '//*[@id="buyer"]/form/div[4]/button')
        login_btn.click()
        time.sleep(10)

        try:
            ok_btn = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[4]/div/button')
            driver.execute_script("arguments[0].scrollIntoView();", ok_btn)
            ok_btn.click()
            time.sleep(5)
        except NoSuchElementException:
            ok_btn = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[4]/div/button')
            driver.execute_script("arguments[0].scrollIntoView();", ok_btn)
            ok_btn.click()
            time.sleep(5)


    ###################### SELLER AGREES ##############
    def seller_agrees():
        # ## myp2p
        p2p_btn = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/aside/div/nav/ul/li[3]/a')
        p2p_btn.click()
        time.sleep(2)

        # storing the current window handle to get back to dashboard
        main_page = driver.current_window_handle
        time.sleep(20)

        rows = driver.find_element(By.XPATH,
                                   '/html/body/div[1]/div/div/div[2]/div/section/div/div/div/div[2]/div/div[2]/div/div[2]/div/div[2]/span[2]/select')
        drop_rows = Select(rows)

        # select by visible text
        drop_rows.select_by_visible_text("100 rows")
        time.sleep(2)

        ### Find the first respond link and click
        terms_link = driver.find_element(By.LINK_TEXT, "Respond to Terms")
        driver.execute_script("arguments[0].scrollIntoView();", terms_link)
        terms_link.click()
        time.sleep(5)

        # changing the handles to access the response pop up
        response_popup = ""
        for handle in driver.window_handles:
            if handle != main_page:
                response_popup = handle

        # change the control to the response page
        driver.switch_to.window(response_popup)

        # #modal
        try:
            terms_options = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/form/div[2]/div/div/div[2]/select')
            drop_terms = Select(terms_options)

        except NoSuchElementException:
            terms_options = driver.find_element(By.XPATH, '/html/body/div[4]/div/div/form/div[2]/div/div/div[2]/select')
            drop_terms = Select(terms_options)

        # select by visible text
        drop_terms.select_by_visible_text("Agree")
        # drop_impediment.select_by_visible_text("Yes (Order is not ok)")
        # drop_impediment.select_by_visible_text("Buyer and I have agreed to another delivery attempt")
        time.sleep(2)

        try:
            submit_btn = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/form/div[2]/div/div/button')
            driver.execute_script("arguments[0].scrollIntoView();", submit_btn)
            submit_btn.click()
            time.sleep(10)

        except NoSuchElementException:
            submit_btn = driver.find_element(By.XPATH, '/html/body/div[4]/div/div/form/div[2]/div/div/button')
            driver.execute_script("arguments[0].scrollIntoView();", submit_btn)
            submit_btn.click()
            time.sleep(10)

        # change control to main page
        driver.switch_to.window(main_page)

        try:
            ok_btn = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[4]/div/button')
            driver.execute_script("arguments[0].scrollIntoView();", ok_btn)
            ok_btn.click()
            time.sleep(10)
        except NoSuchElementException:
            ok_btn = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[4]/div/button')
            driver.execute_script("arguments[0].scrollIntoView();", ok_btn)
            ok_btn.click()
            time.sleep(10)
        # "/html/body/div[3]/div/div[4]/div/button"

        dash_btn = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/aside/div/nav/ul/li[1]/a')
        dash_btn.click()
        time.sleep(5)


    ###################### SELLER DISAGREES ##############
    def seller_disagrees():
        # ## myp2p
        p2p_btn = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/aside/div/nav/ul/li[3]/a')
        p2p_btn.click()
        time.sleep(2)

        # storing the current window handle to get back to dashboard
        main_page = driver.current_window_handle
        time.sleep(20)

        rows = driver.find_element(By.XPATH,
                                   '/html/body/div[1]/div/div/div[2]/div/section/div/div/div/div[2]/div/div[2]/div/div[2]/div/div[2]/span[2]/select')
        drop_rows = Select(rows)

        # select by visible text
        drop_rows.select_by_visible_text("100 rows")
        time.sleep(2)

        ### Find the first respond link and click
        terms_link = driver.find_element(By.LINK_TEXT, "Respond to Terms")
        driver.execute_script("arguments[0].scrollIntoView();", terms_link)
        terms_link.click()
        time.sleep(5)

        # changing the handles to access the response pop up
        response_popup = ""
        for handle in driver.window_handles:
            if handle != main_page:
                response_popup = handle

        # change the control to the response page
        driver.switch_to.window(response_popup)

        # #modal
        try:
            terms_options = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/form/div[2]/div/div/div[2]/select')
            drop_terms = Select(terms_options)

        except NoSuchElementException:
            terms_options = driver.find_element(By.XPATH, '/html/body/div[4]/div/div/form/div[2]/div/div/div[2]/select')
            drop_terms = Select(terms_options)

        # select by visible text
        drop_terms.select_by_visible_text("Disagree")
        time.sleep(2)

        input_reason = driver.find_element(By.XPATH,
                                           '//html/body/div[4]/div/div/form/div[2]/div/div/div[3]/textarea')
        driver.execute_script("arguments[0].scrollIntoView();", input_reason)
        input_reason.send_keys("The deal is not sweet yet.")

        try:
            submit_btn = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/form/div[2]/div/div/button')
            driver.execute_script("arguments[0].scrollIntoView();", submit_btn)
            submit_btn.click()
            time.sleep(10)

        except NoSuchElementException:
            submit_btn = driver.find_element(By.XPATH, '/html/body/div[4]/div/div/form/div[2]/div/div/button')
            driver.execute_script("arguments[0].scrollIntoView();", submit_btn)
            submit_btn.click()
            time.sleep(10)

        # change control to main page
        driver.switch_to.window(main_page)

        try:
            ok_btn = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[4]/div/button')
            driver.execute_script("arguments[0].scrollIntoView();", ok_btn)
            ok_btn.click()
            time.sleep(10)
        except NoSuchElementException:
            ok_btn = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[4]/div/button')
            driver.execute_script("arguments[0].scrollIntoView();", ok_btn)
            ok_btn.click()
            time.sleep(10)
        # "/html/body/div[3]/div/div[4]/div/button"

        dash_btn = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/aside/div/nav/ul/li[1]/a')
        dash_btn.click()
        time.sleep(5)


    # ############ MAKE PAYMENT
    def make_payment():
        # ## myP2P
        p2p_btn = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/aside/div/nav/ul/li[3]/a')
        p2p_btn.click()
        time.sleep(2)

        # storing the current window handle to get back to dashboard
        main_page = driver.current_window_handle
        time.sleep(20)

        ### Find the first payment link and click to pay
        payment_link = driver.find_element(By.LINK_TEXT, "Make Payment")
        payment_link.click()
        time.sleep(5)

        # changing the handles to access the details page
        details_page = ""
        for handle in driver.window_handles:
            if handle != main_page:
                details_page = handle

        # change the control to the details page
        driver.switch_to.window(details_page)

        # #modal
        yes_btn = driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div/div[3]/div[2]/button[2]')
        yes_btn.click()
        time.sleep(15)

        # change control to main page
        driver.switch_to.window(main_page)

        success_radio_btn = driver.find_element(By.XPATH,
                                                '/html/body/div/div/div/div/section/div/div/div[2]/div/section/div/div/div/div[1]/div[1]/div/div[1]/div')
        success_radio_btn.click()
        time.sleep(5)

        paystack_pay_btn = driver.find_element(By.XPATH, '//*[@id="test-cards"]/button')
        paystack_pay_btn.click()
        time.sleep(30)

        close_btn = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div/button')
        close_btn.click()
        time.sleep(5)

        dash_btn = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/aside/div/nav/ul/li[1]/a')
        dash_btn.click()
        time.sleep(5)


    ##### BUYER CREATES P2P TRANSACTION
    def buyer_creates_p2p():
        create_btn = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/nav/ul[2]/li/a')
        create_btn.click()
        time.sleep(2)

        continue_btn = driver.find_element(By.XPATH,
                                           '//*[@id="root"]/div/div/div[2]/section/div/div[2]/div[1]/div[3]/button')
        continue_btn.click()
        time.sleep(2)

        input_title = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/section/div/div[2]/div[1]/input')
        input_title.send_keys("Purchase of a pair of boots")

        # find category option
        category = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/section/div/div[3]/div[1]/select')
        drop_cat = Select(category)

        # select by visible text
        drop_cat.select_by_visible_text("General Transaction")
        time.sleep(2)

        if test_scope == "buyer creates p2p with new seller":
            input_seller_no = driver.find_element(By.XPATH,
                                                  '/html/body/div[1]/div/div/div[2]/section/div/div[4]/div[1]/div[1]/input')
            input_seller_no.send_keys(NEW_SELLER_NO)

            input_seller_email = driver.find_element(By.XPATH,
                                                     '/html/body/div[1]/div/div/div[2]/section/div/div[5]/div[1]/input')
            input_seller_email.send_keys(NEW_SELLER_EMAIL)
            time.sleep(5)
        else:
            input_seller_no = driver.find_element(By.XPATH,
                                                  '/html/body/div[1]/div/div/div[2]/section/div/div[4]/div[1]/div[1]/input')
            input_seller_no.send_keys(AT_SELLER_NO)

        try:
            input_ngn_price = driver.find_element(By.XPATH,
                                                  '/html/body/div[1]/div/div/div[2]/section/div/div[5]/div[1]/div/div/div/input')
            driver.execute_script("arguments[0].scrollIntoView();", input_ngn_price)
            input_ngn_price.clear()
            input_ngn_price.send_keys("10000")
        except NoSuchElementException:
            input_ngn_price = driver.find_element(By.XPATH,
                                                  '/html/body/div[1]/div/div/div[2]/section/div/div[6]/div[1]/div/div/div/input')
            driver.execute_script("arguments[0].scrollIntoView();", input_ngn_price)
            input_ngn_price.clear()
            input_ngn_price.send_keys("10000")

        try:
            input_qty = driver.find_element(By.XPATH,
                                            '/html/body/div[1]/div/div/div[2]/section/div/div[6]/div/div[1]/input')
            input_qty.clear()
            input_qty.send_keys("1")
            time.sleep(10)
        except NoSuchElementException:
            input_qty = driver.find_element(By.XPATH,
                                            '/html/body/div[1]/div/div/div[2]/section/div/div[7]/div/div[1]/input')
            input_qty.clear()
            input_qty.send_keys("1")
            time.sleep(10)

        try:

            escrow_buyer_radio_btn = driver.find_element(By.XPATH,
                                                         '/html/body/div[1]/div/div/div[2]/section/div/div[8]/div[1]/div[1]/input')
            # escrow_buyer_radio_btn = driver.find_element(By.XPATH,
            #                                   '/html/body/div[1]/div/div/div[2]/section/div/div[8]/div[1]/div[1]/input')
            escrow_buyer_radio_btn.click()
            time.sleep(5)
        except NoSuchElementException:

            escrow_buyer_radio_btn = driver.find_element(By.XPATH,
                                                         '/html/body/div[1]/div/div/div[2]/section/div/div[7]/div[1]/div[1]/input')
            escrow_buyer_radio_btn.click()
            time.sleep(5)

        try:
            no_ship_radio_btn = driver.find_element(By.XPATH,
                                                    '/html/body/div[1]/div/div/div[2]/section/div/div[8]/div/div[1]/div[1]/input')
            no_ship_radio_btn.click()
            time.sleep(5)
        except NoSuchElementException:
            no_ship_radio_btn = driver.find_element(By.XPATH,
                                                    '/html/body/div[1]/div/div/div[2]/section/div/div[9]/div/div[1]/div[1]/input')
            no_ship_radio_btn.click()
            time.sleep(5)

        try:
            input_address = driver.find_element(By.XPATH,
                                                '//*[@id="root"]/div/div/div[2]/section/div/div[9]/div/div[1]/textarea')
            driver.execute_script("arguments[0].scrollIntoView();", input_address)
            input_address.send_keys("3a, Oroke Drike, Ikoyi, Lagos. Nigeria.")
        except NoSuchElementException:
            input_address = driver.find_element(By.XPATH,
                                                '//*[@id="root"]/div/div/div[2]/section/div/div[10]/div/div[1]/textarea')
            driver.execute_script("arguments[0].scrollIntoView();", input_address)
            input_address.send_keys("3a, Oroke Drike, Ikoyi, Lagos. Nigeria.")

        try:
            input_description = driver.find_element(By.XPATH,
                                                    '//*[@id="root"]/div/div/div[2]/section/div/div[11]/div[1]/textarea')
            driver.execute_script("arguments[0].scrollIntoView();", input_description)
            input_description.send_keys("Expensive designer boots for my daughter.")
        except NoSuchElementException:
            input_description = driver.find_element(By.XPATH,
                                                    '//*[@id="root"]/div/div/div[2]/section/div/div[12]/div[1]/textarea')
            driver.execute_script("arguments[0].scrollIntoView();", input_description)
            input_description.send_keys("Expensive designer boots for my daughter.")

        # find payment option
        try:
            payment_btn = driver.find_element(By.XPATH,
                                              '//*[@id="root"]/div/div/div[2]/section/div/div[12]/div[1]/select')
            driver.execute_script("arguments[0].scrollIntoView();", payment_btn)
            drop_payment = Select(payment_btn)
        except NoSuchElementException:
            payment_btn = driver.find_element(By.XPATH,
                                              '//*[@id="root"]/div/div/div[2]/section/div/div[13]/div[1]/select')
            driver.execute_script("arguments[0].scrollIntoView();", payment_btn)
            drop_payment = Select(payment_btn)

        # select by visible text
        drop_payment.select_by_visible_text("Paystack (NGN Debit and Credit Payment)")
        time.sleep(2)

        try:
            start_btn = driver.find_element(By.XPATH,
                                            '//*[@id="root"]/div/div/div[2]/section/div/div[13]/div/button[2]')
            driver.execute_script("arguments[0].scrollIntoView();", start_btn)
            start_btn.click()
            time.sleep(25)
        except NoSuchElementException:
            start_btn = driver.find_element(By.XPATH,
                                            '//*[@id="root"]/div/div/div[2]/section/div/div[14]/div/button[2]')
            driver.execute_script("arguments[0].scrollIntoView();", start_btn)
            start_btn.click()
            time.sleep(25)

        try:
            ok_btn = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[4]/div/button')
            driver.execute_script("arguments[0].scrollIntoView();", ok_btn)
            ok_btn.click()
            time.sleep(10)
        except NoSuchElementException:
            ok_btn = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[4]/div/button')
            driver.execute_script("arguments[0].scrollIntoView();", ok_btn)
            ok_btn.click()
            time.sleep(10)

        dash_btn = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/aside/div/nav/ul/li[1]/a')
        dash_btn.click()
        time.sleep(10)


    ### BUYER LOGOUT
    def buyer_logout():
        # find human icon option
        human_btn = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/nav/ul[2]/div/ul/a')
        driver.execute_script("arguments[0].scrollIntoView();", human_btn)
        human_btn.click()
        time.sleep(2)

        # select by visible text
        logout_option = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/nav/ul[2]/div/ul/div/li[3]')
        logout_option.click()
        time.sleep(10)


    #### ESCROW PROCESS
    def escrow_delivery():
        # ## orders
        orders_btn = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/aside/div/nav/ul/li[2]/a')
        orders_btn.click()
        time.sleep(2)

        # storing the current window handle to get back to dashboard
        main_page = driver.current_window_handle
        time.sleep(20)

        rows = driver.find_element(By.XPATH,
                                   '/html/body/div[1]/div/div/div[2]/div/section/div/div/div/div[2]/div/div[2]/div/div[2]/div/div[2]/span[2]/select')
        drop_rows = Select(rows)

        # select by visible text
        drop_rows.select_by_visible_text("100 rows")
        time.sleep(2)

        ### Find the first delivery link and click to pay
        delivery_link = driver.find_element(By.LINK_TEXT, "Delivery Completed.")
        driver.execute_script("arguments[0].scrollIntoView();", delivery_link)
        delivery_link.click()
        time.sleep(5)

        # changing the handles to access the delivery pop up
        delivery_popup = ""
        for handle in driver.window_handles:
            if handle != main_page:
                delivery_popup = handle

        # change the control to the delivery page
        driver.switch_to.window(delivery_popup)

        # #modal
        yes_deliver_btn = driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div[3]/button[1]')
        yes_deliver_btn.click()
        time.sleep(5)

        # change control to main page
        driver.switch_to.window(main_page)

        try:
            ok_btn = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[4]/div/button')
            driver.execute_script("arguments[0].scrollIntoView();", ok_btn)
            ok_btn.click()
            time.sleep(10)
        except NoSuchElementException:
            ok_btn = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[4]/div/button')
            driver.execute_script("arguments[0].scrollIntoView();", ok_btn)
            ok_btn.click()
            time.sleep(10)

        dash_btn = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/aside/div/nav/ul/li[1]/a')
        dash_btn.click()
        time.sleep(5)


    def escrow_accept():
        # ## orders
        orders_btn = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/aside/div/nav/ul/li[2]/a')
        orders_btn.click()
        time.sleep(2)

        # storing the current window handle to get back to dashboard
        main_page = driver.current_window_handle
        time.sleep(20)

        rows = driver.find_element(By.XPATH,
                                   '/html/body/div[1]/div/div/div[2]/div/section/div/div/div/div[2]/div/div[2]/div/div[2]/div/div[2]/span[2]/select')
        drop_rows = Select(rows)

        # select by visible text
        drop_rows.select_by_visible_text("100 rows")
        time.sleep(2)

        ### Find the first accept link and click to pay
        accept_link = driver.find_element(By.LINK_TEXT, "Accept")
        driver.execute_script("arguments[0].scrollIntoView();", accept_link)
        accept_link.click()
        time.sleep(5)

        # changing the handles to access the accept pop up
        accept_popup = ""
        for handle in driver.window_handles:
            if handle != main_page:
                accept_popup = handle

        # change the control to the accept page
        driver.switch_to.window(accept_popup)

        # #modal
        yes_accept_btn = driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div[3]/button[1]')
        yes_accept_btn.click()
        time.sleep(15)

        # change control to main page
        driver.switch_to.window(main_page)

        try:
            ok_btn = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[4]/div/button')
            driver.execute_script("arguments[0].scrollIntoView();", ok_btn)
            ok_btn.click()
            time.sleep(10)
        except NoSuchElementException:
            ok_btn = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[4]/div/button')
            driver.execute_script("arguments[0].scrollIntoView();", ok_btn)
            ok_btn.click()
            time.sleep(10)

        dash_btn = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/aside/div/nav/ul/li[1]/a')
        dash_btn.click()
        time.sleep(5)


    def escrow_reject_no_fee():
        # ## orders
        orders_btn = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/aside/div/nav/ul/li[2]/a')
        orders_btn.click()
        time.sleep(2)

        # storing the current window handle to get back to dashboard
        main_page = driver.current_window_handle
        time.sleep(20)

        rows = driver.find_element(By.XPATH,
                                   '/html/body/div[1]/div/div/div[2]/div/section/div/div/div/div[2]/div/div[2]/div/div[2]/div/div[2]/span[2]/select')
        drop_rows = Select(rows)

        # select by visible text
        drop_rows.select_by_visible_text("100 rows")
        time.sleep(2)

        ### Find the first reject link and click to pay

        reject_link = driver.find_element(By.LINK_TEXT, "Reject")
        driver.execute_script("arguments[0].scrollIntoView();", reject_link)
        reject_link.click()
        time.sleep(5)

        # changing the handles to access the options pop up
        reject_popup = ""
        for handle in driver.window_handles:
            if handle != main_page:
                reject_popup = handle

        # change the control to the options popup
        driver.switch_to.window(reject_popup)

        # #modal
        try:
            no_fee_radio_btn = driver.find_element(By.XPATH,
                                                   '/html/body/div[3]/div/div/div/div/form/div[1]/div[1]/div[1]/input')
            no_fee_radio_btn.click()
            time.sleep(5)

        except NoSuchElementException:
            no_fee_radio_btn = driver.find_element(By.XPATH,
                                                   '/html/body/div[4]/div/div/div/div/form/div[1]/div[1]/div[1]/input')
            no_fee_radio_btn.click()
            time.sleep(5)

        try:
            submit_btn = driver.find_element(By.XPATH, '//html/body/div[3]/div/div/div/div/form/div[2]/input')
            submit_btn.click()
            time.sleep(5)

        except NoSuchElementException:
            submit_btn = driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div/div/form/div[2]/input')
            submit_btn.click()
            time.sleep(5)

        # change control to main page
        driver.switch_to.window(main_page)

        try:
            ok_btn = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[4]/div/button')
            driver.execute_script("arguments[0].scrollIntoView();", ok_btn)
            ok_btn.click()
            time.sleep(10)
        except NoSuchElementException:
            ok_btn = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[4]/div/button')
            driver.execute_script("arguments[0].scrollIntoView();", ok_btn)
            ok_btn.click()
            time.sleep(10)

        dash_btn = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/aside/div/nav/ul/li[1]/a')
        dash_btn.click()
        time.sleep(5)


    def escrow_reject_with_fee():
        # ## orders
        orders_btn = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/aside/div/nav/ul/li[2]/a')
        orders_btn.click()
        time.sleep(2)

        # storing the current window handle to get back to dashboard
        main_page = driver.current_window_handle
        time.sleep(20)

        rows = driver.find_element(By.XPATH,
                                   '/html/body/div[1]/div/div/div[2]/div/section/div/div/div/div[2]/div/div[2]/div/div[2]/div/div[2]/span[2]/select')
        drop_rows = Select(rows)

        # select by visible text
        drop_rows.select_by_visible_text("100 rows")
        time.sleep(2)

        ### Find the first reject link and click to pay
        reject_link = driver.find_element(By.LINK_TEXT, "Reject")
        driver.execute_script("arguments[0].scrollIntoView();", reject_link)
        reject_link.click()
        time.sleep(5)

        # changing the handles to access the reject pop up
        reject_popup = ""
        for handle in driver.window_handles:
            if handle != main_page:
                reject_popup = handle

        # change the control to the options popup
        driver.switch_to.window(reject_popup)

        # #modal

        incur_fee_radio_btn = driver.find_element(By.XPATH,
                                                  '/html/body/div[3]/div/div/div/div/form/div[1]/div[5]/div[1]/input')
        incur_fee_radio_btn.click()
        time.sleep(5)

        try:
            submit_btn = driver.find_element(By.XPATH, '//html/body/div[3]/div/div/div/div/form/div[2]/input')
            submit_btn.click()
            time.sleep(5)

        except NoSuchElementException:
            submit_btn = driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div/div/form/div[2]/input')
            submit_btn.click()
            time.sleep(5)

        # change control to main page
        driver.switch_to.window(main_page)

        try:
            ok_btn = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[4]/div/button')
            driver.execute_script("arguments[0].scrollIntoView();", ok_btn)
            ok_btn.click()
            time.sleep(10)
        except NoSuchElementException:
            ok_btn = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[4]/div/button')
            driver.execute_script("arguments[0].scrollIntoView();", ok_btn)
            ok_btn.click()
            time.sleep(10)

        dash_btn = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/aside/div/nav/ul/li[1]/a')
        dash_btn.click()
        time.sleep(5)


    def seller_confirms_ok():
        # ## orders
        orders_btn = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/aside/div/nav/ul/li[2]/a')
        orders_btn.click()
        time.sleep(2)

        # storing the current window handle to get back to dashboard
        main_page = driver.current_window_handle
        time.sleep(20)

        rows = driver.find_element(By.XPATH,
                                   '/html/body/div[1]/div/div/div[2]/div/section/div/div/div/div[2]/div/div[2]/div/div[2]/div/div[2]/span[2]/select')
        drop_rows = Select(rows)

        # select by visible text
        drop_rows.select_by_visible_text("100 rows")
        time.sleep(2)

        ### Find the first delivery link and click to pay
        impediment_link = driver.find_element(By.LINK_TEXT, "Confirm Impediment")
        driver.execute_script("arguments[0].scrollIntoView();", impediment_link)
        impediment_link.click()
        time.sleep(5)

        # changing the handles to access the delivery pop up
        delivery_popup = ""
        for handle in driver.window_handles:
            if handle != main_page:
                delivery_popup = handle

        # change the control to the delivery page
        driver.switch_to.window(delivery_popup)

        # #modal
        impediment_options = driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div/div/form/div[1]/select')
        drop_impediment = Select(impediment_options)

        # select by visible text
        drop_impediment.select_by_visible_text("Yes (Order is ok)")
        # drop_impediment.select_by_visible_text("Yes (Order is not ok)")
        # drop_impediment.select_by_visible_text("Buyer and I have agreed to another delivery attempt")
        time.sleep(2)

        submit_btn = driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div/div/form/div[2]/input')
        driver.execute_script("arguments[0].scrollIntoView();", submit_btn)
        submit_btn.click()
        time.sleep(10)

        # change control to main page
        driver.switch_to.window(main_page)

        try:
            ok_btn = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[4]/div/button')
            driver.execute_script("arguments[0].scrollIntoView();", ok_btn)
            ok_btn.click()
            time.sleep(10)
        except NoSuchElementException:
            ok_btn = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[4]/div/button')
            driver.execute_script("arguments[0].scrollIntoView();", ok_btn)
            ok_btn.click()
            time.sleep(10)
        # "/html/body/div[3]/div/div[4]/div/button"

        dash_btn = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/aside/div/nav/ul/li[1]/a')
        dash_btn.click()
        time.sleep(5)


    def seller_confirms_not_ok():
        # ## orders
        orders_btn = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/aside/div/nav/ul/li[2]/a')
        orders_btn.click()
        time.sleep(2)

        # storing the current window handle to get back to dashboard
        main_page = driver.current_window_handle
        time.sleep(20)

        rows = driver.find_element(By.XPATH,
                                   '/html/body/div[1]/div/div/div[2]/div/section/div/div/div/div[2]/div/div[2]/div/div[2]/div/div[2]/span[2]/select')
        drop_rows = Select(rows)

        # select by visible text
        drop_rows.select_by_visible_text("100 rows")
        time.sleep(2)

        ### Find the first delivery link and click to pay
        impediment_link = driver.find_element(By.LINK_TEXT, "Confirm Impediment")
        driver.execute_script("arguments[0].scrollIntoView();", impediment_link)
        impediment_link.click()
        time.sleep(5)

        # changing the handles to access the delivery pop up
        delivery_popup = ""
        for handle in driver.window_handles:
            if handle != main_page:
                delivery_popup = handle

        # change the control to the delivery page
        driver.switch_to.window(delivery_popup)

        # #modal
        impediment_options = driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div/div/form/div[1]/select')
        drop_impediment = Select(impediment_options)
        # impediment_options.click()
        # "//*[@id="response"]"

        # select by visible text
        drop_impediment.select_by_visible_text("No (Order is not ok)")
        # drop_impediment.select_by_visible_text("Buyer and I have agreed to another delivery attempt")
        time.sleep(2)

        submit_btn = driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div/div/form/div[2]/input')
        driver.execute_script("arguments[0].scrollIntoView();", submit_btn)
        submit_btn.click()
        time.sleep(10)

        # change control to main page
        driver.switch_to.window(main_page)

        try:
            ok_btn = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[4]/div/button')
            driver.execute_script("arguments[0].scrollIntoView();", ok_btn)
            ok_btn.click()
            time.sleep(10)
        except NoSuchElementException:
            ok_btn = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[4]/div/button')
            driver.execute_script("arguments[0].scrollIntoView();", ok_btn)
            ok_btn.click()
            time.sleep(10)
        # "/html/body/div[3]/div/div[4]/div/button"

        dash_btn = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/aside/div/nav/ul/li[1]/a')
        dash_btn.click()
        time.sleep(5)


    def another_attempt():
        # ## orders
        orders_btn = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/aside/div/nav/ul/li[2]/a')
        orders_btn.click()
        time.sleep(2)

        # storing the current window handle to get back to dashboard
        main_page = driver.current_window_handle
        time.sleep(20)

        rows = driver.find_element(By.XPATH,
                                   '/html/body/div[1]/div/div/div[2]/div/section/div/div/div/div[2]/div/div[2]/div/div[2]/div/div[2]/span[2]/select')
        drop_rows = Select(rows)

        # select by visible text
        drop_rows.select_by_visible_text("100 rows")
        time.sleep(2)

        ### Find the first delivery link and click to pay
        impediment_link = driver.find_element(By.LINK_TEXT, "Confirm Impediment")
        driver.execute_script("arguments[0].scrollIntoView();", impediment_link)
        impediment_link.click()
        time.sleep(5)

        # changing the handles to access the delivery pop up
        delivery_popup = ""
        for handle in driver.window_handles:
            if handle != main_page:
                delivery_popup = handle

        # change the control to the delivery page
        driver.switch_to.window(delivery_popup)

        # #modal
        impediment_options = driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div/div/form/div[1]/select')
        drop_impediment = Select(impediment_options)
        # impediment_options.click()
        # "//*[@id="response"]"

        # select by visible text
        drop_impediment.select_by_visible_text("Buyer and I have agreed to another delivery attempt")
        time.sleep(2)

        submit_btn = driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div/div/form/div[2]/input')
        driver.execute_script("arguments[0].scrollIntoView();", submit_btn)
        submit_btn.click()
        time.sleep(10)

        # change control to main page
        driver.switch_to.window(main_page)

        try:
            ok_btn = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[4]/div/button')
            driver.execute_script("arguments[0].scrollIntoView();", ok_btn)
            ok_btn.click()
            time.sleep(10)
        except NoSuchElementException:
            ok_btn = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[4]/div/button')
            driver.execute_script("arguments[0].scrollIntoView();", ok_btn)
            ok_btn.click()
            time.sleep(10)
        # "/html/body/div[3]/div/div[4]/div/button"

        dash_btn = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/aside/div/nav/ul/li[1]/a')
        dash_btn.click()
        time.sleep(5)


    def raise_dispute_order():
        # ## orders
        orders_btn = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/aside/div/nav/ul/li[2]/a')
        orders_btn.click()
        time.sleep(2)

        # storing the current window handle to get back to dashboard
        main_page = driver.current_window_handle
        time.sleep(20)

        rows = driver.find_element(By.XPATH,
                                   '/html/body/div[1]/div/div/div[2]/div/section/div/div/div/div[2]/div/div[2]/div/div[2]/div/div[2]/span[2]/select')
        drop_rows = Select(rows)

        # select by visible text
        drop_rows.select_by_visible_text("100 rows")
        time.sleep(2)

        ### Find the first delivery link and click to pay
        dispute_link = driver.find_element(By.LINK_TEXT, "Raise Dispute")
        driver.execute_script("arguments[0].scrollIntoView();", dispute_link)
        dispute_link.click()
        time.sleep(5)

        # changing the handles to access the dispute pop up
        dispute_popup = ""
        for handle in driver.window_handles:
            if handle != main_page:
                dispute_popup = handle

        # change the control to the dispute form
        driver.switch_to.window(dispute_popup)

        # #modal

        subject_input = driver.find_element(By.XPATH,
                                            '/html/body/div[1]/div/div/div[2]/div/div/section/div/div/div/div/div[2]/div/div/input')
        driver.execute_script("arguments[0].scrollIntoView();", subject_input)
        subject_input.send_keys("Issue with my order")

        dispute_desc_input = driver.find_element(By.XPATH,
                                                 '/html/body/div[1]/div/div/div[2]/div/div/section/div/div/div/div/div[3]/div/div/textarea')
        driver.execute_script("arguments[0].scrollIntoView();", dispute_desc_input)
        dispute_desc_input.send_keys(
            "Issue with my order. The buyer does not want to pay for the goods which has already been opened.")

        # attachment_input = driver.find_element(By.XPATH,
        #                                          '/html/body/div[1]/div/div/div[2]/div/div/section/div/div/div/div/div[4]/div/div/input')
        # driver.execute_script("arguments[0].scrollIntoView();", attachment_input)
        # attachment_input.click()
        # time.sleep(5)

        send_btn = driver.find_element(By.XPATH,
                                       '/html/body/div[1]/div/div/div[2]/div/div/section/div/div/div/div/button')
        driver.execute_script("arguments[0].scrollIntoView();", send_btn)
        send_btn.click()
        time.sleep(10)

        # change control to main page
        driver.switch_to.window(main_page)

        try:
            ok_btn = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[4]/div/button')
            driver.execute_script("arguments[0].scrollIntoView();", ok_btn)
            ok_btn.click()
            time.sleep(10)
        except NoSuchElementException:
            ok_btn = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[4]/div/button')
            driver.execute_script("arguments[0].scrollIntoView();", ok_btn)
            ok_btn.click()
            time.sleep(10)
        # "/html/body/div[3]/div/div[4]/div/button"

        dash_btn = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/aside/div/nav/ul/li[1]/a')
        dash_btn.click()
        time.sleep(5)


    def raise_dispute():
        # ## orders
        dispute_btn = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/aside/div/nav/ul/li[5]/a')
        dispute_btn.click()
        time.sleep(2)

        # storing the current window handle to get back to dashboard
        main_page = driver.current_window_handle
        time.sleep(20)

        rows = driver.find_element(By.XPATH,
                                   '/html/body/div[1]/div/div/div[2]/div/section/div/div/div/div[2]/div/div[2]/div/div[2]/div/div[2]/span[2]/select')
        drop_rows = Select(rows)

        # select by visible text
        drop_rows.select_by_visible_text("100 rows")
        time.sleep(2)

        ### Find the first delivery link and click to pay
        dispute_link = driver.find_element(By.LINK_TEXT, "Raise Dispute")
        driver.execute_script("arguments[0].scrollIntoView();", dispute_link)
        dispute_link.click()
        time.sleep(5)

        # changing the handles to access the dispute pop up
        dispute_popup = ""
        for handle in driver.window_handles:
            if handle != main_page:
                dispute_popup = handle

        # change the control to the dispute form
        driver.switch_to.window(dispute_popup)

        # #modal

        subject_input = driver.find_element(By.XPATH,
                                            '/html/body/div[1]/div/div/div[2]/div/div/section/div/div/div/div/div[2]/div/div/input')
        driver.execute_script("arguments[0].scrollIntoView();", subject_input)
        subject_input.send_keys("Issue with my order")

        dispute_desc_input = driver.find_element(By.XPATH,
                                                 '/html/body/div[1]/div/div/div[2]/div/div/section/div/div/div/div/div[3]/div/div/textarea')
        driver.execute_script("arguments[0].scrollIntoView();", dispute_desc_input)
        dispute_desc_input.send_keys(
            "Issue with my order. The buyer does not want to pay for the goods which has already been opened.")

        # attachment_input = driver.find_element(By.XPATH,
        #                                          '/html/body/div[1]/div/div/div[2]/div/div/section/div/div/div/div/div[4]/div/div/input')
        # driver.execute_script("arguments[0].scrollIntoView();", attachment_input)
        # attachment_input.click()
        # time.sleep(5)

        send_btn = driver.find_element(By.XPATH,
                                       '/html/body/div[1]/div/div/div[2]/div/div/section/div/div/div/div/button')
        driver.execute_script("arguments[0].scrollIntoView();", send_btn)
        send_btn.click()
        time.sleep(10)

        # change control to main page
        driver.switch_to.window(main_page)

        try:
            ok_btn = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[4]/div/button')
            driver.execute_script("arguments[0].scrollIntoView();", ok_btn)
            ok_btn.click()
            time.sleep(10)
        except NoSuchElementException:
            ok_btn = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[4]/div/button')
            driver.execute_script("arguments[0].scrollIntoView();", ok_btn)
            ok_btn.click()
            time.sleep(10)
        # "/html/body/div[3]/div/div[4]/div/button"

        dash_btn = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/aside/div/nav/ul/li[1]/a')
        dash_btn.click()
        time.sleep(5)


    def cancel_dispute():
        # ## orders
        dispute_btn = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/aside/div/nav/ul/li[5]/a')
        dispute_btn.click()
        time.sleep(2)

        # storing the current window handle to get back to dashboard
        main_page = driver.current_window_handle
        time.sleep(20)

        rows = driver.find_element(By.XPATH,
                                   '/html/body/div[1]/div/div/div[2]/section/div/div/div/div/div/div[2]/div/div[2]/div/div[2]/span[2]/select')
        drop_rows = Select(rows)

        # select by visible text
        drop_rows.select_by_visible_text("100 rows")
        time.sleep(2)

        ### Find the first cancel dispute link and click
        cancel_link = driver.find_element(By.LINK_TEXT, "Cancel Dispute")
        driver.execute_script("arguments[0].scrollIntoView();", cancel_link)
        cancel_link.click()
        time.sleep(5)

        # changing the handles to access the dispute pop up
        dispute_popup = ""
        for handle in driver.window_handles:
            if handle != main_page:
                dispute_popup = handle

        # change the control to the dispute form
        driver.switch_to.window(dispute_popup)

        # #modal

        try:
            cancel_btn = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[3]/button[2]')
            driver.execute_script("arguments[0].scrollIntoView();", cancel_btn)
            cancel_btn.click()
            time.sleep(10)
        except NoSuchElementException:
            cancel_btn = driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div[3]/button[2]')
            driver.execute_script("arguments[0].scrollIntoView();", cancel_btn)
            cancel_btn.click()
            time.sleep(10)

        # change control to main page
        driver.switch_to.window(main_page)

        try:
            error_text = driver.find_element(By.XPATH, '/html/body/div[3]/div').text
            print(error_text)
            # Take a screenshot
            now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot_cancel = f"error_screenshot_{now}.png"
            driver.save_screenshot(screenshot_cancel)
            # Print the error message
            print(f"Error occurred: {error_text}")
        except NoSuchElementException:
            pass

        try:
            ok_btn = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[4]/div/button')
            driver.execute_script("arguments[0].scrollIntoView();", ok_btn)
            ok_btn.click()
            time.sleep(10)
        except NoSuchElementException:
            ok_btn = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[4]/div/button')
            driver.execute_script("arguments[0].scrollIntoView();", ok_btn)
            ok_btn.click()
            time.sleep(10)

        dash_btn = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/aside/div/nav/ul/li[1]/a')
        dash_btn.click()
        time.sleep(5)


    def add_service_provider():
        # ## myp2p
        orders_btn = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/aside/div/nav/ul/li[2]/a')
        orders_btn.click()
        time.sleep(2)

        # storing the current window handle to get back to dashboard
        main_page = driver.current_window_handle
        time.sleep(20)

        rows = driver.find_element(By.XPATH,
                                   '/html/body/div[1]/div/div/div[2]/div/section/div/div/div/div[2]/div/div[2]/div/div[2]/div/div[2]/span[2]/select')
        drop_rows = Select(rows)

        # select by visible text
        drop_rows.select_by_visible_text("100 rows")
        time.sleep(2)

        ### Find the first SP link and click
        sp_link = driver.find_element(By.LINK_TEXT, "Add Service Provider")
        driver.execute_script("arguments[0].scrollIntoView();", sp_link)
        sp_link.click()
        time.sleep(5)

        # changing the handles to access the sp pop up
        sp_popup = ""
        for handle in driver.window_handles:
            if handle != main_page:
                sp_popup = handle

        # change the control to the sp page
        driver.switch_to.window(sp_popup)

        # #modal
        try:
            sp_options = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/select')
            drop_sp = Select(sp_options)

        except NoSuchElementException:
            sp_options = driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div[2]/select')
            drop_sp = Select(sp_options)

        # select by visible text
        drop_sp.select_by_visible_text("Yemi Provider (yemi.smtp01@gmail.com)")
        time.sleep(2)

        try:
            input_commi = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/input')
            driver.execute_script("arguments[0].scrollIntoView();", input_commi)
            input_commi.clear()
            input_commi.send_keys("10")

        except NoSuchElementException:
            input_commi = driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div[2]/input')
            driver.execute_script("arguments[0].scrollIntoView();", input_commi)
            input_commi.clear()
            input_commi.send_keys("10")

        try:
            assign_btn = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[3]/button[1]')
            driver.execute_script("arguments[0].scrollIntoView();", assign_btn)
            assign_btn.click()
            time.sleep(10)
        except NoSuchElementException:
            assign_btn = driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div[3]/button[1]')
            driver.execute_script("arguments[0].scrollIntoView();", assign_btn)
            assign_btn.click()
            time.sleep(10)

        # change control to main page
        driver.switch_to.window(main_page)

        try:
            ok_btn = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[4]/div/button')
            driver.execute_script("arguments[0].scrollIntoView();", ok_btn)
            ok_btn.click()
            time.sleep(10)

        except NoSuchElementException:
            ok_btn = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[4]/div/button')
            driver.execute_script("arguments[0].scrollIntoView();", ok_btn)
            ok_btn.click()
            time.sleep(10)

        dash_btn = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/aside/div/nav/ul/li[1]/a')
        dash_btn.click()
        time.sleep(5)


    ######################### CALL THE FUNCTIONS #############################

    if test_scope == "buyer login and logout":
        buyer_login()
        buyer_logout()

    if test_scope == "buyer creates p2p" or test_scope == "buyer creates p2p with new seller":
        buyer_login()
        buyer_creates_p2p()
        buyer_logout()

    if test_scope == "seller creates p2p" or test_scope == "seller creates p2p with new buyer":
        seller_login()
        seller_creates_p2p()
        seller_logout()

    if test_scope == "make payment":
        buyer_login()
        make_payment()
        buyer_logout()

    if test_scope == "escrow accept":
        seller_login()
        escrow_delivery()
        seller_logout()
        buyer_login()
        escrow_accept()
        buyer_logout()

    if test_scope == "buyer accepts":
        buyer_login()
        escrow_accept()
        buyer_logout()

    if test_scope == "end to end":
        seller_login()
        seller_creates_p2p()
        seller_logout()
        # MAKE PAYMENT
        buyer_login()
        make_payment()
        buyer_logout()
        # SELLER DELIVERS
        seller_login()
        escrow_delivery()
        seller_logout()
        # BUYER ACCEPTS
        # buyer_login()
        # escrow_accept()
        # buyer_logout()
        # BUYER REJECTS
        buyer_login()
        escrow_reject_no_fee()
        buyer_logout()
        # ANOTHER ATTEMPT BY SELLER
        seller_login()
        another_attempt()
        seller_logout()
        # SELLER DELIVERS
        seller_login()
        escrow_delivery()
        seller_logout()
        # ANOTHER ATTEMPT BY BUYER
        buyer_login()
        escrow_reject_no_fee()
        buyer_logout()
        # SELLER CONFIRMS NOT OK
        seller_login()
        seller_confirms_not_ok()
        seller_logout()
        # BUYER CANCELS DISPUTE
        buyer_login()
        cancel_dispute()
        buyer_logout()

    if test_scope == "seller delivers":
        seller_login()
        escrow_delivery()
        seller_logout()

    if test_scope == "add service provider":
        seller_login()
        add_service_provider()
        seller_logout()

    if test_scope == "buyer rejects":
        buyer_login()
        escrow_reject_no_fee()
        buyer_logout()

    if test_scope == "seller confirms ok":
        seller_login()
        seller_confirms_ok()
        seller_logout()

    if test_scope == "seller confirms not ok":
        seller_login()
        seller_confirms_not_ok()
        seller_logout()

    if test_scope == "another attempt":
        seller_login()
        another_attempt()
        seller_logout()

    if test_scope == "raise dispute from order":
        seller_login()
        raise_dispute_order()
        seller_logout()

    if test_scope == "seller cancels dispute":
        seller_login()
        cancel_dispute()
        seller_logout()

    if test_scope == "buyer cancels dispute":
        buyer_login()
        cancel_dispute()
        # buyer_logout()

    # if test_scope == "end to end":
    #     seller_login()
    #     seller_creates_p2p()
    #     seller_logout()
    #     buyer_login()
    #     make_payment()
    #     buyer_logout()
    #     seller_login()
    #     escrow_delivery()
    #     seller_logout()
    #     buyer_login()
    #     escrow_accept()
    #     buyer_logout()

    if test_scope == "seller login":
        seller_login()

    if test_scope == "buyer login":
        buyer_login()

    if test_scope == "seller agrees":
        seller_login()
        seller_agrees()
        seller_logout()

    if test_scope == "seller disagrees":
        seller_login()
        seller_disagrees()
        seller_logout()

    driver.quit()
