
# FastAPI with Machine Learning

## Author
Muhammad Ahsan

## Project Overview
This project demonstrates the integration of machine learning with FastAPI, enabling robust API management along with advanced image processing capabilities. The application allows users to upload images, which are then processed to detect and crop faces using machine learning techniques.

## Features
- **Image Upload**: Users can upload images for processing.
- **Face Detection**: Implements facial recognition to identify faces in the uploaded images.
- **Image Cropping**: Automatically crops the detected faces from the images.
- **API Management**: Utilizes FastAPI for efficient management of backend operations, including request handling and response sending.

## Technologies Used
- **FastAPI**: As the core framework to create RESTful APIs.
- **OpenCV**: For image processing tasks.
- **MediaPipe**: Used for accurate face detection in images.
- **Docker**: For containerizing the application and ensuring consistency across different deployment environments.

## Getting Started

### Prerequisites
- Python 3.8+
- Docker (for deployment)

### Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/fastapi-machine-learning.git
   cd fastapi-machine-learning
   ```

2. **Set up a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running Locally
To run the application locally, execute:
```bash
uvicorn app.main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.

## API Endpoints
- `POST /upload-image/`: Uploads an image and returns the image with detected faces.
- `GET /docs`: Access the automatically generated Swagger UI to interact with the API directly.

## Docker Deployment
To build and run the Docker container:
```bash
docker build -t fastapi-ml .
docker run -p 8000:8000 fastapi-ml
```

## Contributing
Contributions are welcome! Please fork the project and submit a pull request, or create an issue to suggest changes or report bugs.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact Information
- Muhammad Ahsan - [your-email@example.com](mailto:your-email@example.com)
- Project Link: [https://github.com/yourusername/fastapi-machine-learning](https://github.com/yourusername/fastapi-machine-learning)
