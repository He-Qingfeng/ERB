import os

municipalities = ["北京市", "上海市", "天津市", "重庆市"]
autonomous_regions_order = [
    "西藏自治区", "内蒙古自治区", "广西壮族自治区",
    "宁夏回族自治区", "新疆维吾尔自治区"
]

def get_provinces(base_path):
    provinces = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    provinces_sorted = (
        [p for p in municipalities if p in provinces] +
        sorted([p for p in provinces if p not in municipalities and p not in autonomous_regions_order]) +
        [p for p in autonomous_regions_order if p in provinces]
    )
    return provinces_sorted

def get_dirs(path):
    return sorted([d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))])

def generate_readme(base_path):
    readme_path = os.path.join(base_path, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write("# 目录\n\n")

        provinces = get_provinces(base_path)
        for province in provinces:
            # 一级目录，省或直辖市，不带链接
            f.write(f"<details>\n<summary><span style='font-size:20px;font-weight:bold'>{province}</span></summary>\n\n")

            province_path = os.path.join(base_path, province)

            if province in municipalities:
                # 直辖市，二级目录是区县，要跳转链接，缩进1个空格
                subdirs = get_dirs(province_path)
                if len(subdirs) == 1 and subdirs[0] == "市辖区":
                    shixiaqu_path = os.path.join(province_path, "市辖区")
                    counties = get_dirs(shixiaqu_path)
                    for county in counties:
                        county_link = f"[{county}]({province}/市辖区/{county})"
                        f.write(f" - <span style='font-size:16px'>{county_link}</span>\n")
                else:
                    for county in subdirs:
                        county_link = f"[{county}]({province}/{county})"
                        f.write(f" - <span style='font-size:16px'>{county_link}</span>\n")

            else:
                # 省，二级目录是市，不带链接，缩进1个空格
                cities = get_dirs(province_path)
                for city in cities:
                    f.write(f" <details>\n <summary><span style='font-size:16px'>{city}</span></summary>\n\n")
                    city_path = os.path.join(province_path, city)
                    counties = get_dirs(city_path)
                    # 三级目录是区县，要跳转链接，缩进2个空格，字号14px
                    for county in counties:
                        county_link = f"[{county}]({province}/{city}/{county})"
                        f.write(f"  - <span style='font-size:14px'>{county_link}</span>\n")
                    f.write("\n </details>\n")

            f.write("\n</details>\n\n")

if __name__ == "__main__":
    base_path = os.path.dirname(os.path.abspath(__file__))
    generate_readme(base_path)