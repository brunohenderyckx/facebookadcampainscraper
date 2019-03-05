from selenium import webdriver
import csv
import datetime
import time


def fb_login(credentials):
    """
    Function takes in a credentials text file, first row account name, second row psw. It navigates a selenium session to 'www.facebook.com' and uses the given credentials to login
    """
    with open(credentials, 'r') as file:
        cred = file.readlines()

    driver.get('https://business.facebook.com/adsmanager/manage/campaigns?business_id=871386852915826&date=2018-10-01_2018-11-')
    driver.execute_script("document.body.style.zoom='80%'")

    a = driver.find_element_by_id('email')
    a.send_keys(cred[0])
    print("Email Id entered...")
    b = driver.find_element_by_id('pass')
    b.send_keys(cred[1])
    print("Password entered...")
    c = driver.find_element_by_id('loginbutton')
    c.click()


def scrape_url(url, rows=15):
    """
    This function takes the URL of a google ad manager campaign, and appends the campaign details to the pre-defined list
    """
    driver.get(url)
    for r in range(1, int(rows)+1):
        # print(url, r)
        try:
            name_path = '//*[@id="ads_pe_container"]/div[2]/div[2]/div[2]/div/div[3]/div/div/div/div/div[2]/div/div/div[1]/div/div/div[2]/div/div/div[1]/div[3]/div['+str(r)+']/div/div/div[1]/div/div[3]'
            name = driver.find_element_by_xpath(name_path).text

            imp_path = '//*[@id="ads_pe_container"]/div[2]/div[2]/div[2]/div/div[3]/div/div/div/div/div[2]/div/div/div[1]/div[1]/div/div[2]/div/div/div/div[3]/div['+str(r)+']/div/div/div[2]/div/div[5]/div'
            imp = driver.find_element_by_xpath(imp_path).text

            amountspent_path = '//*[@id="ads_pe_container"]/div[2]/div[2]/div[2]/div/div[3]/div/div/div/div/div[2]/div/div/div[1]/div[1]/div/div[2]/div/div/div/div[3]/div['+str(r)+']/div/div/div[2]/div/div[7]/div'
            amountspent = driver.find_element_by_xpath(amountspent_path).text

            ends_path = '//*[@id="ads_pe_container"]/div[2]/div[2]/div[2]/div/div[3]/div/div/div/div/div[2]/div/div/div[1]/div[1]/div/div[2]/div/div/div/div[3]/div['+str(r)+']/div/div/div[2]/div/div[8]/div'
            ends = driver.find_element_by_xpath(ends_path).text

            cpr_path = '//*[@id="ads_pe_container"]/div[2]/div[2]/div[2]/div/div[3]/div/div/div/div/div[2]/div/div/div[1]/div[1]/div/div[2]/div/div/div/div[3]/div['+str(r)+']/div/div/div[2]/div/div[6]/div'
            cpr = driver.find_element_by_xpath(cpr_path).text.replace('\n', ' ')

            row_text = [name, imp, amountspent, ends, cpr, url]
            results.append(row_text)

            with open('results ' + str(time.strftime('%Y-%m-%d %H-%M')) + '.csv', 'a', newline='') as fd:
                writer = csv.writer(fd)
                writer.writerow(row_text)

            if r == rows:
                with open('large_table ' + str(time.strftime('%Y-%m-%d %H-%M')) + '.csv', 'a', newline='') as f:
                    writer = csv.writer(f)
                    too_large = [url]
                    writer.writerow(too_large)
        except:
            pass



if __name__ == '__main__':
    # Locate the chrome webdriver

    driver = webdriver.Chrome(executable_path=r'C:/Users/bhenderyckx/Desktop/Jupyter Notebooks/Selenium webdriver/chromedriver.exe')
    results = []

    # Login to fb via the fb_login function
    fb_login('C:/Users/bhenderyckx/Desktop/Training/Personal Training/Python/fb scrape/cred.txt')

    # Read in a set of URLS, which will be used later pass through the scrape(url) function
    urls = []
    with open('C:/Users/bhenderyckx/Desktop/Training/Personal Training/Python/fb scrape/urls.csv', 'r') as f:
        for line in f:
            urls.append(line)

    with open('results ' + str(time.strftime('%Y-%m-%d %H-%M')) + '.csv', 'a', newline='') as fd:
        writer = csv.writer(fd)
        writer.writerow(['name', 'imp', 'amountspent', 'ends','cpr','url'])

    start_time = datetime.datetime.now()

    # Feed the FB urls to the scrape_url() function
    for i, u in enumerate(urls):
        scrape_url(u, 12)
        print('**** Analyzed {}% or {} out of {}, runtime so far: {} minutes, expected time left: {} minutes ****'.format(round( (i+1) / len(urls) * 100, 1),
                                                                                                                          i+1,
                                                                                                                          len(urls),
                                                                                                                          round((datetime.datetime.now() - start_time).seconds / 60 , 1),
                                                                                                                          round(round((datetime.datetime.now() - start_time).seconds / (i+1) * len(urls)/60,1) - round((datetime.datetime.now() - start_time).seconds / 60 , 1),1)
                                                                                                                          )
              )

    # Print the results list
    print("*** Entire list of {} urls scraped, total process took {} minutes".format(len(urls), round((datetime.datetime.now() - start_time).seconds / (i+1) * len(urls)/60,1)))
