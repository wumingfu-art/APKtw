import requests, re, os, sys

USERNAME = os.environ.get('APK_USERNAME', '')
PASSWORD = os.environ.get('APK_PASSWORD', '')

session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0'})

login_page = session.get('https://apk.tw/member.php?mod=logging&action=login', timeout=15)
formhash = re.search(r'name="formhash"\s+value="(\w+)"', login_page.text)
formhash = formhash.group(1) if formhash else ''

session.post('https://apk.tw/member.php?mod=logging&action=login&loginsubmit=yes&inajax=1', data={
    'formhash': formhash, 'loginfield': 'username',
    'username': USERNAME, 'password': PASSWORD, 'cookietime': '2592000'
}, timeout=15)

sign_url = 'https://apk.tw/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=1&inajax=1'
sign_page = session.get(sign_url, timeout=15)

if '已經簽到' in sign_page.text:
    print('ℹ️ 今天已簽到'); sys.exit(0)

result = session.post(sign_url + '&submit=true', data={'formhash': formhash, 'qdxq': 'kx'}, timeout=15)
print('🎉 簽到成功！' if '簽到成功' in result.text or 'signSuc' in result.text else '⚠️ 結果不明：' + result.text[:200])
