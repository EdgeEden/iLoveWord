import requests
import uuid
import json
import time

def translate(word):
    url = 'https://fanyi.baidu.com/sug'
    data = {'kw': word}
    return str(json.loads(requests.post(url, data=data).text))
def getData():
    # 获取当前时间戳
    timestamp = int(time.time() * 10000)
    getUrl = 'https://skl.hdu.edu.cn/api/paper/new?type=0&week=4&startTime=' + str(timestamp)
    getHeaders = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Host': 'skl.hdu.edu.cn',
        'Origin': 'https://skl.hduhelp.com',
        'Pragma': 'no-cache',
        'Referer': 'https://skl.hduhelp.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'cross-site',
        # 获取当前uuid（测试发现是uuid1）
        'skl-ticket': str(uuid.uuid1()),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0',
        # 自己的token
        'X-Auth-Token': 'xxxxxxx-xxxxx-xxxxx-xxxx-xxxxxxxxxxxx'#自己的token，从浏览器请求头里复制来
    }
    response = requests.get(getUrl, headers=getHeaders)
    return json.loads(response.text)


def postData(answer):
    url = 'https://skl.hdu.edu.cn/api/paper/save'

    postHeaders = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Host': 'skl.hdu.edu.cn',
        'Origin': 'https://skl.hduhelp.com',
        'Referer': 'https://skl.hduhelp.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'skl-ticket': str(uuid.uuid1()),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0',
        'X-Auth-Token': 'xxxxxxx-xxxxx-xxxxx-xxxx-xxxxxxxxxxxx'#自己的token，从浏览器请求头里复制来
    }
    requests.post(url, headers=postHeaders, data=answer)


def getAnswer(word):

    optionList = ['A', 'B', 'C', 'D']
    transResult = translate(word['title'])
    #print(transResult)
    for option in optionList:
        if word[f'answer{option}'] in transResult:
            return option
    for option in optionList:
        transResult = translate(word[f'answer{option}'])
        if word['title'] in transResult:
            return option

        if '，' in word['title']:
            zhList = word['title'].split('，')
            if zhList[1] in transResult:
                return option
            elif zhList[0] in transResult:
                return option
        elif '...' in word['title']:
            zhList = word['title'].split('...')
            if zhList[1] in transResult:
                return option
            elif zhList[0] in transResult:
                return option
    return 'C'
if __name__ == '__main__':
    with open('answerList', 'r') as f:
        answerSource = f.read()
    answerDic = json.loads(answerSource)
    paper = getData()
    print(paper)
    answerDic['paperId'] = paper['paperId']
    print('********正在答题中.........')
    for index in range(0, 100):
        answerDic['list'][index]['input'] = getAnswer(paper['list'][index])
        answerDic['list'][index]['paperDetailId'] = paper['list'][index]['paperDetailId']
    #time.sleep(60 * 5)
    postData(json.dumps(answerDic))
    print('答题以结束')
