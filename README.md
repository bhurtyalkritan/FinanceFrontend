# Fidelity Interview Prep

**Fidelity Interview Prep** is a comprehensive Streamlit application designed to assist candidates in preparing for technical interviews at Fidelity. The application integrates with a Spring Boot API to manage and explore data related to users, portfolios, assets, and transactions. Additionally, it offers advanced SQL querying capabilities, educational content on Object-Oriented Programming (OOP), and detailed API documentation.

## Table of Contents

- [Features](#features)
- [Demo](#demo)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Authentication](#authentication)
  - [Tabs Overview](#tabs-overview)
- [Advanced SQL Queries](#advanced-sql-queries)
- [Object-Oriented Programming (OOP) Tutorials](#object-oriented-programming-oop-tutorials)
- [API Documentation](#api-documentation)
- [Deployment](#deployment)
  - [Deploying Spring Boot API](#deploying-spring-boot-api)
  - [Deploying Streamlit App](#deploying-streamlit-app)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

- **User Management**: View and manage user data.
- **Portfolio Management**: Explore user portfolios.
- **Asset Management**: Analyze assets within portfolios.
- **Transaction Management**: Monitor transactions related to assets.
- **Health Check**: Verify the health status of the API.
- **User Count**: Display the total number of users.
- **Advanced SQL Querying**: Perform complex SQL queries on the loaded data.
- **Object-Oriented Programming (OOP) Tutorials**: Learn the four pillars of OOP with examples and diagrams.
- **API Documentation**: Comprehensive documentation of all API endpoints.

## Demo

<img width="1470" alt="image" src="https://github.com/user-attachments/assets/c9f6cf0c-7f97-41db-b0ff-3714ac57acea">


## Installation

### Prerequisites

- **Python 3.7+**
- **Git**
- **Java (for Spring Boot API)**

### Clone the Repository

```bash
git clone https://github.com/yourusername/fidelity-interview-prep.git
cd fidelity-interview-prep
```

### Set Up a Virtual Environment

It's recommended to use a virtual environment to manage dependencies.

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install Python Dependencies

```bash
pip install -r requirements.txt
```

Note: Ensure that `requirements.txt` includes all necessary packages:

```
streamlit
requests
pandas
pandasql
graphviz
```

Additionally, install the Graphviz system package:

Ubuntu/Debian:

```bash
sudo apt-get install graphviz
```

macOS (using Homebrew):

```bash
brew install graphviz
```

Windows:

Download and install Graphviz from [Graphviz Download](https://graphviz.org/download/).

## Configuration

### Spring Boot API

Ensure that your Spring Boot API is running and accessible at `http://localhost:8080/api`. Update the `BASE_URL` in the Streamlit application if your API is hosted elsewhere.

### Environment Variables

You can set environment variables for authentication if required. For simplicity, the default credentials are set to:

Username: `admin`
Password: `admin123`

Modify these in the Streamlit sidebar as needed.

## Usage

### Running the Application

Activate your virtual environment and run the Streamlit app:

```bash
streamlit run app.py
```

Replace `app.py` with the actual filename if different.

### Authentication

Upon launching the application, navigate to the sidebar to enter your API credentials:

- Username: Default is `admin`
- Password: Default is `admin123`

### Tabs Overview

The application is organized into several tabs, each serving a distinct purpose:

#### Users

- View all users.
- Automatically loads user data on startup.

#### Portfolios

- Explore portfolios associated with users.
- Automatically loads portfolio data based on loaded users.

#### Assets

- Analyze assets within each portfolio.
- Automatically loads asset data based on loaded portfolios.

#### Transactions

- Monitor transactions related to each asset.
- Automatically loads transaction data based on loaded assets.

#### Health Check

- Verify the health status of the API.
- Provides real-time status information.

#### User Count

- Displays the total number of users.
- Automatically calculates based on loaded user data.

#### Advanced SQL Query

- Perform custom and pre-made SQL queries on the loaded data.
- Includes a variety of complex query examples for in-depth analysis.

#### OOP

- Educational content on Object-Oriented Programming.
- Covers the four pillars: Encapsulation, Inheritance, Polymorphism, and Abstraction with examples and diagrams.

#### Docs

- Comprehensive API documentation.
- Details all available endpoints and data schemas.
- Links to Swagger UI for interactive API exploration.

## Advanced SQL Queries

The Advanced SQL Query tab allows you to perform complex queries on the loaded datasets. It includes both custom query input and a selection of pre-made queries covering various scenarios:

- Users with Most Portfolios
- Assets with Highest Total Value
- Transactions Summary per Asset
- Users with No Portfolios
- Portfolios with No Assets
- Top 5 Most Traded Assets
- Average Asset Value per Portfolio
- Users with Portfolios Exceeding a Total Value
- Assets Purchased in Last 30 Days
- Users by Age Group
- Assets Distribution by Type
- Transactions Above Average Quantity
- Portfolios with Diversified Assets
- Inactive Users (No Transactions)
- Top Performing Assets by Return Rate
- Custom Subquery
- Window Functions Example

To use the pre-made queries:

1. Select the desired query from the dropdown menu.
2. Provide any necessary parameters (e.g., value thresholds).
3. Click the corresponding button to execute the query.
4. View the results displayed in a table format.

To write a custom query:

1. Enter your SQL query in the provided text area.
2. Click "Run Advanced SQL Query" to execute.
3. The results will be displayed below.

Example Custom Query:

```sql
SELECT u.name, COUNT(p.id) AS portfolio_count
FROM users u
JOIN portfolios p ON u.id = p.userId
GROUP BY u.name
HAVING portfolio_count > 2
```

## Object-Oriented Programming (OOP) Tutorials

The OOP tab provides in-depth tutorials on the four pillars of Object-Oriented Programming:

1. Encapsulation
2. Inheritance
3. Polymorphism
4. Abstraction

Each section includes:

- Detailed explanations.
- Runnable Python code examples.
- Visual diagrams using Graphviz.

## API Documentation

The Docs tab offers comprehensive documentation for all API endpoints provided by the Spring Boot backend. It includes:

- Overview: Base URL and general information.
- Controllers:
  - User Controller
  - Portfolio Controller
  - Asset Controller
  - Transaction Controller
  - Home Controller
- Schemas:
  - User
  - Portfolio
  - Asset
  - Transaction
  - PageUser
  - PageableObject
  - SortObject
- Swagger UI: Link to interactive API documentation.

### Accessing Swagger UI

For interactive API exploration and testing, access the Swagger UI at:

```bash
http://localhost:8080/swagger-ui/index.html
```

Note: Ensure that the Spring Boot API server is running to access Swagger UI.

## Deployment

### Deploying Spring Boot API

You can deploy your Spring Boot API for free using platforms like Render.com, Railway.app, Fly.io, or Oracle Cloud Free Tier. Follow these general steps:

1. Choose a Cloud Platform: Select one from Render.com, Railway.app, Fly.io, or Oracle Cloud Free Tier.
2. Create an Account and Set Up:
   - Sign up for the chosen platform.
   - Connect your GitHub repository containing the Spring Boot project.
3. Configure Deployment:
   - Set build and start commands.
   - Configure environment variables (e.g., PORT).
4. Deploy:
   - Initiate the deployment process.
   - Monitor build logs for any issues.
5. Access the API:
   - Once deployed, the platform will provide a URL to access your API.
   - Update the `BASE_URL` in the Streamlit application accordingly.

Refer to the Deployment section or individual platform documentation for step-by-step instructions.

### Deploying Streamlit App

To deploy the Streamlit application, consider platforms like Streamlit Sharing, Heroku, or Render.com.

#### Using Streamlit Sharing

1. Sign Up for Streamlit Sharing:
   - Visit Streamlit Sharing and request access if you haven't already.
2. Push Your Code to GitHub:
   - Ensure your Streamlit app code is in a GitHub repository.
3. Deploy:
   - In Streamlit Sharing, connect your GitHub account.
   - Select the repository and branch containing your app.
   - Specify the entry file (e.g., `app.py`).
4. Run and Share:
   - Streamlit Sharing will build and deploy your app.
   - Access the provided URL to view your application.

#### Using Heroku

1. Install Heroku CLI:

   ```bash
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. Log In to Heroku:

   ```bash
   heroku login
   ```

3. Create a New Heroku App:

   ```bash
   heroku create your-app-name
   ```

4. Deploy:
   - Add a Procfile with the following content:

     ```
     web: streamlit run app.py --server.port=$PORT --server.enableCORS false
     ```

   - Push to Heroku:

     ```bash
     git add .
     git commit -m "Deploy to Heroku"
     git push heroku main
     ```

5. Access Your App:
   - Visit `https://your-app-name.herokuapp.com` to view your Streamlit application.

#### Using Render.com

1. Create an Account on Render.com.
2. Create a New Web Service:
   - Connect your GitHub repository.
   - Specify build and start commands.
3. Deploy:
   - Render.com will build and deploy your app automatically.
   - Access the provided URL to view your application.

## Contributing

Contributions are welcome! Follow these steps to contribute:

1. Fork the Repository.
2. Create a New Branch:

   ```bash
   git checkout -b feature/YourFeature
   ```

3. Make Changes.
4. Commit and Push:

   ```bash
   git commit -m "Add your feature"
   git push origin feature/YourFeature
   ```

5. Open a Pull Request.

## License

This project is licensed under the MIT License.
