import uiautomator2 as u2

d = u2.connect_usb('8c34fd5fc9af')
d.screen_on()
d.unlock()
d.set_click_post_delay(3)
d.press('home')
d.set_fastinput_ime(True)
d(text='钉钉').click()

if d(text='登录').exists:
    print('need login')
    d(resourceId="com.alibaba.android.rimet:id/et_pwd_login").click()
    d.send_keys('qaz.1234')
    d(text='登录').click()
else:
    pass


d(text='工作', className='android.widget.TextView').click()
if '考勤打卡' in d.dump_hierarchy():
    d.click(100, 675)


