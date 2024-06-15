from datetime import datetime, timedelta

import requests

from .owncloud_client import CustomClient as Client

permissions = {
    'OCS_SHARE_TYPE_USER': '0',
    'OCS_SHARE_TYPE_GROUP': '1',
    'OCS_SHARE_TYPE_LINK': '3',
    'OCS_SHARE_TYPE_REMOTE': '6',
    'R': '1',
    'U': '2',
    'UR': '3',
    'C': '4',
    'CR': '5',
    'CUR': '7',
    'D': '8',
    'RD': '9',
    'URD': '11',
    'CRD': '13',
    'CURD': '15',
    'Share': '16',
    'R + Reshare': '17',
    'UR + Reshare': '19',
    'CR + Reshare': '21',
    'CUR + Reshare': '23',
    'RD + Reshare': '25',
    'URD + Reshare': '27',
    'CRD + Reshare': '29',
    'CURD + Reshare': '31', }


def generate_upload_link_with_token(username, password, folder_path, expiretion_days):
    # Initialize Nextcloud client
    oc = Client('http://46.249.99.102:3000')
    oc.login(username, password)

    now = datetime.now()
    one_day_later = now + timedelta(days=expiretion_days)
    expiretion_time = one_day_later.strftime('%Y-%m-%d')
    share_info = {
        'perms': 1,  # Permissions: 1 (read), 15 (full control)
        'public_upload': True,  # Allow public upload
        'name': 'upload_link',  # Name of the share
        'expire': expiretion_time,
        'hide_download': True
    }
    share_id = oc.custom_params(folder_path, **share_info)

    return share_id.get_link()


def create_directory_if_does_not_exist(oc: Client, folder_path):
    try:
        folder_info = oc.file_info(folder_path)
        if 'file_type' in folder_info.__dict__ and folder_info.__dict__['file_type'] == 'dir':
            return True
        else:
            return False
    except Exception as e:
        print(f"An error occurred while checking folder existence: {e}")
        try:
            oc.mkdir(folder_path)
            return True
        except Exception as e:
            print(f"An error occurred while creating folder: {e}")
            return False


def makeGroupFolder(folder):
    # اطلاعات اتصال به Nextcloud
    base_url = "https://your-nextcloud-url.com"
    username = "admin"
    password = "admin"

    # مشخصات پوشه گروهی و Quota
    group_folder_name = folder
    quota_limit = "5MB"

    # تعیین هدرها
    headers = {"OCS-APIRequest": "true"}

    # اطلاعات برای ارسال
    data = {
        "groupid": "quota_group",
        "foldername": group_folder_name,
        "quota": quota_limit
    }

    # ایجاد پوشه گروهی با Quota
    response = requests.post(
        "http://46.249.99.102:3000/ocs/v2.php/apps/groupfolders/folders",
        headers=headers,
        data=data,
        auth=(username, password)
    )

    if response.status_code == 200:
        print("Group folder created successfully with Quota.")
    else:
        print("Error occurred:", response.text)

    upload_link = generate_upload_link_with_token(
        'admin', 'admin', group_folder_name, 2)


# def get_files_links_from_folder(username, password, directory):
#     oc = Client('http://46.249.99.102:3000')
#     oc.login(username, password)
#     files_data = dict()
#     files = oc.list(directory)
#     for file in files:
#         if file.file_type == 'file':
#             print('-----------------------')
#             print(oc.is_shared(file.get_path()))
#             print(generate_upload_link_with_token('admin', 'admin', file.get_path() + '/' + file.name, 1))
#             print(oc.is_shared(file.get_path()))
#     return files_data


# def get_files_links_from_folder(username, password, directory):
#     oc = Client('http://46.249.99.102:3000')
#     oc.login(username, password)
#     files_data = dict()
#     files = oc.list(directory)
#     for file_info in files:
#         if file_info.file_type == 'file':
#             file_path = directory + file_info.name
#             link = ('admin', 'admin', file_path, 1)
#             files_data[str(file_info.name).strip().replace('.svg', '')] = file_path
#     return files_data
if __name__ == '__main__':

    # makeGroupFolder("Saddd")
    # upload_link = generate_upload_link_with_token('admin', 'admin', 'gemmara', 2)
    get_files_links_from_folder(
        'admin', 'admin', 'DjangoApplication/Flags/circle_flags/')
    # if upload_link:
    #     print("Upload Link:", upload_link)
    # else:
    #     print("Failed to generate upload link.")
