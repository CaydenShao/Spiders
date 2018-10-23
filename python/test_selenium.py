from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

if __name__ == '__main__':
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)")
    driver = webdriver.Ie(desired_capabilities = dcap)
    time.sleep(3)
    driver.get("http://www.baidu.com")
    assert u"百度" in driver.title
    elem = driver.find_element_by_name("wd")
    elem.clear()
    elem.send_keys(u"网络爬虫")
    elem.send_keys(Keys.RETURN)
    time.sleep(3)
    assert u"网络爬虫。" not in driver.page_source
    driver.close()