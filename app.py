import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'recipes'
app.config["MONGO_URI"] = 'mongodb+srv://root:r00tUser@myfirstcluster-xc4tx.mongodb.net/recipes?retryWrites=true'

mongo = PyMongo(app)

@app.route('/')

@app.route('/recipe_index')
def recipe_index():
    return render_template("index.html", recipe=mongo.db.recipe.find())

@app.route('/get_recipe')
def get_recipe():
    return render_template("recipe.html", recipe=mongo.db.recipe.find())


@app.route('/add_recipe')
def add_recipe():
    return render_template("addrecipe.html",
    search_recipes=mongo.db.search_recipes.find())
    
@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipe = mongo.db.recipe
    recipe.insert_one(request.form.to_dict())
    return redirect(url_for('get_recipe'))


@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    the_recipe =  mongo.db.recipe.find_one({"_id": ObjectId(recipe_id)})
    all_searches =  mongo.db.search_recipes.find()
    return render_template('editrecipe.html', recipe = the_recipe,
                           search_recipes = all_searches)

@app.route('/update_recipe/<recipe_id>', methods=["POST"])
def update_recipe(recipe_id):
    recipe = mongo.db.recipe
    recipe.update( {'_id': ObjectId(recipe_id)},
    {
        'recipe_name':request.form.get('recipe_name'),
        'cuisine':request.form.get('cuisine'),
        'author': request.form.get('author'),
        'suitable_for': request.form.get('suitable_for'),
        'ingredients':request.form.get('ingredients'),
        'procedure':request.form.get('procedure'),
        'image':request.form.get('image')
    })
    return redirect(url_for('get_recipe'))


# recieves the search bar input and the filter button selection and finds the recipe
@app.route('/find_recipe', methods=['GET', 'POST'])
def find_recipe():
    searchitem = request.args.get('searchitem')
    print (searchitem)
    if request.method == 'POST':
        search_results = request.form.to_dict('searchitem')
        
    query = ( { "$text": { "$search": searchitem } } )
    search_results = mongo.db.recipe.find(query)

    return render_template('recipe.html', search_results=search_results, searchitem=searchitem)


# search bar
@app.route('/searchbar_item', methods=['GET','POST'])
def searchbar_item():

    # get search item and redirect to find_recipe route
    searchitem = request.form['search']
    return redirect(url_for('find_recipe', searchitem=searchitem))


# filter button vegetarian
@app.route('/radio_filter_veg', methods=['GET','POST'])
def radio_filter_veg():

    # get search item and redirect to find_recipe route
    searchitem = request.form['vegetarian']
    return redirect(url_for('find_recipe', searchitem=searchitem))


# filter button meateaters
@app.route('/radio_filter_meat', methods=['GET','POST'])
def radio_filter_meat():

    # get search item and redirect to find_recipe route
    searchitem = request.form['meateaters']
    return redirect(url_for('find_recipe', searchitem=searchitem))




@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipe.remove({'_id': ObjectId(recipe_id)})
    return redirect(url_for('get_recipe'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
