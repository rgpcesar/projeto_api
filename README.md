# REST API Test Automation Mini-Course

This repository contains the material for a 4-lesson mini-course on REST API test automation using Python.

## Repository Structure

*   **/api-exemplo**: A sample Flask-based REST API used for the testing exercises throughout the course. It includes models for users and posts, and the corresponding API routes.
*   **/aula1**: **Lesson 1: Introduction to API Testing.** This lesson covers the basics of REST APIs and how to make requests using the `requests` library in Python. The `solucao.py` file contains the solution for this lesson's exercises.
*   **/aula2**: **Lesson 2: Introduction to Pytest.** This lesson introduces the Pytest framework for structuring tests and making assertions. The `solucao.py` file demonstrates how to refactor the code from Lesson 1 into Pytest tests.
*   **/aula3**: **Lesson 3: Data-Driven Testing.** This lesson covers how to read test data from external files (like CSV) to run the same test with multiple data inputs. The `solucao.py` and `casos_de_teste.csv` files contain the solution and test data for this lesson.
*   **/aula4**: **Lesson 4: Reporting and Allure Framework.** This lesson shows how to generate rich test reports using the Allure framework. The `solucao/` directory contains a complete example with tests and the generated Allure report.
*   **/exemplo**: Contains a simple Python script `exemplo.py`.

## How to Use

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/projeto_api.git
    cd projeto_api
    ```
2.  **Set up the sample API:**
    ```bash
    cd api-exemplo
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    flask run
    ```
3.  **Follow the lessons:** Each `aula` folder is self-contained and corresponds to a lesson in the mini-course. You can follow the presentations (`.html` files) and see the solutions in the `solucao.py` or `solucao/` directories.
