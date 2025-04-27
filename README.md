# 🏥 Health Information System

This project is a **basic Health Information System** built using **Flask**, **SQLite**, and **HTML/CSS**.  
It allows a doctor (user) to manage clients and health programs easily through a web interface.

## ✨ Features
- Create new health **programs** (e.g., TB, Malaria, HIV, etc.)
- **Register** new clients with name, age, and gender
- **Enroll** clients into multiple health programs
- **Search** for clients and view a full list
- **View** a client’s detailed profile and enrolled programs
- **Expose** client profiles via a **RESTful API** for external systems

## 📷 Screenshots

### Home Page
![Home Page](images/homepage.png)

### Create Program
![Create Program](images/create_program.png)

### Register Client Page
![Register Client](images/register_client.png)

### Enroll Client Page
![Enroll Client](images/enroll_client.png)

### Client Profile Page
![Client Profile](images/profile.png)

### Search Clients Page
![Search Clients](images/search.png)


## 🚀 Technologies Used
- **Python 3**
- **Flask**
- **SQLite3** (Database)
- **HTML5**, **CSS3** (Frontend)
- **Flask-WTF** (for future form handling)

## 🛠️ Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/GraceMuli/HealthInformationSystem.git
   cd HealthInformationSystem
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate    # On Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python run.py
   or
   flask run
   ```

## 📑 API Endpoints

- **Get a client's profile** (JSON):
  ```
  GET /api/client/<client_id>
  ```

  **Example Response**:
  ```json
  {
    "id": 1,
    "name": "Grace",
    "age": 18,
    "gender": "Female",
    "programs": ["Malaria"]
  }
  ```

## 👩‍💻 Author
- Grace Muli

## 📜 License
This project is licensed under the [MIT License](LICENSE).
