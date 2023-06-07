# Signed by Lumi aka. Your local brat enthusiast: Yuss
import os
import asyncio
import aiohttp
import argparse
from tqdm import tqdm

parser = argparse.ArgumentParser(
                    prog='Unstability.ai History Downloader',
                    description='Downloads your Image history to a subfolder',
                    epilog='python history_dl.py')

parser.add_argument('auth_token')

args = parser.parse_args()

history = []

async def process_image_history(auth_token):
    image_history = await fetch_image_history(auth_token)
    image_history.sort(key=lambda x: x["requested_at"])
    
    output_folder = "history_output"
    os.makedirs(output_folder, exist_ok=True)
    
    existing_images = set()
    subfolders = [f.name for f in os.scandir(output_folder) if f.is_dir()]
    for subfolder in subfolders:
        index, subfolder_id = subfolder.split("_")
        existing_images.add(subfolder_id)
    
    progress_bar = tqdm(total=len(image_history), desc="Downloading images", unit="image")
    
    semaphore = asyncio.Semaphore(16)
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for index, batch in enumerate(image_history, start=1):
            task = asyncio.ensure_future(process_batch(index, batch, output_folder, existing_images, semaphore))
            tasks.append(task)
        
        for task in asyncio.as_completed(tasks):
            await task
            progress_bar.update(1)
        
        progress_bar.close()

async def fetch_image_history(auth_token):
    url = "https://www.unstability.ai/api/image_history"
    headers = {
        "User-Agent": "Mozilla/5.0 (Nintendo 3DS; U; ; en) Version/1.7412.EU",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        "Content-Type": "application/json",
        "Cookie": f'__Secure-next-auth.session-token={auth_token}'
    }
    body = {"items": 50}
    result = []
    
    async with aiohttp.ClientSession() as session:
        while True:
            print(f"Fetching history {len(result)}")
            async with session.post(url, headers=headers, json=body) as response:
                data = await response.json()
                if(response.status != 200 or len(data) == 1):
                    print("Invalid Token or Empty history! Please doublecheck.")
                    exit(1)
                result.extend(data["results"])
                
                if "next_page_key" in data:
                    next_page_key = data["next_page_key"]
                    body["next_page_key"] = next_page_key
                else:
                    break
    
    history = result
    return result

def save_image_info(batch_folder, image_info):
    with open(os.path.join(batch_folder, "image_info.txt"), "w") as file:
        for key, value in image_info.items():
            file.write(f"{key}: {value}\n")

def check_existing_images(output_folder, batch_id):
    subfolders = [f.name for f in os.scandir(output_folder) if f.is_dir()]
    for subfolder in subfolders:
        index, subfolder_id = subfolder.split("_")
        if subfolder_id == batch_id:
            print(f"Skip existing ${batch_id}")
            return True, int(index)
    return False, -1

async def download_image(session, image_url, destination):
    async with session.get(image_url) as response:
        with open(destination, "wb") as file:
            while True:
                chunk = await response.content.read(1024)
                if not chunk:
                    break
                file.write(chunk)

async def process_batch(index, batch, output_folder, existing_images, semaphore):
    async with semaphore:
        batch_id = batch["id"].replace("REQUEST#", "")
        
        if batch_id in existing_images:
            return
        
        batch_folder_name = f"{index}_{batch_id}"
        batch_folder = os.path.join(output_folder, batch_folder_name)
        os.makedirs(batch_folder, exist_ok=True)
        
        save_image_info(batch_folder, batch["image_info"])
        
        async with aiohttp.ClientSession() as session:
            tasks = []
            for image in batch["images"]:
                image_id = image["id"].replace("IMAGE#", "")
                image_url = image["original"]
                image_filename = f"{image_id}.jpg"
                image_path = os.path.join(batch_folder, image_filename)
                
                task = asyncio.ensure_future(download_image(session, image_url, image_path))
                tasks.append(task)
            
            await asyncio.gather(*tasks)

async def delete_image_history(auth_token):
    local_history = history
    if not local_history:
        local_history = await fetch_image_history(auth_token)

    images_to_delete = []
    for request in local_history:
        print(request["image_info"])
        images_to_delete.extend([image["id"] for image in request["images"]])

    progress_bar = tqdm(total=len(images_to_delete), desc="Deleting images", unit="image")
    semaphore = asyncio.Semaphore(8)

    async with aiohttp.ClientSession() as session:
        tasks = []
        for image_id in images_to_delete:
            task = asyncio.ensure_future(delete_image(auth_token, image_id, semaphore))
            tasks.append(task)

        for task in asyncio.as_completed(tasks):
            await task
            progress_bar.update(1)

        progress_bar.close()


async def delete_image(auth_token, image_id, semaphore):
    url = "https://www.unstability.ai/api/deleteImage"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Content-Type": "application/json",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "Cookie": f'__Secure-next-auth.session-token={auth_token}'
    }
    payload = {"id": image_id}

    async with semaphore:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                status = response.status

                if status == 200:
                    print(f"Successfully deleted {image_id}")
                elif status == 429:
                    retry_after = response.headers.get("Retry-After")
                    if retry_after:
                        retry_time = int(retry_after)
                    else:
                        retry_time = 10

                    print(f"Rate limited. Retrying in {retry_time} seconds...")
                    await asyncio.sleep(retry_time)
                    return await delete_image(auth_token, image_id, semaphore)
                else:
                    response_text = await response.text()
                    print(f"Failed to delete {image_id} (status: {status}). Response: {response_text}")

                return status == 200



backup_preference = input("Do you want to make a backup by downloading all images + prompts before you delete them? (yes / no): ")

if backup_preference.lower() in ["yes", "y"]:    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(process_image_history(args.auth_token))


loop = asyncio.get_event_loop()
loop.run_until_complete(delete_image_history(args.auth_token))

