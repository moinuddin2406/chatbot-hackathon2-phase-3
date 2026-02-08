# API Contract: MCP Task Tools

## Overview
This document defines the API contracts for the MCP (Model Control Protocol) task management tools. These tools are called by the AI agent to perform operations on tasks.

## Common Request Format
All MCP tool requests follow this format:

```json
{
  "user_id": "string (required)",
  "params": "object (varies by tool)"
}
```

## Common Response Format
All MCP tool responses follow this format:

```json
{
  "success": "boolean",
  "data": "object (varies by tool and success)",
  "error": "object (present only on failure)"
}
```

### Error Object Format
```json
{
  "code": "string",
  "message": "string"
}
```

---

## Tool: add_task

### Description
Creates a new task for the specified user.

### Request Parameters
```json
{
  "user_id": "string (required)",
  "title": "string (required)",
  "description": "string (optional)"
}
```

### Response Data (on success)
```json
{
  "task_id": "string",
  "title": "string",
  "description": "string",
  "completed": "boolean",
  "created_at": "string (ISO datetime)"
}
```

### Example Request
```json
{
  "user_id": "user123",
  "title": "Buy milk",
  "description": "Get 2% milk from the grocery store"
}
```

### Example Response
```json
{
  "success": true,
  "data": {
    "task_id": "task456",
    "title": "Buy milk",
    "description": "Get 2% milk from the grocery store",
    "completed": false,
    "created_at": "2026-02-06T18:30:00Z"
  }
}
```

---

## Tool: list_tasks

### Description
Retrieves a list of tasks for the specified user, with optional filtering.

### Request Parameters
```json
{
  "user_id": "string (required)",
  "status": "string (optional, enum: 'all', 'pending', 'completed'; default: 'all')"
}
```

### Response Data (on success)
```json
{
  "tasks": [
    {
      "task_id": "string",
      "title": "string",
      "description": "string",
      "completed": "boolean",
      "created_at": "string (ISO datetime)",
      "updated_at": "string (ISO datetime)"
    }
  ]
}
```

### Example Request
```json
{
  "user_id": "user123",
  "status": "pending"
}
```

### Example Response
```json
{
  "success": true,
  "data": {
    "tasks": [
      {
        "task_id": "task456",
        "title": "Buy milk",
        "description": "Get 2% milk from the grocery store",
        "completed": false,
        "created_at": "2026-02-06T18:30:00Z",
        "updated_at": "2026-02-06T18:30:00Z"
      },
      {
        "task_id": "task789",
        "title": "Walk the dog",
        "description": "",
        "completed": false,
        "created_at": "2026-02-06T17:45:00Z",
        "updated_at": "2026-02-06T17:45:00Z"
      }
    ]
  }
}
```

---

## Tool: complete_task

### Description
Marks a task as completed for the specified user.

### Request Parameters
```json
{
  "user_id": "string (required)",
  "task_id": "string (required)"
}
```

### Response Data (on success)
```json
{
  "task_id": "string",
  "completed": "boolean",
  "updated_at": "string (ISO datetime)"
}
```

### Example Request
```json
{
  "user_id": "user123",
  "task_id": "task456"
}
```

### Example Response
```json
{
  "success": true,
  "data": {
    "task_id": "task456",
    "completed": true,
    "updated_at": "2026-02-06T19:15:00Z"
  }
}
```

---

## Tool: update_task

### Description
Updates properties of an existing task for the specified user.

### Request Parameters
```json
{
  "user_id": "string (required)",
  "task_id": "string (required)",
  "title": "string (optional)",
  "description": "string (optional)",
  "completed": "boolean (optional)"
}
```

### Response Data (on success)
```json
{
  "task_id": "string",
  "title": "string",
  "description": "string",
  "completed": "boolean",
  "updated_at": "string (ISO datetime)"
}
```

### Example Request
```json
{
  "user_id": "user123",
  "task_id": "task456",
  "title": "Buy whole milk",
  "completed": false
}
```

### Example Response
```json
{
  "success": true,
  "data": {
    "task_id": "task456",
    "title": "Buy whole milk",
    "description": "Get 2% milk from the grocery store",
    "completed": false,
    "updated_at": "2026-02-06T19:20:00Z"
  }
}
```

---

## Tool: delete_task

### Description
Deletes a task for the specified user.

### Request Parameters
```json
{
  "user_id": "string (required)",
  "task_id": "string (required)"
}
```

### Response Data (on success)
```json
{
  "task_id": "string",
  "deleted": "boolean"
}
```

### Example Request
```json
{
  "user_id": "user123",
  "task_id": "task456"
}
```

### Example Response
```json
{
  "success": true,
  "data": {
    "task_id": "task456",
    "deleted": true
  }
}
```