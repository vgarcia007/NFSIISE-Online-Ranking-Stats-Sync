import os
import requests

# Function to upload files
def upload_files(start_dir, config_file):
    api_url = "https://garcias-garage.de/nfs2se-ranking/post_v2"

    # Get a list of stf files
    stf_files = [f for f in os.listdir(start_dir) if f.endswith('.stf')]

    for stf_file in stf_files:
        file_path = os.path.join(start_dir, stf_file)

        # Read the file content as bytes
        with open(file_path, 'rb') as f:
            stf_content = f.read()

        with open(config_file, 'rb') as f:
            config_content = f.read()

        # Construct the request payload
        payload = {
            'stf': (stf_file, stf_content, 'application/octet-stream'),
            'config': (config_file, config_content, 'application/octet-stream')
        }

        # Send the request
        response = requests.post(api_url, files=payload)

        # Print the response
        print(f"Uploading stats for {stf_file}: {response.status_code}")

# Function to download track files
def download_track_files(start_dir, track_files):
    download_url = "https://garcias-garage.de/nfs2se-ranking/download/{}"

    for track_file in track_files:
        response = requests.get(download_url.format(track_file))

        if response.status_code == 200:
            file_path = os.path.join(start_dir, track_file)

            # Save the downloaded file
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded stats for {track_file}")
        else:
            print(f"Failed to download stats for {track_file}: {response.status_code} - {response.text}")

if __name__ == "__main__":
    # Use AppData path for start_dir
    start_dir = os.path.join(os.getenv('AppData'), '.nfs2se', 'stats')
    config_file = os.path.join(os.getenv('AppData'), '.nfs2se', 'config', 'config.dat')

    track_files = ["oval.stf", "oz.stf", "last.stf", "nort.stf", "pac.stf", "med.stf", "myst.stf", "mono.stf"]

    # Upload files
    upload_files(start_dir, config_file)

    # Download track files
    download_track_files(start_dir, track_files)