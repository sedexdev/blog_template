#!/bin/bash

# This script let's you update the metadata of an existing blog post:
# It accepts a single integer value as an argument

# During script execution
#   1. ! Content is not updated !
#   2. Leave a field blank to keep the existing value 

# check $1 was provided and is a single integer value
if [[ -z "$1" ]]; then
    echo "Error: no post ID provided. Exiting"
    exit 1
elif ! [[ "$1" =~ ^[0-9]+$ ]]; then
    echo "Error: Post ID must be a single integer value. Exiting"
    exit 1
fi

# set vars
ROOT="${HOME}/path/to/your/project"
INDEX_JSON="${ROOT}/src/index.json"
POST_ID="$1"

# get the current post data
current_post=$(jq --arg id "$POST_ID" '.posts[] | select(.id == ($id | tonumber))' "${INDEX_JSON}")

# exit if post not found
if [[ -z "$current_post" ]]; then
    echo "Error: No post found with ID ${POST_ID}. Exiting"
    exit 1
fi

# get the length of the posts array
POSTS_LENGTH=$(jq '.posts | length' "${INDEX_JSON}")

# list the existing posts and their IDs
echo "Existing posts:"
if [[ "$POSTS_LENGTH" -eq 0 ]]; then
    echo "No posts found..."
    exit 1
fi
echo ""
jq '.posts | sort_by(.id) | .[] | "\(.id) - \(.title)"' "${INDEX_JSON}"

# display post being updating
echo ""
echo "Post to update:"
echo ""
echo "${current_post}"
echo ""
# alert user that blank values will not update the post
echo "Leave a value blank to keep the current value"
echo ""

# get the title of the new post
read -p "Post title: " title
if [ -z "$title" ]; then
    title=$(echo "$current_post" | jq -r '.title')
fi

# get the image path
read -p "Image path (images/<file_name.png>): " image
if [ -z "$image" ]; then
    image=$(echo "$current_post" | jq -r '.head_img')
fi

# get the post tags
read -p "Post tags (comma separated): " tags
if [ -z "$tags" ]; then
    tags=$(echo "$current_post" | jq -r '.tags | join(",")')
fi

# get the description
read -p "Post description: " description
if [ -z "$description" ]; then
    description=$(echo "$current_post" | jq -r '.meta_description')
fi

# get related post IDs
read -p "Related post IDs (comma separated): " related
if [ -z "$related" ]; then
    related=$(echo "$current_post" | jq -r '.related | join(",")')
fi

# convert comma-separated tags to JSON array
IFS=',' read -r -a tag_array <<< "$tags"
JSON_TAGS="["
for tag in "${tag_array[@]}"; do
    trimmed_tag=$(echo "$tag" | xargs)
    JSON_TAGS+="\"${trimmed_tag}\","
done
JSON_TAGS="${JSON_TAGS%,}]"

# convert comma-separated ids to JSON array with integer values
IFS=',' read -r -a id_array <<< "$related"
RELATED="["
for id in "${id_array[@]}"; do
    trimmed_id=$(echo "$id" | xargs)
    RELATED+="${trimmed_id},"
done
RELATED="${RELATED%,}]"

# update the date
UPDATED_DATE=$(date +"%d/%m/%Y")

# update the post in the index.json file
jq --arg id "$POST_ID" --arg title "$title" --arg image "$image" --argjson tags "$JSON_TAGS" --arg description "$description" --argjson related "$RELATED" --arg updated "$UPDATED_DATE" \
    '(.posts[] | select(.id == ($id | tonumber)) | .title) = $title | 
     (.posts[] | select(.id == ($id | tonumber)) | .head_img) = $image | 
     (.posts[] | select(.id == ($id | tonumber)) | .tags) = $tags | 
     (.posts[] | select(.id == ($id | tonumber)) | .meta_description) = $description | 
     (.posts[] | select(.id == ($id | tonumber)) | .related) = $related |
     (.posts[] | select(.id == ($id | tonumber)) | .updated) = $updated' \
    "${INDEX_JSON}" > tmp.json && mv tmp.json "${INDEX_JSON}"

echo ""
echo "Post updated successfully."
