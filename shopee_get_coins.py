from playwright.sync_api import Playwright, sync_playwright, expect
import time
import os

#登入網頁
def shopee_login(page,id,pwd): 
    try:   
        page.goto("https://shopee.tw/buyer/login",timeout=5000) 
        page.locator("input[name='loginKey']").fill(id)
        page.locator("input[name='password']").fill(pwd)
        page.locator("input[name='password']").press("Enter")   
        page.wait_for_url("https://shopee.tw/?is_from_login=true")
        return True        
    except Exception as e:
        print(e)
        return False
#登出網頁
def shoppe_logout(page):
    page.goto("https://shopee.tw/buyer/logout",timeout=5000) 

#每日簽到獲得金幣網頁
def shopee_get_coins(page):
    page.goto("https://shopee.tw/shopee-coins",timeout=5000)
    time.sleep(2)
    name = page.locator(".navbar__username").nth(0).inner_text()
    status =  page.locator(".pcmall-dailycheckin_3uUmyu").nth(0)    #點擊獲得蝦幣
    if '今日簽到獲得' in status.inner_text():
        status.click() 
        time.sleep(2000)  
    coins = page.locator('xpath=//*[@id="main"]/div/div[2]/div/main/section[1]/div[1]/div/section/a/p').nth(0).inner_text()
    print('帳號：%s 擁有蝦幣：%s，' %(name,coins),status.inner_text())  

with sync_playwright() as playwright:

    #帳密設定
    shoppe_account = [
        {'id':'0971887282','pwd':'KC775008uu'},
        {'id':'0916342811','pwd':'KC775008uu'}, 
        {'id':'0975775008','pwd':'kevin1122'}
    ]

    ss_file = "shoppe_cookies.json"     
    #browser = playwright.chromium.launch(headless=False) #顯示視窗
    browser = playwright.chromium.launch() #不顯示視窗
    if(os.path.isfile(ss_file)):
        context = browser.new_context(storage_state=ss_file) #Cookies讀入
    else:
        context = browser.new_context()
    page = context.new_page()
    #---< BEGIN > ---
    for account in shoppe_account:
        shopee_login(page,account['id'],account['pwd'])
        shopee_get_coins(page)    
        shoppe_logout(page)
    #---< END > ---
    try:
        context.storage_state(path=ss_file) #Cookies存檔
    except Exception as e:
        print(e)

    context.close()
    browser.close()    


