from datetime import time
from time import sleep

import requests
from numpy.f2py.auxfuncs import throw_error

# 在文件开头的导入部分添加
import random

dms = [
    {
        "zydm": "085400",
        "zymc": "电子信息",
    },
    {
        "zydm": "085401",
        "zymc": "新一代电子信息技术（含量子技术等）",
    },
    {
        "zydm": "085402",
        "zymc": "通信工程（含宽带网络、移动通信等）",
    },
    {
        "zydm": "085403",
        "zymc": "集成电路工程",
    },
    {
        "zydm": "085404",
        "zymc": "计算机技术",
    },
    {
        "zydm": "085405",
        "zymc": "软件工程",
    },
    {
        "zydm": "085406",
        "zymc": "控制工程",
    },
    {
        "zydm": "085407",
        "zymc": "仪器仪表工程",
    },
    {
        "zydm": "085408",
        "zymc": "光电信息工程",
    },
    {
        "zydm": "085409",
        "zymc": "生物医学工程",
    },
    {
        "zydm": "085410",
        "zymc": "人工智能",
    },
    {
        "zydm": "085411",
        "zymc": "大数据技术与工程",
    },
    {
        "zydm": "085412",
        "zymc": "网络与信息安全",
    }
]

cookie = "JSESSIONID=0C924A910CA20DCC98E4ECD4E6B54F03; TS0197d085=01886fbf6e6453aaca079b8989eab66e5da5eb4b4ec5840a122387bc30957bed0ae988ee8c3c56fa001b05c591795a4556869fb1b0b8c10b5296f55e19588d29af3c5f2c6aa05d6c18ef01808bd2e8abae503ab3d073f496f921af96421d6894657f87c4a41507a4c206b735618da36022225eca0c; Hm_lvt_9c8767bf2ffaff9d16e0e409bd28017b=1745561857; _ga_8YMQD1TE48=GS1.1.1745561858.1.0.1745563018.0.0.0; _ga_RNH4PZV76K=GS1.1.1745561860.1.1.1745563028.0.0.0; aliyungf_tc=ed4fc51b64a12e0ea7c672fc5573786f5c707e03dcb164ce9942e56c7f19d9e2; JSESSIONID=57132606B76C8A10945A83A186F10C74; XSRF-CCKTOKEN=01f47d429eea0526cdff3bc5ac19b03d; CHSICC_CLIENTFLAGYZ=c8f9a44c8df8c84e8e020810f11d4bf5; CHSICC02=!wgoqcNB2MD0Y3XXzYxYLahOzddj6Y1J88xsT+peUJ6cSu9Vi+UfUWvfg8inSWAu0FGCz6XfyoxO/; CHSICC01=!Jqgw7a9e3G4vM8InVPBkiJOoJxwY2jLVnPkHxsWzaEIWF4In3aFZct4v+jsgut4pTEXPSecck1Lfyg==; Hm_lvt_3916ecc93c59d4c6e9d954a54f37d84c=1751886725,1753349287,1753769137; HMACCOUNT=BA621BBECBA88B8A; _gid=GA1.3.1064778298.1753769138; CHSICC_CLIENTFLAGZSML=cbb01b369fcd2c506b9696e007e7543d; _ga_TT7MCH8RRF=GS2.1.s1753769183$o3$g0$t1753769185$j58$l0$h0; acw_tc=ac11000117537710204973904e49a4393062b9443e9c6660da5dfd1595235e; TS01d9ac57=01886fbf6e21eff75ea63d69070a470a05ea0df2fad6e1d6ca2b32003a41ad75634681e033738f46b834e56dcb525eafa8b2402fa2855fa5c6f577282a5cbf0484731117546dc71ff794392f7f8e119144678037bdcbc2a4dd7772ab83852ae31131f9bad86c4546244ba27e423af89d3d56c21d7efe37caabe170375056404552838c275e; _ga_YZV5950NX3=GS2.1.s1753769138$o4$g1$t1753771852$j45$l0$h0; _ga=GA1.3.1811512623.1745561858; Hm_lpvt_3916ecc93c59d4c6e9d954a54f37d84c=1753771853"


def fetch_school_data(dm):
    url = "https://yz.chsi.com.cn/zsml/rs/zydws.do"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Origin": "https://yz.chsi.com.cn",
        "Referer": "https://yz.chsi.com.cn/zsml/a/zydetail.do?zydm=085400",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "cookie": cookie
    }

    all_data = []
    page_size = 10  # 每页数据量
    current_page = 1
    total_pages = 1  # 初始值，会在第一次请求后更新

    while current_page <= total_pages:
        data = {
            "zydm": dm["zydm"],
            "zymc": dm["zymc"],
            "xxfs": "2",
            # "dwlxs[0]": "syl",
            "dwlxs[0]": "all",
            "start": str((current_page - 1) * page_size),
            "curPage": str(current_page),
            "pageSize": str(page_size)
        }
        # 将固定的0.5秒睡眠改为1-5秒随机睡眠
        sleep_time = random.uniform(1, 3)
        sleep(sleep_time)
        response = requests.post(url, headers=headers, data=data)
        if response.status_code != 200:
            throw_error(response.text)

        response_data = response.json()
        all_data.extend(response_data['msg']['list'])

        # 更新总页数
        if current_page == 1:
            total_pages = response_data['msg']['totalPage']

        current_page += 1

    # 将分页获取的所有数据合并到原始响应结构中
    if all_data:
        response_data['msg']['list'] = all_data
        response_data['msg']['totalCount'] = len(all_data)

    return response_data


def fetch_school_detail(school):
    url = "https://yz.chsi.com.cn/zsml/rs/yjfxs.do"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Origin": "https://yz.chsi.com.cn",
        "Referer": f"https://yz.chsi.com.cn/zsml/zydetail.do?zydm={school['zydm']}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "cookie": cookie
    }

    data = {
        "zydm": school['zydm'],
        "zymc": school['zymc'],
        "dwdm": school['dwdm'],
        "xxfs": "2",
        "dwlxs[0]": "syl",
        "start": "0",
        "pageSize": "10"
    }

    sleep_time = random.uniform(1, 3)
    sleep(sleep_time)
    response = requests.post(url, headers=headers, data=data)
    if response.status_code != 200:
        throw_error(response.text)

    return response.json()


school_map = {}


def process_school_data():
    for v in dms:
        response_data = fetch_school_data(v)
        if response_data['msg']['list']:
            print(f"有数据{v}, len:{len(response_data['msg']['list'])}")
        else:
            print(f"没有数据{v}")

        for school in response_data['msg']['list']:
            detail_data = fetch_school_detail(school)
            if detail_data['msg']['list']:
                print(f"详情有数据{school}, len:{len(detail_data['msg']['list'])}")
            else:
                print(f"详情没有数据{school}")
            school['detail'] = detail_data['msg']['list'] if detail_data['msg']['list'] else []

        # 将结果保存为JSON文件
        import json
        n = f"./tmp/{v['zymc']}.json"
        with open(n, 'w', encoding='utf-8') as f:
            json.dump(response_data, f, ensure_ascii=False, indent=2)

            print("数据已保存到1.json文件")


# 使用示例
if __name__ == "__main__":
    # process_school_data()
    pass
