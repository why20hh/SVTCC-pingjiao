import requests
from bs4 import BeautifulSoup
from lxml import html
import time

try:
    def submit(n, kch):
        tjurl = 'http://xspj.svtcc.edu.cn/Career/SetTeacherMeasurementResult?testID={}'.format(kch)
        header = {
            'Origin': 'http://xspj.svtcc.edu.cn',
            'Connection': 'keep-alive',
            'Host': 'xspj.svtcc.edu.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36',
            'Referer': 'http://xspj.svtcc.edu.cn/Career/TeacherMeasurement/43944'
        }
        data = {
            'asid': n
        }
        session.post(tjurl, data=data, headers=header)


    base_url = 'http://xspj.svtcc.edu.cn/Main/Login'
    xh = int(input('请输入学号：'))
    data = {
        'n': xh,
        'p': xh,
        'a': xh
    }
    session = requests.session()
    html_text = session.post(url=base_url, data=data)
    html_cp = session.post('http://xspj.svtcc.edu.cn/Career/StudentToTeacher')
    bsobj = BeautifulSoup(html_cp.content, "lxml")
    kc = 1
    for tag in bsobj.find_all("a"):
        review_url = 'http://xspj.svtcc.edu.cn' + tag.get("href")
        kch = review_url.strip().split('/')[-1]
        if 'StudentAdd' in review_url:
            pass
        else:
            review_bsObj = session.get(review_url)
            html_text = review_bsObj.content.decode("utf-8")
            content = html.etree.HTML(html_text)
            value = content.xpath('//*[@id="TestQuestiong"]/div/div/div[1]/input/@value')
            a = 0
            while a < len(value):
                if a < 27:
                    n = value[a]
                    a += 1
                    submit(n, kch)
                else:
                    value = content.xpath('//*[@id="TestQuestiong"]/div/div[29]/div[2]/input/@value')
                    n = value[0]
                    a += 1
                    submit(n, kch)
                    print('提交')
        session.post('http://xspj.svtcc.edu.cn/Career/SetTeacherMeasurementFinish?testID={}'.format(kch))
        print('第{}门课程已经评教完成'.format(kc))
        kc += 1
    print('所有课程已经评教,请登陆确认')
    print('程序10秒后自动关闭')
    time.sleep(10)
except:
    print('未知错误')
    time.sleep(10)
