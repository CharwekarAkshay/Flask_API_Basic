import sqlite3
from flask_restful import reqparse, Resource
from flask_jwt import jwt_required

from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This field cannot be empty'
                        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not foud'}, 404

        
    def post(self, name):
        if ItemModel.find_by_name(name): 
            return {"message": "An item with name '{}' already exist.".format(name)}, 400
        
        data = Item.parser.parse_args()
        
        item = ItemModel(name, data['price'])

        try:
            item.insert()
        except:
            return {"message": "An error occure while inserting the item."}, 500

        return item.json(), 201


    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        if ItemModel.find_by_name(name):
            query = "DELETE FROM items WHERE name = ?";
            cursor.execute(query, (name,))
            connection.commit()
            connection.close()
            return {'message': 'Item has been deleted'}
        return {'message': 'Item you want to delete doesn\'t exist'}
        

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'])

        if  ItemModel.find_by_name(name):
            # add exception handling
            item.update()    
        else:
            #Add exception handling 
            item.insert()

        return item.json()


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