# 3D Geometry Service

## API Endpoints

This Flask application provides a RESTful API for operations on 3D geometric shapes. Here are the available endpoints:

### Mesh Endpoints

#### Rotate Mesh

- **URL**: `/api/v1/meshes/rotation`
- **Method**: `POST`
- **Description**: Rotates a 3D mesh around the X, Y, or Z axis by a given degree.
- **Payload**:
  - `vertices`: An array of vertex coordinates. Each vertex is a list of three floats (x, y, z).
  - `rotation`: An object containing the rotation angles in degrees for the X, Y, and Z axis.
- **Success Response**:
  - **Code**: `200 OK`
  - **Content**: An object with the rotated vertices of the mesh.
- **Error Response**:
  - **Code**: `400 Bad Request`
  - **Content**: An error message indicating invalid input data.

#### Translate Mesh

- **URL**: `/api/v1/meshes/translation`
- **Method**: `POST`
- **Description**: Translates a 3D mesh by units along the X, Y, and Z axis.
- **Payload**:
  - `vertices`: An array of vertex coordinates.
  - `translation`: An object with translation distances along the X, Y, and Z axis.
- **Success Response**:
  - **Code**: `200 OK`
  - **Content**: An object with the translated vertices of the mesh.
- **Error Response**:
  - **Code**: `400 Bad Request`
  - **Content**: An error message indicating invalid input data.

### Points Endpoints

#### Convex Hull

- **URL**: `/api/v1/points/convex-hull`
- **Method**: `POST`
- **Description**: Calculates the convex hull of a set of 3D points.
- **Payload**:
  - `points`: An array of 3D points.
- **Success Response**:
  - **Code**: `200 OK`
  - **Content**: An object with the vertices of the convex hull.
- **Error Response**:
  - **Code**: `400 Bad Request`
  - **Content**: An error message indicating invalid input data.

#### Bounding Box

- **URL**: `/api/v1/points/bounding-box`
- **Method**: `POST`
- **Description**: Calculates the bounding box of a set of 3D points, optimizing the rotation for minimal volume.
- **Payload**:
  - `points`: An array of 3D points.
- **Success Response**:
  - **Code**: `200 OK`
  - **Content**: An object with the vertices of the bounding box and the rotation angles in degrees.
- **Error Response**:
  - **Code**: `400 Bad Request`
  - **Content**: An error message indicating invalid input data.

### Polygon Endpoints

#### Check Polygon Convexity

- **URL**: `/api/v1/polygons/is-convex-polygon`
- **Method**: `POST`
- **Description**: Checks if a polygon in 3D space is convex.
- **Payload**:
  - `vertices`: An array of 3D vertices.
- **Success Response**:
  - **Code**: `200 OK`
  - **Content**: An object with a boolean indicating the convexity of the polygon.
- **Error Response**:
  - **Code**: `400 Bad Request`
  - **Content**: An error message indicating invalid input data.

---

Please ensure that you provide accurate and well-formatted JSON payloads when making requests to these endpoints. Examples of valid request bodies and more detailed error messages can be found within the source code comments.


## Getting Started
Before you begin, ensure you have the following installed on your system:
- [Git](https://git-scm.com/)
- [Python 3](https://www.python.org/downloads/) (version 3.6 or later)

Set up virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

### Prerequisites
```bash
pip install -r requirements.txt
```
## Running the Application
```bash
python app.py
```
## Swagger UI
Go to http://127.0.0.1:5000/apidocs/

## Testing with Postman
1. Testing with Postman (Postman is a powerful tool for testing APIs)
2. Install Postman from Postman's website.
3. Launch Postman locally.
4. Create a new request and select the appropriate HTTP method and enter endpoint URL.
- If necessary, add headers, URL parameters, or body data.
5. Click the 'Send' button to make the request.
6. Review the response data, status code, and headers.
