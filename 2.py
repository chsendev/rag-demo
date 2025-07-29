import json
import os
from glob import glob
import csv


def merge_json_details():
    # 获取所有专业JSON文件
    json_files = glob('./tmp/*.json')

    all_data = {}

    i = 0

    for json_file in json_files:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

            # 遍历每个学校的招生信息
            for school in data['msg']['list']:
                # 获取学校名称
                dwmc = school.get('dwmc', '未知学校')

                i += len(school['detail'])
                if dwmc not in all_data:
                    all_data[dwmc] = school
                else:
                    # 如果学校名称已存在，合并详情数据
                    if 'detail' in school:
                        all_data[dwmc]['detail'].extend(school['detail'])

    # 保存合并后的数据
    with open('./tmp/all/all.json', 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    print(f"合并完成，共合并{i}条详情数据到all.json")

    # 创建CSV文件并写入数据
    with open('./tmp/all/all.csv', 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # 写入表头
        writer.writerow([
            '学校代码', '学校名称', '是否自划线院校', '所在省市', '学院名称',
            '专业代码', '专业名称', '研究方向代码', '研究方向名称', '学习方式',
            '考试方式', '招生人数', '政治科目', '外语科目', '数学科目', '专业课科目', '其他'
        ])

        # 遍历所有学校数据
        for school in all_data.values():
            # 遍历每个专业的详情
            for detail in school.get('detail', []):
                # 获取考试科目信息
                kskmz = detail.get('kskmz', [])
                oth = "空"
                if len(kskmz) > 0:
                    km1 = kskmz[0].get('km1Vo', {}).get('kskmmc', '空') + kskmz[0].get('km1Vo', {}).get('kskmdm', '空')
                    km2 = kskmz[0].get('km2Vo', {}).get('kskmmc', '空') + kskmz[0].get('km2Vo', {}).get('kskmdm', '空')
                    km3 = kskmz[0].get('km3Vo', {}).get('kskmmc', '空') + kskmz[0].get('km3Vo', {}).get('kskmdm', '空')
                    km4 = kskmz[0].get('km4Vo', {}).get('kskmmc', '空') + kskmz[0].get('km4Vo', {}).get('kskmdm', '空')

                    if len(kskmz) > 1:
                        for i, v in enumerate(kskmz[1:]):
                            km1_ = v.get('km1Vo', {}).get('kskmmc', '空') + v.get('km1Vo', {}).get(
                                'kskmdm', '空')
                            km2_ = v.get('km2Vo', {}).get('kskmmc', '空') + v.get('km2Vo', {}).get(
                                'kskmdm', '空')
                            km3_ = v.get('km3Vo', {}).get('kskmmc', '空') + v.get('km3Vo', {}).get(
                                'kskmdm', '空')
                            km4_ = v.get('km4Vo', {}).get('kskmmc', '空') + v.get('km4Vo', {}).get(
                                'kskmdm', '空')
                            oth += f"【{i}】{km1_}-{km2_}-{km3_}-{km4_}"
                        # oth = json.dumps(kskmz[1:], ensure_ascii=False)
                else:
                    print(f"没有考试科目信息 {school}")

                # 写入一行数据
                writer.writerow([
                    school.get('dwdm', ''),  # 学校代码
                    school.get('dwmc', ''),  # 学校名称
                    school.get('zhx', ''),  # 是否自划线院校
                    school.get('szss', ''),  # 所在省市
                    detail.get('yxsmc', ''),  # 学院名称
                    detail.get('zydm', ''),  # 专业代码
                    detail.get('zymc', ''),  # 专业名称
                    detail.get('yjfxdm', ''),  # 研究方向代码
                    detail.get('yjfxmc', ''),  # 研究方向名称
                    detail.get('xxfs', ''),  # 学习方式
                    detail.get('ksfsmc', ''),  # 考试方式
                    detail.get('nzsrs', ''),  # 招生人数
                    km1,  # 政治科目
                    km2,  # 外语科目
                    km3,  # 数学科目
                    km4,  # 专业课科目
                    oth
                ])
    print("CSV文件已生成：./tmp/all/all.csv")


if __name__ == "__main__":
    merge_json_details()
