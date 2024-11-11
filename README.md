# Leave Application and Approval System

This is a full-stack Leave Application and Approval System built using React, Django, and Docker. The application allows employees to apply for leave and managers to view, approve, or reject leave requests. 

## Features

- **User Roles**: Two roles - Employee and Manager.
- **Employee**: 
  - Apply for leave.
  - View status of leave applications.
- **Manager**: 
  - View leave requests with employee details in a modal.
  - Approve or reject leave requests.
  - Provide reasons for rejecting leave requests in a secondary modal.
- **Authentication**: Login functionality for both roles.
- **Real-time Notifications**: Employees get notified of approval or rejection of leave.
- **Containerized Environment**: Docker setup for easy deployment and environment consistency.

## Technologies Used

- **Frontend**: React, TailwindCSS, Lucide React icons
- **Backend**: Django, Django REST Framework
- **Database**: PostgreSQL
- **Containerization**: Docker
- **API Client**: Axios
- **Other Libraries**: `react-loader-spinner` for loading animations

## Installation and Setup

### Prerequisites

- **Docker**: Ensure Docker is installed on your system.
- **Git**: For cloning the repository.

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Snehaa-k/LeaveFlow-backend 
   cd leave-application-system
