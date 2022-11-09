from flask import Flask, request, Response
import os
import json

user_db = { 1 : { 'name' : 'Aleksandr', 'age' : 32},
            2 : { 'name' : 'Sergey', 'age' : 37}
}

app = Flask(__name__)

## Передача параметра в ссылке 
@app.route("/user/<int:user_id>")
def user(user_id):
    return user_db[user_id]

## Передача параметров через ?nane=&id=  и добавление POST запросом
@app.route("/user",methods=['POST', 'GET'])
def get_user():
    if request.method == 'POST' and request.is_json:
        user_db[len(user_db)+1] = request.get_json()
        return user_db
    else:
        user_id = request.args.get('id', '')
        user_name = request.args.get('name', '')
        if user_id:
            return user_db[int(user_id)]
        elif user_name:
            for key, value in user_db.items():
                if value['name'] == user_name:
                    return value
            return '<h1>Пользователь с именем '+ user_name +' не найден<h1>', 200
        else:
            return '<h1>Некорректные параметры запроса. Ожидаются name или id <h1>', 400

## API using Flask Restfull

from flask_restful import Resource, Api
api = Api(app)

class Main(Resource):
    def get(self):
        json_string = json.dumps({ u'/user_id/<id пользователя>' : u'Позволяет получить пользователя по переданному id',
                            u'/user_name/<имя пользователя>' : u'Позволяет получить пользователя по имени',
                            u'/users' : u'Позволяет получить всех пользователей'
                          }, indent =4, ensure_ascii = False )


        response = Response(json_string,content_type="application/json; charset=utf-8" )
        return response
class Users(Resource):
    def get(self,user_id = None, user_name = None):
        print(request.url_rule)

        if str(request.url_rule) == '/api/users':
            return user_db
        if str(request.url_rule) == '/api/users/id/<int:user_id>':
            return  user_db[user_id]
        if str(request.url_rule) == '/api/users/name/<user_name>':
            for key, value in user_db.items():
                if value['name'] == user_name:
                    return value

    def post(self):
        if str(request.url_rule) == '/api/users/add':
            user_db[len(user_db)+1] = request.get_json()
            return user_db

api.add_resource(Main, '/api')
api.add_resource(Users, '/api/users','/api/users/add','/api/users/id/<int:user_id>','/api/users/name/<user_name>')

if __name__=="__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)













