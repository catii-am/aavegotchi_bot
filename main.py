import random
import re
import subprocess
from math import sqrt
import requests
import undetected_chromedriver.v2 as uc
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from multiprocessing import Pool
import time, cv2, json, copy, numpy as np
from fake_useragent import UserAgent
from collections import defaultdict
import os
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
import cv2
# import mss
import numpy as np
from selenium import webdriver
from PIL import Image
import io



class Selenium:
    def __init__(self, mnemonic, profile_name) -> None:
        split = re.split('@',mnemonic)
        self.mnemonicc = split[0]
        self.proxyy = f"--proxy-server={split[-1]}"
        self.profile_name = str(profile_name)
        pass

    def start_driver(self, mnemonic, profile_name):
        # time.sleep(random.randint(1,10))
        options = uc.ChromeOptions()
        options.add_argument('--no-first-run')
        options.add_argument('--no-service-autorun')
        options.add_argument('--password-store=basic')
        if len(re.split('@', mnemonic)) > 1:
            proxy = f"--proxy-server={re.split('@', mnemonic)[1]}"
            options.add_argument(proxy)

        options.add_argument('--load-extension=C:\\utils\\RO,C:\\utils\\MM')
        driver = uc.Chrome(
            options=options,
            executable_path = f'undetected_chromedriver/{str(profile_name)}.exe'
        )
        self.driver = driver
        self.driver.set_window_size(1280,900)
        self.ac = ActionChains(driver)
        return driver

    def take_element(self, path, timeout=20, delay=0):
        element = ""
        try:
            element = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(("css selector", path)))
        except Exception as e:
            print(f"No element after {timeout} seconds of waiting!!!")
            return None
        if element is not None:
            time.sleep(delay)
            return element
        else:
            print(f"NO SUCH ELEMENT!\n Path: {path}")
        self.driver.execute_script("""document.body.style.backgroundColor = 'green'""")
        input()

    def refresh(self):
        self.driver.refresh()

    def check_element(self, path):
        element = self.driver.find_elements_by_xpath(path)
        if len(element) > 0:
            random.choice(122, 223, 334)

    def del_extra_element(self, path):
        self.driver.execute_script(f'document.querySelector("{path}").remove();')

    def send_keys_delay(element, string, delay=0):
        for character in string:
            element.send_keys(character)
            time.sleep(delay)

    def hold_key(self, key, delay=0):
        ac = ActionChains(self.driver)
        ac.key_down(key).pause(delay).key_up(key).perform()

    def send_key(self, key):
        ac = ActionChains(self.driver)
        ac.send_keys(key).perform()

    def key_down(self, key):
        ac = ActionChains(self.driver)
        ac.key_down(key).perform()

    def key_up(self, key):
        ac = ActionChains(self.driver)
        ac.key_up(key).perform()


class Metamask(Selenium):
    def __init__(self, mnemonic, password, driver) -> None:
        split = re.split('@',mnemonic)
        self.mnemonic = split[0]
        self.proxy = f"--proxy-server={split[-1]}"
        self.password = password
        self.driver = driver

    def installMM(self, path_mm):
        while True:
            if len(self.driver.window_handles) > 1:
                self.driver.close()
                print('MM installed')
                break
            else:
                time.sleep(1)

    def restore_wallet(self):
        while True:
            try:
                self.take_element("button").click()  # enter mm
                break
            except Exception as e:
                self.refresh()
        self.take_element("button").click()  # choose restoration by mnemonic
        self.take_element("button").click()  # don't send telemetry
        self.take_element("input").send_keys(self.mnemonic)  # put mnemonic
        self.take_element("#password").send_keys(self.password)  # put password
        self.take_element("#confirm-password").send_keys(self.password)  # repeat password
        self.take_element(".first-time-flow__terms", timeout=60).click()  # agree terms
        self.take_element("button").click()  # login to mm
        self.take_element("button[role='button']", timeout=60).click()  # access invitation

    def add_network(self, network, rpc, chain_id, currency, explorer):
        self.driver.get(self.driver.current_url.split('#')[0] + "#settings/networks/add-network")
        network_inputs = self.take_element(".networks-tab__add-network-form-body").find_elements("css selector",
                                                                                                 ".form-field__input")
        Metamask.send_keys_delay(network_inputs[0], network)
        Metamask.send_keys_delay(network_inputs[1], rpc)
        Metamask.send_keys_delay(network_inputs[2], chain_id)
        Metamask.send_keys_delay(network_inputs[3], currency)
        Metamask.send_keys_delay(network_inputs[4], explorer)
        self.take_element("button.button:nth-child(2)").click()  # save network
        time.sleep(2)

