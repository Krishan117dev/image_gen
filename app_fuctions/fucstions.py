import os
import re

os.environ["OPENAI_API_KEY"] = "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"
import requests

from openai import OpenAI

def generate_prompt(L2_Category, L1_Category):
    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "make sure all prompts should be in number points like 1,2,3,4,5"
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"“Create a detailed and imaginative 5 prompt that will generate an image of a {L2_Category} within the broader {L1_Category}. The prompt should set a scene that brings out the unique characteristics and environment of the {L2_Category}, ensuring that the resulting image captures its essence in a way that is distinct from other members of the {L1_Category}.”\nUse this meta-prompt as a template, filling in the specific parent class ({L1_Category}) and child class ({L2_Category}) to generate your unique image prompts"
                    }
                ]
            }
        ],
        temperature=0,
        max_tokens=2000,
    )

    prompt =response.choices[0].message.content
    
    return prompt

from openai import OpenAI

def generate_image(prompt, size="1024x1024", quality="standard", n=1):
    client = OpenAI()
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size=size,
        quality=quality,
        n=n,
    )
    image_url = response.data[0].url
    return image_url




class FileDownloader:
    def __init__(self, directory, L1_Category, L2_Category):
        self.directory = directory
        self.L1_Category = L1_Category
        self.L2_Category = L2_Category

    def download_file(self, url, file_number):
        # Create the directory if it doesn't exist
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

        # Format the filename
        filename = f"{self.L1_Category}_{self.L2_Category}_{file_number:02d}.png"

        # Full path to save the file
        full_path = os.path.join(self.directory, filename)

        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Open a file in binary write mode
            with open(full_path, "wb") as file:
                # Write the content of the response to the file
                file.write(response.content)
            print(f"File {filename} downloaded successfully.")
        else:
            print(f"Failed to download file. Status code: {response.status_code}")


def process_prompts(L2_Category, L1_Category, directory):
    prompt = generate_prompt(L2_Category, L1_Category)
    descriptions = re.split(r'\d+\.', prompt)
    descriptions = [desc.strip() for desc in descriptions if desc.strip()]
    downloader = FileDownloader(directory, L1_Category, L2_Category)
    for i, desc in enumerate(descriptions):
        image_url = generate_image(desc)
        downloader.download_file(image_url, i+1)