from zai import ZaiClient

client = ZaiClient(api_key="aaa40df3ad354a00a516cad9d0bb5cdb.CYSCyGYeBeZE25Xz")

response = client.chat.completions.create(
    model="glm-4.6v",
    messages=[
        {
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://cloudcovert-1305175928.cos.ap-guangzhou.myqcloud.com/%E5%9B%BE%E7%89%87grounding.PNG"
                    },
                },
                {
                    "type": "text",
                    "text": "Where is the second bottle of beer from the right on the table? Provide coordinates in [[xmin,ymin,xmax,ymax]] format",
                },
            ],
            "role": "user",
        }
    ],
    thinking={"type": "enabled"},
)

print(response.choices[0].message)