class Aavegotchi(Metamask):
    def __init__(self, driver, profile_name) -> None:
        self.driver = driver
        self.profile_name = str(profile_name)

    def go_to_site(self):
        self.driver.get("https://verse.aavegotchi.com/")
        return self

    def login(self):
        print("Login")
        # input("Press Enter to continue...")
        time.sleep(3)
        connect_mm = self.take_element(".retro-border > button", timeout=10, delay=1)  # connect mm
        if not connect_mm: return
        connect_mm.click()
        choose_mm = self.take_element('.wallet-card', timeout=10, delay=1)
        if not choose_mm: return
        choose_mm.click()  # choose mm
        time.sleep(3)
        if len(self.driver.window_handles) > 1:
            self.driver.switch_to.window(self.driver.window_handles[1])  # go to mm window
            self.take_element('.btn-primary').click()  # confirm mm
            self.take_element('.btn-primary').click()  # confirm double mm
            self.driver.switch_to.window(self.driver.window_handles[0])  # go to main window

    def prepare_game(self):
        # time.sleep(30)
        self.take_element('.lazyload-wrapper').click()  # choose aavegotchi
        for i in range(4):
            portal = self.take_element('.selected-gotchi-container', delay=1)  # choose portal
            portal.click()  # go to portal
            # time.sleep(1)
            self.take_element('.random-spawn-container').click()
            time.sleep(5)
            self.driver.switch_to.window(self.driver.window_handles[1])  # go to mm window
            self.take_element('.btn-primary').click()  # sign mm
            if self.take_element('.btn-primary'):
                self.take_element('.btn-primary').click()  # sign mm again
            self.driver.switch_to.window(self.driver.window_handles[0])  # go to main window
            time.sleep(15)
            upd_portal = self.take_element('.selected-gotchi-container', timeout=0.5)
            if upd_portal is None:
                return True
        return True

    def is_game_loaded(self):
        return bool(self.take_element(".input[value='40']", 100, delay=10))  # check for loading game

    def increase_vision(self):
        self.increase_measure()
        extra_dom_elements = [".bottom-right-container"]
        for el in extra_dom_elements:
            self.del_extra_element(el)
            self.send_key("m")

    def increase_measure(self):
        measure_input = self.take_element("input[type='range']")
        time.sleep(2)
        ac = ActionChains(self.driver)
        for i in range(20):
            ac.click_and_hold(measure_input).move_by_offset(0, 120).release().perform()
            time.sleep(5)
            if self.take_element(".input[value='0']", timeout=0.5):
                return

    def check_crystals_airdrop(self):
        self.upd_map()
        rejoice_img = cv2.imread(f'photos\\rejoice.png')
        map_img = cv2.imread(f'photos\\map_{str(self.profile_name)}.png')
        # map_img = map_img[550:760, 500:580] # resize img
        result = cv2.matchTemplate(rejoice_img, map_img, cv2.TM_SQDIFF)
        min_val = cv2.minMaxLoc(result)[0]
        return min_val < 1000

    def is_crystals_airdrop(self, timeout=230):
        start = time.time()
        while not self.check_crystals_airdrop():
            if time.time() - start > timeout:
                return
        return True

    def _grouped_crystas(crystals_location):
        counter = defaultdict(int)
        length = len(crystals_location)
        while length:
            crystal = crystals_location[length - 1]
            counter[json.dumps(crystal)] += 1
            for crystal_ in copy.deepcopy(crystals_location):
                if crystal != crystal_ and (
                ((abs(crystal[0] - crystal_[0]) < 5) and (abs(crystal[1] - crystal_[1]) < 5))):
                    del crystals_location[crystals_location.index(crystal_)]
                    counter[json.dumps(crystal)] += 1
                    length -= 1
            length -= 1
        return dict(counter)

    def _get_crystals_locations(self):
        click = 0

        data = self.driver.get_screenshot_as_png()

        img = Image.open(io.BytesIO(data))
        numpy_array = np.asarray(img)
        # img = np.array(sct.grab(monitor))
        frame = cv2.cvtColor(numpy_array, cv2.COLOR_RGB2BGR)
        frame_HSV = cv2.rectangle(frame, (0, 575), (300, 875), (255, 255, 255), -1)

        crystals = {
            "green": {  # ^
                "lower": [0, 223, 0],
                "upper": [0, 223, 0]
            }
        }

        # here
        crystal_locations = []
        for crystal in list(reversed(crystals)):
            lower = np.array(crystals[crystal]["lower"])  # BGR-code of your lowest colour
            upper = np.array(crystals[crystal]["upper"])  # BGR-code of your highest colour
            mask = cv2.inRange(frame_HSV, lower, upper)
            coord = cv2.findNonZero(mask)
            if coord is not None:
                for i in range(len(coord)):
                    crystal_locations.append(coord[i][0].tolist())
                return crystal_locations
        return []

    def distance(self, x_1, y_1, x_2, y_2):
        return sqrt((x_2 - x_1) ** 2 + (y_2 - y_1) ** 2)

    def nearest_crystal(self):
        crystals_location = self._get_crystals_locations()
        if len(crystals_location) == 0:
            return None

        group_crystals = Aavegotchi._grouped_crystas(crystals_location)
        min_distance = {"X": 0, "Y": 0, "distance": 10 ** 10}
        for group in group_crystals:
            X, Y = json.loads(group)
            dis = self.distance(X, Y, 642, 437)
            if min_distance["distance"] > dis:
                # min_distance = {"X": X+5, "Y": Y-5, "distance": dis}
                min_distance = {"X": X, "Y": Y, "distance": dis} #here
        return min_distance

    def upd_map(self):
        self.driver.save_screenshot(f'photos\\map_{str(self.profile_name)}.png')

    def _move_to(self, X, Y):
        ac = ActionChains(self.driver)
        el = self.driver.find_element("css selector", "canvas")
        ac.click_and_hold().move_to_element_with_offset(el, X, Y).release().perform()

    def play_game(self, work_time=20, sleep_time=40):
        double_check = False
        time.sleep(5)
        used_work_time = work_time
        while True:
            # test_all = time.time()
            # used_sleep_time = sleep_time - (used_work_time - work_time)
            print("Sleep! used_work_time:", used_work_time)
            time.sleep(sleep_time - (used_work_time - work_time))
            print("Work!")
            start = time.time()
            used_work_time = 0
            while double_check or (used_work_time < work_time):

                self.upd_map()
                nearest_crystal_location = self.nearest_crystal()
                X, Y = nearest_crystal_location["X"], nearest_crystal_location["Y"]

                double_check = False
                if X or Y:
                    self._move_to(X, Y+5)
                    print("Stop MOVE!")
                    ac = ActionChains(self.driver)
                    ac.release().perform()
                    double_check = True
                used_work_time = time.time() - start
                # print("all:", time.time() - test_all)

    def test(self):
        A = 0
        choice_key = ' '
        fake_crystal = 0
        move_x_list = [
            70,
            640,
            1160
        ]
        move_y_list = [
            30,
            440,
            800
        ]
        ac = None
        el = None
        Flag = True
        nearest_crystal_location = None
        cnt = 0
        tmove = 0
        treload = 0

        while True:
            self.check_element('/html/body/div[1]/div[3]/div/div/h2')
            tmove += 1
            # treload += 1
            if Flag:
                nearest_crystal_location = self.nearest_crystal()
            X = 0
            Y = 0

            if ac == None:
                ac = ActionChains(self.driver)
                el = self.driver.find_element("css selector", "canvas")

            if nearest_crystal_location:
                if choice_key != ' ':
                    self.key_up(choice_key)
                    A = 0
                    choice_key = ' '
                Flag = False
                X, Y = nearest_crystal_location["X"], nearest_crystal_location["Y"]
                # print(f'{X}, {Y}')
                if X or Y:
                    if 625 < X < 665 or 415 < Y < 450:
                        fake_crystal += 1
                    ac.click_and_hold().perform()
                    if fake_crystal > 3:
                        time.sleep(7)
                    else:
                        time.sleep(0.005)
                    ac.move_to_element_with_offset(el, X, Y).perform()
                    nearest_crystal_location = self.nearest_crystal() #here
            else:
                if A == 0:
                    sleep = random.randint(30,50)
                    choice_key = random.choice(['w', 'a', 's', 'd'])
                    self.key_down(choice_key)
                if A > sleep:
                    self.key_up(choice_key)
                    A = 0
                else:
                    A += 1
                Flag = True
                fake_crystal = 0
                cnt=cnt+1
                if cnt>10 and choice_key == ' ':
                    cnt = 0
                    ac.move_to_element(el).perform()
                    ac.release().perform()
                    fake_crystal = 0
                    choice_key = ' '

            if tmove > 6000:
                move_x = random.choice(move_x_list)
                move_y = random.choice(move_y_list)
                if move_x == 640 and move_y == 440:
                    move_x = random.choice(70, 1160)
                    move_y = random.choice(30, 800)
                ac.reset_actions()
                ac.move_by_offset(move_x, move_y).click_and_hold().perform()
                time.sleep(7)
                ac.release().perform()
                ac.reset_actions()
                tmove = 0
            if treload > 72000:
                treload = 0
                random.choice(122, 223, 334)


