from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel

class Item(Resource):
    # Make sure to parse the required argument we want
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price",
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument(
        "store_id",
        type=int,
        required=True,
        help="Each item requires a store_id."
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            return item.json()
        return {"message": "Item not found."}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": "The item with name '{}' already exists.".format(name)}, 400 # Bad Request

        data = Item.parser.parse_args()

        item = ItemModel(name, data["price"], data["store_id"]) # **data

        try:
            item.save_to_db()
            return item.json(), 201
        except:
            return {"message": "An error occurred while inserting the item."}, 500

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {"message": "Item deleted"}

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if not item:
            item = ItemModel(name, data["price"], data["store_id"])
        else:
            item.price = data["price"]

        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        return {"item": [item.json() for item in ItemModel.query.all()]}
        # return {"item": list(map(lambda x: x.json(), ItemModel.query.all()))}