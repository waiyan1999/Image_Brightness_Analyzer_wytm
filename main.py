import os
import cv2
import numpy as np

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse,JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from datetime import datetime
import database as db


app = FastAPI(title = "Image Brightness Analyzer" , version = "1.0.0")

os.makedirs("result",exist_ok=True)

app.mount("/result",StaticFiles(directory="result"),name="result")

app.add_middleware(CORSMiddleware, allow_origins = ["*"], allow_methods= ["*"], allow_headers = ["*"],)


def analyze_image_brightness(img_path: str , filename: str) -> dict :
    
    img = cv2.imread(img_path)
    
    if img is None:
        raise HTTPException (status_code=400 , detail= "Could not read image")
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    avg_brightness = np.mean(gray)
    
    min_val, max_val ,min_loc , max_loc = cv2.minMaxLoc(gray)
    
    #Brightness point in red
    cv2.circle(img, max_loc , 10 ,(0,0,255), 2)
    cv2.putText(img, 'Brightest',( max_loc[0]+15 , max_loc[1]),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
    
    #Darkness point in blue
    cv2.circle(img , min_loc , 10 , (255,0,0),2)
    cv2.putText(img ,"Drakest", (min_loc[0] + 15 , min_loc[1]) , cv2.FONT_HERSHEY_SIMPLEX , 0.5 , (255,0,0),1)
    
    timestamp = int(datetime.now().timestamp())
    output_filename = f"output_{timestamp}.png"
    output_path = f"result/{output_filename}"
    cv2.imwrite(output_path,img)
    
    result = {
        "average_brightness" : float (avg_brightness),
        "brightest_point" : [int(max_loc[0]), int(max_loc[1])],
        "darkest_point" : [int(min_loc[0]), int(min_loc[1])],
        "brightest_value" : float(max_val),
        "darkest_value" : float(min_val),
        "processed_img_url" : f"http://localhost:8000/result/{output_filename}"
    }
    
    
    
    
    try :
        db.insert_analysis_result(
            filename=filename,
            average_brightness=result["average_brightness"],
            brightest_value= result['brightest_value'],
            darkest_value=result['darkest_value'],
            processed_img_path=output_path
            
        )
    
    except Exception as e:
        print(f"Database Storage failed : {e}")
        
    return result
    

@app.post('/analyze/')
async def analyze_image(file : UploadFile = File(...)):
    
    if not file.content_type.startswith('image/'):
        raise HTTPException (status_code=400 , detail="File must be an image")
    
    allowed_extensions = {'.jpg','.jpeg','.png'}
    file_extension = os.path.splitext(file.filename)[1].lower()
    
    if file_extension  not in allowed_extensions :
        raise HTTPException(status_code=400,detail="File must be JPEG , JPG or PNG")
    
    tem_path = f"temp_{file.filename}"
    
    try:
        with open (tem_path,"wb") as buffer :
            content = await file.read()
            buffer.write(content)
            
        result = analyze_image_brightness(tem_path,file.filename)
    
        return result
    
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error processing Image {e}")
    
    finally:
        if os.path.exists(tem_path):
            os.remove(tem_path)


@app.get("/download/{filename}")
async def download_processed_image(filename :str):
    
    file_path = f"result/{filename}"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=400 ,detail="file Not found")
    
    
    return FileResponse(
        path=file_path,
        media_type="image/png",
        filename=filename
    )
    
@app.get("/result")
async def get_analysis_history():
    
    try:
        result = db.get_analysis_result()
        return result
    
    except Exception as e:
        raise HTTPException(status_code=400 , detail= "Error Reterving result : str({e})")
    

@app.get("/")
async def root():
    return {"message": "Image Brightness Analyzer ", "version": "1.0.0"}
    
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port= 8000)
    

