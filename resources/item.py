
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    # we only want to parse the 'price' argument from payload
    # in addition, we can specify the type as well (float) in this case

    parser.add_argument('price',
    type = float,
    required = True,
    help = "This field cannot be left blank!"
    )
    
    parser.add_argument('store_id',
    type = int,
    required = True,
    help = "Every item needs a store id"
    )
    
    
    @jwt_required()
    def get(self, name):
        """
        for item in items:
            if item["name"] == name:
                return item
        """
        """
        # achieving the same using filter
        item = next(filter(lambda x: x["name"] == name, items), None)
        return {"item": item}, 200 if item is not None else 404
        """
        """
        # since now we are using a database instead of in-memory
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items where name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        """
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()       
        return {'message': 'Item not found'}, 404
        
    

    def post(self, name):       
        if ItemModel.find_by_name(name)         :
            return {"message": "An item with given name {} already exist".format(name)}, 400 
        data = Item.parser.parse_args()
        print("hello world111111111111111111")        
        
        item = ItemModel(name, data["price"], data['store_id'])
        print("hello world2222222222222")
        try:
            item.save_to_db()
            print("hello world3333333333333")
        except:
            return {"message":"An error occurred"},500
        print("hello world4444444444444444")
        print("The item is {}".format(item))
        
        #return item, 201
        return item.json(), 201

    def delete(self, name):
        item= ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message':'Item deleted'}

    def put(self, name):        
        #data = request.get_json()
        data = Item.parser.parse_args()
        #item = next(filter(lambda x: x["name"] == name, items), None)
        item = ItemModel.find_by_name(name)

                
        if item is None:
            print("Cannot find item {}".format(name))
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            print("Already exists item {}".format(name))
            item.price = data['price']
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):        
        return {"items": [Item.json() for item in ItemModel.query.all()]}
