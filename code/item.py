import sqlite3
from flask_restful import reqparse, Resource
from flask_jwt import jwt_required

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This field cannot be empty'
                        )

    @jwt_required()
    def get(self, name):
        # for item in items:
        #     if item['name'] == name:
        #         return item
        # item = next(filter(lambda x: x['name'] == name, items), None)
        # We can return status code seprated by ,
        # return {'item': item}, 200 if item is not None else 404

        
        item = self.find_by_name(name)
        if item:
            return item
        return {'message': 'Item not foud'}, 404

        
    @classmethod
    def find_by_name(cls, name):
        # Method will return item row if exist otherwise handle it on 
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name = ?"
        result = cursor.execute(query,(name,))
        row = result.fetchone()
           
        if row:
            return {"item": {"name": row[0],"priec": row[1]}}
 

    def post(self, name):

        # if next(filter(lambda x: x['name'] == name, items), None):
        #     # 400 is for bad request
        #     return {"message": "An item with name '{}' already exist.".format(name)}, 400

        # data = Item.parser.parse_args()  # For handling json payload
        # # Prameters
        # # force = Ture then it is not neccessary to set content type in request it will automatically handle it it's not
        # # silent = True then it will not give error
        # item = {'name': name, 'price': data['price']}
        # items.append(item)
        # return item, 201  # Staus code for creation

        if self.find_by_name(name): 
            return {"message": "An item with name '{}' already exist.".format(name)}, 400
        
        data = Item.parser.parse_args()
        
        item = {"name": name, "price": data['price']};

        try:
            self.insert(item)
        except:
            return {"message": "An error occure while inserting the item."}, 500

        return item, 201

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query ="INSERT INTO items VALUES (?, ?)"
        result = cursor.execute(query,(item['name'], item['price']))
        connection.commit()
        connection.close()



    def delete(self, name):
        # Old code
        # global items
        # items = list(filter(lambda x: x['name'] != name, items))
        # return {'message': 'Item has been deleted'}
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "DELETE FROM items WHERE name = ?";
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()
        return {'message': 'Item has been deleted'}

    def put(self, name):
        # Code for reqparser some advance stuff

        data = Item.parser.parse_args()

        # Old code
        # item = next(filter(lambda x: x['name'] == name, items), None)
        # if item is None:
        #     item = {'name': name, 'price': data['price']}
        #     items.append(item)
        # else:
        #     item.update(data)
        # return item

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        # First check if item already exit if not then add and if exist then update the value

        if  self.find_by_name(name):
            query = "UPDATE items SET price = ? WHERE name = ?"
            cursor.execute(query,(data['price'], name,))
        else:
            item = {"name": name, "price": data['price']}
        
        connection.commit()
        connection.close()
        return {'item': {'name':name,'price':data['price']}}


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for item in result.fetchall():
            items.append({"name": item[0],"price": item[1]})
        connection.close()
        return {"items": items}        