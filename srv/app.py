import random

from flask          import Flask, request, jsonify
from flask_cors     import CORS


from model          import Model


# --- Flask --- #
app: Flask = Flask(__name__)
CORS(app)


# --- Model & Data --- #
MODEL = Model()
EMPLOYEE_DATA = []


@app.route('/all-employees', methods=['GET'])
def get_employees():
    return jsonify(EMPLOYEE_DATA), 200


@app.route('/employee/<string:id>', methods=['GET'])
def get_employee(id: str):
    for employee in EMPLOYEE_DATA:
        if employee['id'] == id:
            payload = employee['features']
            payload['id'] = employee['id']
            payload['Name'] = employee['name']
            return jsonify(payload), 200
    
    return jsonify({'error': 'Employee not found'}), 404


@app.route('/add', methods=['POST'])
def add_employee():
    data: dict = request.json['features']

    prediction, exp_features = MODEL.predict(data)

    if 'id' in data:
        for i, _ in enumerate(EMPLOYEE_DATA):
            if EMPLOYEE_DATA[i]['id'] == data['id']:
                EMPLOYEE_DATA[i] = {
                    'id': data.pop('id'),
                    'name': data.pop('Name'),
                    'features': data,
                    'leave_chance': prediction,
                    'exp_features': exp_features
                }
                break
    else:
        EMPLOYEE_DATA.append({
            'id': __gen_id(),
            'name': data.pop('Name'),
            'features': data,
            'leave_chance': prediction,
            'exp_features': exp_features
        })

    return jsonify({'message': 'Employee Added', 'status': 'ok'}), 200


@app.route('/delete/<string:id>', methods=['DELETE'])
def del_employee(id: str):
    for i, _ in enumerate(EMPLOYEE_DATA):
        if EMPLOYEE_DATA[i]['id'] == id:
            del EMPLOYEE_DATA[i]
            return jsonify({'message': 'Employee deleted successfully'}), 200

    return jsonify({'error': 'Employee not found'}), 404


def __gen_id() -> str:
    while True:
        id: str = f'{random.randint(0, 9999):04}'

        if id not in EMPLOYEE_DATA:
            return id


if __name__ == '__main__':
    app.run(debug=True)