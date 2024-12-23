import requests
import subprocess
# 检查更新
def check_update():
    url = "https://api.github.com/repos/CatIsNotFound/ShellToolbox/releases/latest"
    try: 
        response = requests.get(url)  
        if response.status_code  == 200: 
            return response.json()
        else: 
            return 201
    except requests.ConnectionError as e:
        return 101
    except requests.ConnectTimeout as e:
        return 102
    except requests.HTTPError as e:
        return 103

# 获取软件包下载路径
def get_pack_url(pack_json, version_type):
    pack_count = len(pack_json['assets'])
    for i in range(0, pack_count):
        if pack_json['assets'][i]['browser_download_url'].endswith(f'.{version_type}'):
            return pack_json['assets'][i]['browser_download_url']

# 安装或解压软件包
def install_pack(pack:str):
    # print("开始安装/解压...")
    if pack.endswith(".zip"):
        # print("OK~")
        command = f"unzip -o {pack}"
    else:
        return "Debian"
    from funcs.main import get_output
    return get_output(command, "stderr")

# 下载软件包 
def download_file(url, destination):  
    print(f"正在从 {url} 获取 {destination}...") 
    try: 
        response = requests.get(url)   
        response.raise_for_status()  
    except requests.exceptions.ConnectionError  as e: 
        return f"连接错误: {e}" 
    except requests.exceptions.RequestException  as e: 
        return f"请求错误: {e}" 
    try: 
        with open(destination, 'wb') as file:  
            for chunk in response.iter_content(chunk_size=1024):    
                file.write(chunk)    
    except PermissionError as e: 
        return "没有权限下载软件包! 需要管理员或 root 身份执行! " 
    except (FileNotFoundError, IOError) as e: 
        return f"文件操作错误: {e}" 

# 是否为最新版本
def is_newer_version(tag1, tag2): 
    return tag1 != tag2
    
def main(tag_name):
    print("正在检查更新...")
    packs = check_update()
    if packs == 201:
        print("Error(201): 找不到对应更新! 检查获取更新的 URL 是否准确.")
    elif packs == 101:
        print("Error(101): 网络连接错误! 请检查网络! ")
    elif packs == 102:
        print("Error(102): 网络连接超时! 尝试换个网络环境? ")
    elif packs == 103:
        print("Error(103): 连接或解析 HTTP 失败! ")
    else:
        if is_newer_version(packs["tag_name"], tag_name):
            print(f'获取新版本: {packs["tag_name"]}')
            opt = input("检查到有更新版本，是否确认更新软件? (y/n) ")
            if opt == 'y':
                print("正在下载软件包...")
                pack_url = get_pack_url(packs, 1)
                err_code = download_file(pack_url, pack_url.split("/")[-1])
                if err_code != 0:
                    print(f"Error: 下载软件包失败! \n {err_code}")
                print("下载完成，请自行解压并重启软件. ")

        else:
            print("软件已是最新版本！")

if __name__ == '__main__':
    json = check_update()
    with open(".update_info.json", 'w', encoding='utf-8') as file:
        file.write(json)
        file.close()