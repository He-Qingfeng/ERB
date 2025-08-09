import os

# 直辖市、省、自治区分类
municipalities = ["北京市", "上海市", "天津市", "重庆市"]
autonomous_regions_order = ["西藏自治区", "内蒙古自治区", "广西壮族自治区", "宁夏回族自治区", "新疆维吾尔自治区"]

# 获取当前目录下的所有一级目录（省/自治区/直辖市）
def get_provinces(base_path):
    provinces = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    # 排序逻辑：直辖市→其他省→自治区（按给定顺序）
    provinces_sorted = (
        [p for p in municipalities if p in provinces] +
        sorted([p for p in provinces if p not in municipalities and p not in autonomous_regions_order]) +
        [p for p in autonomous_regions_order if p in provinces]
    )
    return provinces_sorted

# 获取地级市目录
def get_cities(province_path):
    return sorted([d for d in os.listdir(province_path) if os.path.isdir(os.path.join(province_path, d))])

# 获取县区目录
def get_counties(city_path):
    return sorted([d for d in os.listdir(city_path) if os.path.isdir(os.path.join(city_path, d))])

# 生成 README.md
def generate_readme(base_path):
    readme_path = os.path.join(base_path, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write("# 目录\n\n")

        provinces = get_provinces(base_path)
        for province in provinces:
            f.write(f"<details>\n<summary>{province}</summary>\n\n")
            province_path = os.path.join(base_path, province)

            # 直辖市：省下直接是区县
            if province in municipalities:
                counties = get_counties(province_path)
                for county in counties:
                    f.write(f"  - [{county}]({province}/{county})\n")
            else:
                # 省份/自治区：省下是地级市
                cities = get_cities(province_path)
                for city in cities:
                    f.write(f"  <details>\n  <summary>{city}</summary>\n\n")
                    counties = get_counties(os.path.join(province_path, city))
                    for county in counties:
                        f.write(f"    - [{county}]({province}/{city}/{county})\n")
                    f.write(f"\n  </details>\n")
            f.write("\n</details>\n\n")

if __name__ == "__main__":
    base_path = os.path.dirname(os.path.abspath(__file__))  # 脚本所在目录
    generate_readme(base_path)