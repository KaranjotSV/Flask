## Flask

The repository contains a Flask application, which performs **CRUD** operations in MongoDB and MySQL.

### Application Execution

  1. Open the `Terminal`.
  2. Clone the repository by entering `git clone https://github.com/KaranjotSV/Flask.git`.
  3. Ensure that `python3` and `pip` is installed on the system.
  4. Create a `virtualenv` by executing the following command: `virtualenv -p python3 env`.
  5. Activate the `env` virtual environment by executing the following command: `source env/bin/activate`.
  6. Enter the cloned repository's directory and execute `pip install -r requirements.txt`.
  7. Now, execute the following command: `python3 app.py` and it will point to the `localhost` with the port.

### Input and Request for different endpoints

  1. `/` - **GET** request, this would return all the existing documents/records in **JSON** format.
  
  2. `/create` - **POST** request with data in **JSON** format, `{"id": "2", "name": "Simranpal", "lname": "Lubana", "major": "CSE", "year": "4th"}`, the `id` has to be unique, this would create a new document in MongoDB and a new record in MySQL, with the given parameters, and would return the `id` in **JSON** format.
  
  3. `/update` - **PUT** request with data in **JSON** format, `{"id": "2", "name": "Karanjot", "lname": "Vilkhu"}`, which ever parameters to be updated are mentioned along with the `id` of the document/record, this would update an existing document in MongoDB and the same record in MySQL having the mentioned `id`.
  
  4. `/delete` - **DELETE** request with `id`, of the document/record to be deleted, in **JSON** format, `{"id": "2"}`, this would delete an existing document from MongoDB and the same record from MySQL having the mentioned `id`.
  
  5. `/detect_prime` - **POST** request with the `number`, to be detected, in **JSON** format, `{"number": "234123563"}`, this would return whether the given `number` is prime or not, in **JSON** format.
  
