# Database Structure Documentation

## Overview

This document outlines the structure of the database system, which consists of 4 main entities: `admin`, `config`, `doc_db`, and `local`. The database appears to be a MongoDB implementation designed to support a document management system with user authentication, session tracking, and system logging capabilities.

## Entities

### 1. `admin`

An empty entity that likely exists for MongoDB administrative purposes.

### 2. `config`

An empty entity, possibly reserved for system configuration settings.

### 3. `doc_db`

The primary data entity containing three collections that store application data:

#### 3.1 `documents` Collection

Stores document files and their associated metadata.

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `_id` | ObjectId | Unique identifier for the document | `ObjectId('67cdeb8f05aba3ef435c300c')` |
| `filename` | String | Name of the stored file | `"CS408_Project_Fall24 (1).pdf"` |
| `file_data` | Binary | Binary content of the file | Binary data (Base64 encoded) |
| `metadata` | Object | Additional information about the document | Varies |

#### 3.2 `sessions` Collection

Tracks user sessions and conversation history.

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `_id` | ObjectId | Unique identifier for the session record | `ObjectId('67c5e1f057a273c032a35899')` |
| `user_id` | String | Reference to the user who owns this session | `"1"` |
| `session_id` | ObjectId | Identifier for the session itself | `ObjectId('67c5e1f057a273c032a35898')` |
| `conversation` | Array | Collection of conversation exchanges | Array of objects |
| `created_at` | DateTime | Timestamp when the session was created | `2025-03-03T17:08:00.031+00:00` |

#### 3.3 `users` Collection

Manages user accounts and authentication information.

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `_id` | ObjectId | Unique identifier for the user record | `ObjectId('67cdde9566dbeaf9e3883198')` |
| `email` | String | User's email address, used for login | `"admin@sabanciuniv.edu"` |
| `password` | String | User's password (Note: appears to be stored in plaintext) | `"admin"` |
| `role` | String | User's role defining permissions | `"admin"` |
| `created_at` | DateTime | Timestamp when the user account was created | `2025-03-09T21:31:49.804+00:00` |

### 4. `local`

Contains system-level information, particularly focused on MongoDB instance details.

#### 4.1 `startup_log` Collection

Records information about MongoDB server startups.

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `_id` | String | Unique identifier for the startup event | `"LAPTOP-B741STJU-1738260825417"` |
| `hostname` | String | Name of the host machine | `"LAPTOP-B741STJU"` |
| `startTime` | DateTime | UTC timestamp of server startup | `2025-01-30T18:13:45.000+00:00` |
| `startTimeLocal` | String | Local timestamp as a formatted string | `"Thu Jan 30 21:13:45.417"` |
| `cmdLine` | Object | Command line arguments used to start the server | Varies |
| `pid` | Integer | Process ID of the MongoDB instance | `34312` |
| `buildinfo` | Object | Information about the MongoDB build | Varies |

## Relationships

- `doc_db` contains the collections `documents`, `sessions`, and `users`
- `local` contains the collection `startup_log`
- `admin` and `config` are currently empty entities

## Security Considerations

1. **Password Storage**: The current implementation appears to store passwords as plaintext in the `users` collection. It is strongly recommended to implement hashing with a secure algorithm (like bcrypt or Argon2) for password storage.

2. **User Roles**: The system has at least one role type (`admin`), suggesting a role-based access control system that should be properly enforced in application logic.

## Usage Notes

- The `documents` collection stores files as binary data, allowing for document retrieval and management
- The `sessions` collection tracks user interactions, maintaining state across user visits
- The `startup_log` provides system diagnostics that can be useful for troubleshooting and auditing

## Recommended Improvements

1. Implement secure password storage with hashing
2. Consider adding indexes for commonly queried fields
3. Add versioning for documents if needed
4. Consider implementing soft delete functionality for documents
5. Add validation rules for each collection