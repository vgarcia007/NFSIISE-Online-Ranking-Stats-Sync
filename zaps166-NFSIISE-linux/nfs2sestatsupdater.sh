#!/bin/bash

# Start Dir
start_dir="/home/$USER/.nfs2se/stats"
config_file="/home/$USER/.nfs2se/config/config.dat"
LOG_FILE="logfile.txt"

# Check if the log file exists, if not, create it
if [ ! -e "$LOG_FILE" ]; then
    touch "$LOG_FILE"
fi

log_message() {
    local message="$1"
    # Add timestamp to the message
    local timestamp=$(date +"%Y-%m-%d %H:%M:%S")
    echo "[$timestamp] $message" >> "$LOG_FILE"
}

# Array for the stf files
srt_files=()

# Loop files
for file in "$start_dir"/*.stf; do
    if [ -f "$file" ]; then
        srt_files+=("$file")
    fi
done

# send files to api
log_message "Uploading stats"
for srt_file in "${srt_files[@]}"; do
    
    echo "Uploading stats for $srt_file"


    curl --silent --output /dev/null --location https://garcias-garage.de/nfs2se-ranking/post_v2 \
    --form stf=@"$srt_file" \
    --form config=@"$config_file"

done

# array of tracks to download times for
track_files=("oval.stf" "oz.stf" "last.stf" "nort.stf" "pac.stf" "med.stf" "myst.stf" "mono.stf")

log_message "Downloading stats"

for TRACK in "${track_files[@]}"; do

    echo "Downloading stats for $start_dir/$TRACK"

    curl -o "$start_dir/$TRACK" --silent "https://garcias-garage.de/nfs2se-ranking/download/$TRACK"

done
