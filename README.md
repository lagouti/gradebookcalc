
# GradebookCalc: A Modular Grade Calculation Application

GradebookCalc is a web-based tool designed to parse, analyze, and calculate student grades based on curriculum and grade files. It provides a step-by-step user interface to load data, review student performance, and compute detailed, weighted semester averages.

## 🚀 How to Run the Application

To get the application running on your local machine, follow these simple steps.

### 1\. Prerequisites

  - **Python 3.8** or newer installed on your system.
  - **pip** (Python's package installer).

### 2\. Clone the Repository

First, clone this repository to your local machine using Git:

```bash
git clone https://github.com/lagouti/gradebookcalc.git
cd gradebookcalc
```

### 3\. Set Up a Virtual Environment

It is highly recommended to use a virtual environment to manage project dependencies and avoid conflicts with other Python projects.

  - **Create the environment:**

    ```bash
    python -m venv venv
    ```

  - **Activate the environment:**

      - On **macOS/Linux**:
        ```bash
        source venv/bin/activate
        ```
      - On **Windows**:
        ```bash
        .\venv\Scripts\activate
        ```

### 4\. Install Dependencies

With the virtual environment active, install the required Python packages using the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

This will install **Flask** and any other necessary libraries.

### 5\. Run the Flask Application

Now you are ready to start the web server.

```bash
flask run
```

You will see output in your terminal indicating that the server is running, typically on `http://127.0.0.1:5000`.

```
 * Serving Flask app 'gradebook_calc'
 * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
```

Open this URL in your web browser to start using GradebookCalc.

-----

## 🏛️ Application Architecture

GradebookCalc is designed with a modular and separated architecture, making it easier to maintain, debug, and extend. The application is split into a **Frontend** user interface and a **Backend** server that handles all business logic.

### Frontend

The frontend is a single-page application built with standard web technologies, ensuring a responsive and interactive user experience without needing a complex JavaScript framework.

  - **`templates/index.html`**: This is the core file for the user interface. It contains all the HTML structure for the accordion layout, modals, buttons, and display areas.
  - **Tailwind CSS**: A utility-first CSS framework used for styling. It is included via a CDN link in the `<head>` of the HTML file, allowing for rapid and consistent styling without writing custom CSS.
  - **Vanilla JavaScript**: All client-side interactivity is handled by plain JavaScript embedded within a `<script>` tag in `index.html`. This script manages:
      - **State**: A simple `appState` object tracks the application's status (e.g., which files are loaded, which student is selected).
      - **API Calls**: Uses the `fetch()` API to communicate with the backend REST endpoints.
      - **DOM Manipulation**: Dynamically updates the UI to display file lists, tables, summaries, and results based on data received from the backend.
      - **UI Logic**: Controls the behavior of the accordion, enables/disables buttons, and handles user interactions.

### Backend

The backend is powered by **Flask**, a lightweight Python web framework. It exposes a series of RESTful API endpoints that the frontend consumes. The logic is further separated into "manager" modules, which handle specific domains of responsibility.

  - **`__init__.py`**: The entry point for the Flask application. It creates the Flask app instance, loads configuration, and registers the main blueprint.

  - **`routes.py`**: This is the heart of the backend API. It defines all the URL endpoints the frontend can call:

      - `/`: Serves the main `index.html` page.
      - `/api/curriculums` & `/api/grades`: List the available data files.
      - `/api/load/curriculum` & `/api/load/grades`: Handle file loading and parsing. These endpoints store the loaded data in the user's `session`.
      - `/api/students` & `/api/semesters`: Provide lists for populating UI selectors.
      - `/api/grades/<student_name>`: Fetches enriched grade data for a specific student.
      - `/api/calculate`: The final endpoint that triggers the gradebook calculation.

  - **`managers/parsing_manager.py`**: Contains all logic related to reading and interpreting the raw CSV files. Its `analyze_and_parse_grades` function is responsible for intelligently identifying student columns, course columns, and grade columns, and then transforming the data into a clean, long format for easier processing.

  - **`managers/calculation_manager.py`**: This module contains the core business logic of the application. The `calculate_final_grades` function takes the parsed curriculum and grade data, along with user selections (student and semester), and performs the complex weighted average calculations as specified.

This modular design ensures a clean separation of concerns: `routes.py` handles web requests and responses, `parsing_manager.py` handles data ingestion, and `calculation_manager.py` handles the core computations.