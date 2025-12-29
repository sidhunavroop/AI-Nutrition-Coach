import requests
import base64
import os
from openai import OpenAI

# -----------------------------
# 1️⃣ Set up key
# -----------------------------
client = OpenAI()

# -----------------------------
# 2️⃣ Image URLs
# -----------------------------
image_urls = [
    'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/5uo16pKhdB1f2Vz7H8Utkg/image-1.png',
    'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/fsuegY1q_OxKIxNhf6zeYg/image-2.png',
    'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/KCh_pM9BVWq_ZdzIBIA9Fw/image-3.png',
    'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/VaaYLw52RaykwrE3jpFv7g/image-4.png'
]

# -----------------------------
# 3️⃣ Encode images to Base64
# -----------------------------
encoded_images = []
for url in image_urls:
    response = requests.get(url)
    encoded_images.append(base64.b64encode(response.content).decode("utf-8"))

# -----------------------------
# 4️⃣ Function to send image + query to OpenAI
# -----------------------------
def generate_model_response(encoded_image, user_query):
    """
    Sends an image and a query to OpenAI GPT-4.1 or GPT-4o model and retrieves the description.
    """
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant. Answer all queries about images in 1-2 sentences."
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": user_query},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{encoded_image}"}
                }
            ]
        }
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    return response.choices[0].message.content

# -----------------------------
# 5️⃣ Query each image
# -----------------------------
user_query = "Describe the photo"

for i, image in enumerate(encoded_images, start=1):
    description = generate_model_response(image, user_query)
    print(f"Description for image {i}: {description}")
