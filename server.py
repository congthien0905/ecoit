import cv2
import numpy as np
from flask import Flask, jsonify, request,send_file
from flask_cors import CORS
import base64
from dotenv import load_dotenv
import io
from PIL import Image

# Thử áp dụng phương pháp adaptive thresholding để cải thiện hình ảnh
def improve_image_with_adaptive_threshold(image):
    # Chuyển đổi PIL Image thành mảng NumPy
    image_np = np.array(image)

    # Chuyển ảnh sang màu xám
    gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)

    # Áp dụng ngưỡng hóa thích ứng (adaptive thresholding)
    adaptive_thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 13
    )

    # Tạo một ảnh trắng có cùng kích thước với ảnh gốc
    white_background = np.full_like(image_np, 255)

    # Tạo mặt nạ dựa trên kết quả của ngưỡng hóa thích ứng để giữ lại văn bản màu gốc
    mask = adaptive_thresh.astype(bool)

    # Áp dụng mặt nạ để thay đổi nền thành màu trắng và giữ lại văn bản với màu sắc gốc
    white_background[mask] = image_np[mask]

    # Trả về ảnh đã xử lý
    return Image.fromarray(white_background)



app = Flask(__name__)
CORS(app)

@app.route('/improve-image', methods=['POST'])
def improve_image():
    try:
        # Lấy file ảnh từ request (phải gửi dưới dạng form-data)
        if 'image' not in request.files:
            return jsonify({"error": "No image file found"}), 400
        
        image_file = request.files['image']
        
        # Lấy tham số format từ yêu cầu (client có thể gửi "jpeg" hoặc "png")
        output_format = request.form.get('format', 'jpeg').lower()  # Mặc định là 'jpeg'
        
        # Mở file ảnh bằng PIL
        img = Image.open(image_file)

        # Cải thiện ảnh
        improved_img = improve_image_with_adaptive_threshold(img)

        # Lưu ảnh đã cải thiện vào bộ đệm
        buffered = io.BytesIO()

        # Xác định định dạng ảnh xuất ra và mimetype tương ứng
        if output_format == 'png':
            mimetype = 'image/png'
            improved_img.save(buffered, format='PNG')
        else:
            mimetype = 'image/jpeg'
            improved_img.save(buffered, format='JPEG')
        
        buffered.seek(0)

        # Trả về ảnh trực tiếp
        return send_file(buffered, mimetype=mimetype)
    except Exception as e:
        print(e)  # Debug lỗi server nếu có
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)
