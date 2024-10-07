# Idea Management API

Rest API that allows users to create, retrieve, and manage ideas. The application uses MongoDB as the database to store ideas and their details.

Idea is made of:
    owner_id: the id of the owner who create the idea 
    subject: the subject of the idea
    details: the details of the idea
    tags: list of string that categoriesed the idea
    
## Features

- Create new ideas with unique identifiers.
- Retrieve a specific idea by its ID.
- Fetch all ideas with optional filtering by tags.
- Delete ideas by their ID.

## API Endpoints

### Create an Idea
- **Endpoint**: `POST /idea/create`
- **Request Body**:
  ```json
  {
    "owner_id": "your_owner_id",
    "subject": "Your idea subject",
    "details": "Detailed description of the idea",
    "tags": ["tag1", "tag2"]
  }

- **Response**:
Status 201: Created

{
  "id": "generated_id"
}
Status 400: Bad Request (validation errors)

---------------------------------------

Get an Idea by ID
- **Endpoint**: GET /idea/<id>

- **Response**:
Status 200: Idea found

{
  "idea": {
    "id": "your_id",
    "owner_id": "your_owner_id",
    "subject": "Your idea subject",
    "details": "Detailed description of the idea",
    "tags": ["tag1", "tag2", "tag3"]
  }
}
Status 404: Idea not found

---------------------------------------

Get All Ideas
- **Endpoint**:: GET /ideas
Query Parameters: tag (optional, can be used multiple times)

- **Response**:
Status 200: List of ideas

{
  "ideas": [
    {
      "id": "your_id",
      "owner_id": "your_owner_id",
      "subject": "Your idea subject",
      "details": "Detailed description of the idea",
      "tags": ["tag1", "tag2"]
    },
    ...
  ]
}

---------------------------------------

Delete an Idea
- **Endpoint**: DELETE /idea/<id>

- **Response**:
Status 204: No Content (successfully deleted)
