from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from rembg import *
from io import BytesIO
from PIL import Image
import uuid
import os
app = FastAPI()

@app.post("/remove_bg")
async def remove_bg_api(file: UploadFile = File(...)):
    content = await file.read()
    image = Image.open(BytesIO(content))
    model = "u2net"
    session = new_session(model)
    image = remove(image,session=session)
    buffered = BytesIO()
    image.save(buffered, format="png")
    buffered.seek(0)
     # 使用 uuid 生成唯一文件名
    filename = f"{str(uuid.uuid4())}.png"
    filename = os.path.join("./output", filename)
    # 将处理后的图像数据写入到文件
    with open(filename, "wb") as f:
        f.write(buffered.getvalue())
    # 返回文件响应
    return FileResponse(filename)

