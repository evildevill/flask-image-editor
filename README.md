# Image Processing Web Application

This is a Flask-based web application that allows users to upload an image and apply various image processing operations. The application has been extended to support more image processing operations.

## Changes Made

The original code supported the following operations:

1. Convert image to grayscale (`cgray`)
2. Save image as webp (`cwebp`)
3. Save image as jpg (`cjpg`)
4. Save image as png (`cpng`)

The updated code now supports the following additional operations:

1. Save image as gif (`cgif`)
2. Save image as jpeg (`cjpeg`)
3. Blur the image (`cblur`)
4. Sharpen the image (`csharpen`)
5. Smooth the image (`csmooth`)
6. Emboss the image (`cemboss`)
7. Rotate the image (`crotate`)
8. Detect edges in the image (`cedges`)
9. Convert image to sepia (`csepia`)
10. Invert the image (`cinvert`)
11. Convert image to a cartoon (`ccartoon`)
12. Compress the image (`ccompress`)

## How to Run

1. Install the required packages: `pip3 install flask opencv-python flask_restful flask_limiter Pillow`

2. Run the application: `python3 main.py`

The application will start on `localhost:5000`.

## How to Use

1. Navigate to the home page (`/`).
2. Choose an image file to upload.
3. Select an operation from the dropdown menu.
4. Click the 'Submit' button to process the image.
5. The processed image will be available at the provided link.

## API

The application also provides an API endpoint (`/api/process`) for processing images. The API accepts POST requests with the image file and the operation as form data. The API supports the same operations as the web interface.

## API Usage

The API endpoint is `/api/process`. It accepts POST requests with the following parameters:

- `file`: The image file to process. This should be a multipart file upload.
- `operation`: The name of the operation to perform on the image. This should be a string.

The API supports the following operations:

- `cwebp`: Save the image as a WEBP file.
- `cjpg`: Save the image as a JPG file.
- `cpng`: Save the image as a PNG file.
- `cgif`: Save the image as a GIF file.
- `cjpeg`: Save the image as a JPEG file.
- `cblur`: Blur the image.
- `csharpen`: Sharpen the image.
- `csmooth`: Smooth the image.
- `cemboss`: Emboss the image.
- `crotate`: Rotate the image 90 degrees clockwise.
- `cedges`: Detect edges in the image.
- `csepia`: Convert the image to sepia.
- `cinvert`: Invert the image.
- `ccartoon`: Convert the image to a cartoon.
- `cgray`: Convert the image to grayscale.
- `ccompress`: Compress the image.

Here's an example of how to use the API with curl:

```bash
curl -X POST -F "operation=cgray" -F "file=@/path/to/your/image.jpg" http://localhost:5000/api/process
```

Replace `/path/to/your/image.jpg` with the path to the image file you want to process.

And here's an example of how to use the API with Python's requests library:

```python
import requests

url = "http://localhost:5000/api/process"
data = {"operation": "cgray"}
files = {"file": open("/path/to/your/image.jpg", "rb")}

response = requests.post(url, data=data, files=files)

# The response will be a JSON object containing the processed image's URL and metadata
print(response.json())
```

### Using the Fetch API in JavaScript:

```javascript
let formData = new FormData();
formData.append("operation", "cgray");
formData.append("file", new File(["/path/to/your/image.jpg"], "image.jpg"));

fetch("http://localhost:5000/api/process", {
    method: "POST",
    body: formData
})
.then(response => response.json())
.then(result => {
    console.log(result);
})
.catch(error => {
    console.error('Error:', error);
});
```

Again, replace `/path/to/your/image.jpg` with the path to the image file you want to process.

## Rate Limiting

The API uses Flask-Limiter to limit the rate of requests. The current limits are 100 requests per day, 10 requests per hour, and 1 request per minute.


## Contributing

Contributions are welcome. Please submit a pull request with any enhancements or bug fixes.