def make_list_from_file(file):
    with open(file, 'r') as f:
        return [x for x in f.read().split("\n") if x]


def worker(account):
    change_graphic = 0
    profile_name, mnemonic, password = account
    print("Start with:", profile_name, mnemonic, password)
    driver = ''
    while True:
        try:
            driver_session = Selenium(mnemonic, profile_name)
            driver = driver_session.start_driver(mnemonic, profile_name)
            metamask = Metamask(mnemonic, password, driver)
            if len(driver.window_handles) > 1:
                driver.close()
            driver.switch_to.window(driver.window_handles[0])
            with open('RO.txt') as f:
                driver.get(f.readline())
            element = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="d1"]/div[2]/div/div[3]/input'))
            )
            driver.find_element_by_xpath('//*[@id="d1"]/div[2]/div/div[3]/input').send_keys(
                'https://verse-static.aavegotchi.com/animations/pickups_x3.png')
            driver.find_element_by_xpath('//*[@id="d1"]/div[2]/div/div[5]/input').send_keys(
                'https://i.ibb.co/dKCTtgm/rgb-conv.png')
            print('RO added')
            time.sleep(1)

            metamask.installMM(os.getenv("METAMASK_PATH"))
            driver.switch_to.window(driver.window_handles[0])  # switch to mm window
            print("MetaMask was started")
            metamask.restore_wallet()
            print("add Polygon")
            metamask.add_network("Matic Mainnet", "https://rpc-mainnet.maticvigil.com/", "137", "MATIC",
                                 "https://explorer.matic.network/")
            print("Polygon added")
            # metamask.Install_RO("RO_PATH")
            # metamask.settings_RO()
            break
        except Exception as e:
            print(e)
            driver.quit()

    aavegotchi = Aavegotchi(driver, profile_name)

    while True:
        try:
            aavegotchi.go_to_site().login()
            print("Prepare game")
            if change_graphic == 0:
                time.sleep(1)
                driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/header/div[2]/button').click()
                driver.find_element(By.XPATH, '//*[@id="portal"]/div/div/div/div[1]/div[3]/div/div[2]/label/span').click()
                driver.find_element(By.XPATH, '//*[@id="portal"]/div/div/div/div[1]/div[3]/div/div[4]/label/span').click()
                driver.find_element(By.XPATH, '//*[@id="portal"]/div/div/div/div[1]/div[3]/div/div[5]/label/span').click()
                driver.find_element(By.XPATH, '//*[@id="portal"]/div/div/div/div[1]/div[3]/div/div[6]/label/span').click()
                driver.find_element(By.XPATH, '//*[@id="portal"]/div/div/div/div[1]/div[3]/div/div[7]/label/span').click()
                # driver.find_element(By.XPATH, '').click()
                driver.find_element(By.XPATH, '//*[@id="portal"]/div/div/div/div[2]/button').click()
                change_graphic += 1
                time.sleep(1)
            if not aavegotchi.prepare_game():
                continue
            print("Aavegotchi go to portal")

            if not aavegotchi.is_game_loaded():
                print("Game Not loaded")
                continue

            print("Aavegotchi loaded")

            aavegotchi.increase_vision()
            time.sleep(300)

            aavegotchi.test()
            return

            if not aavegotchi.is_crystals_airdrop():
                continue
            print("Aavegotchi airdrop")

            aavegotchi.play_game()

            input("GG WP...")
        except Exception as e:
            print(e)

if __name__ == "__main__":
    mnemonics = make_list_from_file("accounts.txt")
    accounts = [(str(i + 1), mnemonics[i], "vegotchi" + str(i + 1)) for i in range(len(mnemonics))]
    p = Pool(processes=len(accounts))
    p.map(worker, accounts)
