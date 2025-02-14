#!/bin/bash

# This script creates a new blog post by updating the following locations and files:
#   1. Create a new HTML file in the src/posts/templates directory
#   2. Update the src/index.json file with the new post metadata
#   3. Update the src/posts/views.py file with the new post route

# set vars
ROOT="${HOME}/path/to/your/project"
HTML_TEMPLATES="${ROOT}/src/posts/templates"
INDEX_JSON="${ROOT}/src/index.json"

# get the length of the posts array
POSTS_LENGTH=$(jq '.posts | length' "${INDEX_JSON}")

# list the existing posts and their IDs
echo "Existing posts:"
if [[ "$POSTS_LENGTH" -eq 0 ]]; then
    echo "No posts found..."
fi
echo ""
jq '.posts | sort_by(.id) | .[] | "\(.id) - \(.title)"' "${INDEX_JSON}"

if ! [[ "$POSTS_LENGTH" -eq 0 ]]; then
    echo ""
fi

# get the title of the new post
read -p "Post title: " title
# get the image path
read -p "Image path (images/<file_name.png>): " image
# get the post tags
read -p "Post tags (comma separated): " tags
# get the description
read -p "Post description: " description
# get related post IDs
read -p "Related post IDs (comma separated): " related

# set post object values

# === set post object ID ===

# if the posts array is empty, create an object with ID 1
if [[ "$POSTS_LENGTH" -eq 0 ]]; then
    NEW_ID=1
else
    # find the maximum ID in the existing posts array
    MAX_ID=$(jq '[.posts[].id] | max' "${INDEX_JSON}" 2>/dev/null || echo 0)
    NEW_ID=$((MAX_ID + 1))
fi

FLASK_PATH=$(echo "${title}" | tr 'A-Z' 'a-z' | tr ' ' '_' | tr '-' '_')
ROUTE="posts.${FLASK_PATH}"
TITLE="${title}"
DATE=$(date +"%d/%m/%Y")

# convert comma-separated tags to JSON array
IFS=',' read -r -a tag_array <<< "$tags"
JSON_TAGS="["
for tag in "${tag_array[@]}"; do
    # trim leading and trailing whitespace
    trimmed_tag=$(echo "$tag" | xargs) 
    JSON_TAGS+="\"${trimmed_tag}\","
done
JSON_TAGS="${JSON_TAGS%,}]"

HEAD_IMG="${image}"
DESCRIPTION="${description}"

# convert comma-separated ids to JSON array
IFS=',' read -r -a id_array <<< "$related"
RELATED="["
for id in "${id_array[@]}"; do
    # trim leading and trailing whitespace
    trimmed_id=$(echo "$id" | xargs) 
    RELATED+="${trimmed_id},"
done
RELATED="${RELATED%,}]"

# print a blank line
echo ""

# create a new HTML file in the src/posts/templates directory
echo "{% extends 'post_heading.html' %}
{% block post_content %}
<div class="text-xl my-16">
    <p>New post...</p>
</div>
{% endblock %}" > "${HTML_TEMPLATES}/${FLASK_PATH}.html"

# update the src/index.json file with the new post metadata
NEW_POST=$(cat <<EOF
{
    "id": ${NEW_ID},
    "path": "/${FLASK_PATH}",
    "route": "${ROUTE}",
    "title": "${TITLE}",
    "date": "${DATE}",
    "tags": ${JSON_TAGS},
    "head_img": "${HEAD_IMG}",
    "meta_description": "${DESCRIPTION}",
    "related": ${RELATED}
}
EOF
)

# append the new post to the "posts" array and save it back
jq --argjson newPost "${NEW_POST}" '.posts += [$newPost]' "${INDEX_JSON}" > tmp.json && mv tmp.json "${INDEX_JSON}"

# update the src/posts/views.py file with the new post route
echo "

@post_bp.route(\"/${FLASK_PATH}\")
def ${FLASK_PATH}() -> Response:
    \"\"\"
    Returns ${title} post template

    Returns:
        Response: app Response object
    \"\"\"
    post = get_post_data(request.path)
    related = get_related_posts(post[\"related\"])
    return render_template(\"${FLASK_PATH}.html\", post=post, related=related, title=f\"{post['title']}\")
" >> "${ROOT}/src/posts/views.py"

# display success message
echo "Post created successfully."