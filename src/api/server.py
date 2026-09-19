import os
import cv2
import numpy as np
import sys
from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
import base64

# Kök dizini ve modül yollarını ekle
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(root_dir)

# OpenCV DLL dizinini sisteme tanıt (Temiz Mimari - DLL kopyalamadan)
opencv_bin_dir = "C:/Users/Halil/Downloads/Programs/opencv/build/x64/vc16/bin"
if os.path.exists(opencv_bin_dir):
    if hasattr(os, 'add_dll_directory'):
        os.add_dll_directory(opencv_bin_dir)
    else:
        os.environ['PATH'] = opencv_bin_dir + os.pathsep + os.environ['PATH']

# Visual Studio CMake derleme dizinlerini Python'un arama yoluna (sys.path) ekle
build_dir_debug = os.path.join(root_dir, 'out', 'build', 'x64-Debug')
build_dir_release = os.path.join(root_dir, 'out', 'build', 'x64-Release')

if os.path.exists(build_dir_debug):
    sys.path.append(build_dir_debug)
if os.path.exists(build_dir_release):
    sys.path.append(build_dir_release)

try:
    import leaf_vision
    print("Başarılı: leaf_vision modülü (C++ motoru) yüklendi!")
except ImportError as e:
    print(f"Hata: leaf_vision modülü bulunamadı. Lütfen C++ projesini derlediğinizden emin olun. Detay: {e}")

app = FastAPI(title="LeafVision API")

# İstemci dosyaları için statik dizin (src/api/static)
static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_index():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return f.read()
    return "index.html bulunamadı."

@app.post("/process")
async def process_image(file: UploadFile = File(...)):
    # Resmi oku
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if img is None:
        return JSONResponse(status_code=400, content={"message": "Geçersiz resim dosyası."})
    
    # Geçici dosyaya kaydet (C++ motoru dosya yolu beklediği için)
    temp_path = "temp_process.jpg"
    cv2.imwrite(temp_path, img)
    
    try:
        # C++ motorunu çalıştır (Yeni Pipeline Modu)
        pipeline_data = leaf_vision.process_leaf(temp_path)
        
        result_pipeline = {}
        for step_name, img_data in pipeline_data.items():
            # Numpy dizisinden OpenCV Mat'a (Gerekirse) ve base64'e çevir
            # C++ tarafı RGB döndüğü için BGR -> RGB dönüşümü gerekebilir veya mat_to_array ona göre ayarlanmıştır.
            # OpenCV imencode BGR bekler.
            if len(img_data.shape) == 3:
                # Renkli resim (RGB -> BGR)
                img_bgr = cv2.cvtColor(img_data, cv2.COLOR_RGB2BGR)
            else:
                img_bgr = img_data
                
            _, buffer = cv2.imencode('.jpg', img_bgr, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
            img_base64 = base64.b64encode(buffer).decode('utf-8')
            result_pipeline[step_name] = f"data:image/jpeg;base64,{img_base64}"
        
        return {
            "success": True, 
            "pipeline": result_pipeline
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == "__main__":
    import uvicorn
    # Yerel erişim için 127.0.0.1 (localhost) kullanılması önerilir
    uvicorn.run(app, host="127.0.0.1", port=8000)
