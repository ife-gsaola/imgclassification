from flask import Flask, render_template,redirect, request,jsonify, url_for
from werkzeug.utils import secure_filename
from PIL import Image
import tensorflow
from io import BytesIO
import base64
import numpy as np
from base64 import b64decode
import cv2
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.utils import img_to_array
from gtts import gTTS
from IPython.display import Audio
import os


app = Flask(__name__)

class_names = ["7 DAY's CROISSANT WITH OREO CREAM FILLING", "7 DAY's CROISSANT WITH SPUMANTE FILLING", 'ADANA KEBAP', 'AERO BUBBLE PEPPERMINT CHOCOLATE', "ANTONIA'S MERMAID CAKE", 'APPETIZER CAKE', 'APPLE AND MERINGUE CAKE', 'APPLE CAKE', 'ASSORTED SALAD', 'ASSORTED SALAD WITH DILL', 'ASSORTED SALAD WITH YELLOW CHERRY TOMATOES', 'Angry', 'BACKGAMMON CAKE', 'BACLAVA', 'BAKED APPLES CAKE WITH WHIPPED CREAM AND CHOCOLATE FLAKES', 'BAKED BEANS WITH SMOKED PORK KNUCKLE', 'BAKED BISCUITS WITH SEEDS AND CHIVES', 'BAKED BROWN MUSHROOMS WITH BUTTER AND DILL', 'BAKED CARROTS WITH DILL BUTTER', 'BAKED CHICKEN DRUMSTICKS', 'BAKED CHICKEN SCHNITZEL WITH BASIL', 'BAKED OATMEAL PUDDING WITH STRAWBERRY AND RASPBERRY', 'BAKED PASTA WITH TUNA', 'BAKED POTATO', 'BAKED POTATO CHIPS WITH YOGURT & HERBS', 'BAKED POTATOES WITH BUTTER AND DILL', 'BAKED RICE PUDDING', 'BAKED RICE WITH RED ONION AND CARROTS', 'BAKED SLICED POTATOES WITH BUTTER AND DILL', 'BAKED STUFFED EGGPLANT WITH PROSCIUTTO AND MUSHROOMS', 'BAKED TORTIGLIONI WITH MUSHROOMS, PARMESAN AND BECHAMEL SAUCE', 'BAKED TROUT FISH', 'BANATEAN SALAMI', 'BARBEQUE DRUMSTICKS', 'BARBEQUE SAUCE', 'BARBEQUE WINGS', "BARBIE'S CAKE", 'BASKET PASTRY', 'BASMATI RICE', 'BASMATI RICE WITH MUSHROOMS', 'BEACH CAKE', 'BEAN SOUP WITH SMOKED PORK MEAT IN BREAD', 'BEE HONEY CAKE SHEETS', 'BEEF BURGER WITH CHEDDAR, SALAD, TOMATOES, ONION, FRIES AND BARBEQUE SAUCE', 'BEEF BURGER WITH ONION JAM', 'BEEF HAMBURGER WITH BARBEQUE SAUCE (ROMANIAN STYLE)', 'BEEF TORTELLONI WITH TOMATO SAUCE', 'BEETROOT AND APPLE SALAD', 'BIG CROISSANT WITH STRAWBERRY FILLING', 'BISCUIT CAKE WITH WHIPPED CREAM', 'BISCUITS WITH BUTTER (TEDI)', 'BISCUITS WITH HONEY', 'BLACK TIGER SHRIMPS IN BUTTER SAUCE', 'BOEUF SALAD', 'BOILED POTATO WITH PARSLEY', 'BOOK CAKE', 'BREAD PAKORA', 'BREAD ROLL WITH SESAME', 'BROWN RICE CHIPS WITH PAPRIKA', 'BUBBLE MINT GUM', 'BUTTER CREAM SANDWICH WITH PORK LOIN AND TOMATOES', 'BUTTERED SPICY MEXICAN VEGETABLES', 'Bean', 'Bitter_Gourd', 'Black', 'Blue', 'Bottle_Gourd', 'Brinjal', 'Broccoli', 'Brown', 'CABBAGE SALAD', 'CARAMEL FILLED CHURROS', 'CARP ROE SALAD', 'CARTABOS (TRADITIONAL ROMANIAN TRANSILVANIA BIG SAUSAGE)', 'CEREALS WITH SUGAR AND SOUR CHERRY', 'CHEESE', 'CHEESE BALLS', 'CHEESE CD WITH CUMIN', 'CHICKEN CUBES WITH SWEET AND SOUR SAUCE', 'CHICKEN FAJITAS', 'CHICKEN KEBAP', 'CHICKEN SHAORMA', 'CHICKEN STEW', 'CHICKEN STEW WITH POTATOES', 'CHICKEN STEW WITH TOMATO SAUCE', 'CHILI POTATO CHIPS', 'CHILLI SAUCE', 'CHINESE NOODLES AND DRIED CHINESE MUSHROOMS', 'CHINESE NOODLES WITH VEGETABLES AND DRIED CHINESE MUSHROOMS', 'CHIPICAO CROISSANT WITH COCOA FILLING', 'CHOCO BALLS CEREALS', 'CHOCOLATE CAKE WITH COCONUT CREAM', 'CHOCOLATE CAKE WITH COCONUT FLAKES', 'CHOCOLATE CAKE WITH WALNUTS', 'CHOCOLATE CANDY  FILLED WITH CHERRY CREAM', 'CHOCOLATE CANDY FILLED WEITH LEMON CREAM', 'CHOCOLATE CANDY FILLED WITH COCONUT CREAM', 'CHOCOLATE CANDY FILLED WITH HAZELNUT CREAM', 'CHOCOLATE CANDY FILLED WITH TURKISH DELIGHT CREAM', 'CHOCOLATE CANDY NUT FILLED WITH SOFT CARAMEL AND PEANUTS', 'CHOCOLATE ECLAIR', 'CHOCOLATE FILLED CHURROS', 'CHOPPED PORK MEAT FUSILLI', 'CHRISTMAS CAKE', 'CHRUP PAKI WITH BACON', 'CHRUP PAKI WITH CHEESE', 'CHRUP PAKI WITH SALT', 'CLASSIC TOAST', 'CLOUD EGG', 'COCOA BISCUITS WITH RUM CREAM (ROMANIAN BISCUITS)', 'COCOA DOUBLE BISCUITS', 'COCOA MILK BURGER', 'COCOA WAFERS CUBES', 'COCONUT CAKE WITH STRAWBERRY WHIPPED CREAM', 'COCONUT CAKE WITH WHIPPED CREAM', 'COOKED CABBAGE WITH PORK RIBS', 'COOKED COUSCOUS WITH DILL', 'COOKIES WITH RASPBERRY JAM (BUSEURI)', 'COQUELETTE CHICKEN WITH MUSHROOM SAUCE AND MASHED POTATOES', 'CORDON BLEU', 'CORN ON THE COBB', 'CORNETTE CARAMEL ICE CREAM', 'CORNETTI RIGATTI WITH SOURCREAM , TENDERLOIN, CORN AND CUCUMBER', 'COVERED PUFFS WITH CHOCOLATE', 'CRANBERRY COOKIES WITH WHITE CHOCOLATE', 'CREAM CHEESE WITH HERBS (CREFEE)', 'CREAMY RANCH CHICKEN PASTA', 'CREMES', 'CREPES WITH JAM', 'CREPES WITH SWEET URDA', 'CRISPY CHICKEN', 'CRISPY CHICKEN WITH SESAME', 'CRISPY PEANUTS COATED WITH PAPRIKA', 'CRUNCHY CHICKEN BREAST', 'CRUNCHY TACO', 'CURRY RICE WITH YOGHURT', 'Cabbage', 'Capsicum', 'Carrot', 'Cauliflower', 'Cucumber', "DANA'S MERMAID CAKE", 'DANISH COOKIES', 'DANISH COOKIES WITH SUGAR', 'DARK CHOCOLATE WITH BRANDY  AND ORANGES CREAM', "DENTIST'S CAKE", 'DIPLOMAT CAKE', 'DOGS CAKE', 'DONALD DUCK CAKE', 'DONUTS WITH VANILLA SUGAR POWDER', 'DOSA WITH CURRY MASHED POTATOES', 'DUCHESSE POTATOES', 'DUCK STEW', 'DUMPLINGS PASTRY', 'DUO CHOCOLAT', 'Didgeridoo', 'Didgeridoo (1)', 'EASTER CAKE', 'EGGBPLANTS SALAD', 'EMMENTAL CHEESE IN SLICES', "ENGINEER'S CAKE", 'EUGENIA FOX BISCUITS WITH COCOA CREAM', 'EUKALIPTUS MENTHOL BONBONS', 'EXPANDED CHIPS WITH SOUR CREAM AND DILL', 'EXTRUDED MAIZE GRITS FLIPS IN TUBE SHAPE WITH CHEESE FLAVOUR', 'FAGARAS CHOCOLATE BAR', 'FARFALLE WITH BECHAMEL SAUCE AND MUSHROOMS', 'FARFALLE WITH SALAMI CARBONARA', 'FERRERO-YOGURETTE CHOCOLATE BAR  FILLED WITH STRAWBERRY YOGURT', 'FILLED PASTRY WITH APPLE JAM', 'FILLED PASTRY WITH STRAWBERRY JAM', 'FISH FINGERS', 'FISH ROE SALAD', "FISHERMAN'S CAKE", 'FLIPS PUFFS WITH ROASTED & SALTED PEANUTS', 'FLOWER LOG PASTRY', 'FLOWER PIE WITH CHEESE', 'FOREST FRUIT CHEESECAKE', 'FRENCH FRIES', 'FRENCH FRIES WITH DRIED VEGETABLE POWDER', 'FRESH GARDEN SALAD', 'FRESH SALMON', 'FRIED BEATEN EGG WHITE', 'FRIED BLACK SEA MUSSELS', 'FRIED BREAD SLICE COATED IN EGG', 'FRIED CASHEW NUTS WITH SALT', 'FRIED CHICKEN DRUMSTICK', 'FRIED CHICKEN SCHNITZEL', 'FRIED EGG', 'FRIED EGG WITH CUMIN SEEDS AND PAPRIKA', 'FRIED EGG WITH VEGETABLE POWDER', 'FRIED PEANUT WITH PAPRIKA', 'FRIED POTATO WEDGES', 'FRIED POTATOES WITH GARLIC', 'FRIED RIBBONS (CHIROANE FRIPTE, MOLDAVIAN DISH)', 'GAME MEAT GOULASH', 'GARLIC SAUCE', 'GERARD COCOA BISCUITS WITH FLAVOURED CREAM', 'GNOCCHI WITH CHEESE AND MUSHROOMS', 'GOGOSI (ROMANIAN DONUTS)', 'GOMBOTI (HUNGARIAN TRADITIONAL DESERT)', 'GOUDA CHEESE IN SLICES', "GRANDMA'S CAKE", 'GREEN LENTILS WITH SMOKED PORK MEAT', 'GREEN LENTILS WITH SMOKED PORK SAUSAGES', 'GREEN SALAD', 'GRILLED CHICKEN', 'GRILLED CHICKEN BREAST', 'GRILLED CHICKEN WINGS', 'GRILLED HOT DOG', 'GRILLED MARINATED PORK MEAT', 'GRILLED PORK', 'GRILLED PORK CHOP', 'GRILLED PORK MEAT', 'GRILLED PORK MEAT BURGER WITH TOMATOES AND MAYONNAISE', 'GRILLED SPICE WINGS', 'GRILLED THURINGER SAUSAGE', 'GRILLED TURKEY BREAST WITH PEACH SAUCE', 'GRILLED TURKEY WITH GRAPE SAUCE', 'Green', 'G├╢ZLEME (TURKISH LAYERED PIE)', 'HASSELBACK CHICKEN WITH BACON AND CHEESE', 'HEART CAKE WITH YOGHURT AND FOREST FRUITS', 'HELLO KITTY CAKE', 'HERBS CRUSTED PORK MOSS WITH MASHED POTATO AND WINE SAUCE', 'HOMEMADE CHILI JAM', 'HOMEMADE CHOCOLATE WITH RUM AND COCONUT BALLS', 'HOMEMADE COCONUT WHITE CHOCOLATE', 'HOMEMADE CRACKERS WITH SALTED CHEESE AND CUMIN SEEDS', 'HOMEMADE CRISPY CHICKEN', 'HOMEMADE GOMBOTI', 'HOMEMADE PRESSED CHEESE', 'HOMEMADE RED GRAPES SAUCE', 'HONEY MILK BURGER', 'HONEY MUESLI BAR WITH SWEET AND SOUR CHERRY', 'HONEY ROASTED PEANUTS', 'HOT SALAMI SANDWICH WITH KETCHUP AND GARLIC SAUCES', "HUNTSMAN'S CAKE", 'Happy', 'INDIAN CURRY', 'JOE COCOA MILK CHOCOLATE WAFER', 'KFC CHICKEN DRUMSTICKS', 'KFC CHILLI CHEESE NUGGETS', 'KFC CRISPY', 'KFC CRISPY HOT DOG', 'KFC DIPPING FRIES', 'KFC HOLIDAY BURGER', 'KFC REAL BURGER', 'KFC VEGAN BURGER', 'KFC WINGS', 'KINDER ICE CREAM SANDWICH', 'KITKAT CHOCOLATE', 'LAMAITA CAKE', 'LAMB STEW WITH BEANS', 'LASAGNA (WITH  BEEF MEAT)', 'LAYERED SLICES OF HAM AND CHEESE', 'LEBER PASTE', 'LEGO CAKE', 'LETTUCE SOUP', 'LINGUINI WITH MUSHROOM AND TOMATOE SAUCE AND SALAMI', 'LOLLIPOPS', 'LONG CHIPS PAPRIKA', 'LONG CHIPS SOUR CREAM & ONION POTATO SNACK', 'LONG THIN PUFF PASTRY WITH SESAME', 'MACARONI PUDDING', 'MAGURA MINI CAKE WITH MILK', 'MAGURA MINI-ROULADE FILLED WITH BERRIES AND CHEESECAKE', 'MARS ICE CREAM', 'MARSHMALLOW BISCUITS WITH COCONUT GLAZE', 'MASALA DOSA', 'MASALA RAGU SAUCE', 'MASHED POTATO WITH PAPRIKA POWDER, ONION AND PARSLEY', 'MASHED POTATOES', 'MASHED POTATOES WITH SPRINKLED PARSLEY', 'MENTOS MINT', 'MEXICAN THIN PITA BREAD', 'MEXICAN VEGETABLES WITH BUTTER', 'MEXICAN WHITE RICE WITH VEGETABLES', 'MICI (BEEF & PORK MEAT)', 'MICKY MOUSE CAKE', 'MILK CHOCOLATE CARAMEL WAFER BISCUIT', 'MILK FILLED CANDIES', 'MILKA ALPIN MILK CHOCOLATE BAR', 'MILKA BUBBLY WHITE AERATED CHOCOLATE BAR', 'MILKSHAKE DESERT', 'MINI BAGUETTE', 'MINI SAUSAGE WRAPPED IN PASTRY', 'MINT AND MANGO-PINEAPPLE CHOCOLATE FLAVOUR', 'MIXED FRUITS BUBBLE GUM', 'MOLDAVIAN PIE WITH CHEESE', 'MORTADELLA BOLOGNA IGP WITH PISTACHIOS', 'MUESLI BAR WITH APPLES AND APRICOTS', 'MUTTON GOULASH', 'MUTTON SKEWERS', 'NACHO FRIES', 'NAKED CHICKEN TACO', "NEWBORN BABY'S CAKE", 'NUSSSCHNECKEN', 'OMELETTE WITH SALAMI AND CHEESE', 'ORANGE HELLO KITTY CAKE', 'OREO BISCUITS COVERED WITH WHITE CHOCOLATE', 'OREO ICE CREAM CONE', 'OREO ICE CREAM SANDWICH', 'ORIENTAL SALAD (ROMANIAN VERSION)', 'OVEN BAKED CHIPS WITH VEGGIE BARBEQUE FLAVOUR', 'PAKORA', 'PASTRY BAR WITH CHIA SEEDS', 'PASTRY BAR WITH MOZZARELLA', 'PASTRY POUCHES', 'PASTRY TWIST', 'PENNE RAGU', 'PENNE WITH MASALA RAGU', 'PICNIC BASKET PASTRY', 'PISTACHIO CRUSTED PORK MOSS WITH MASHED POTATOES AND RED GRAPES SAUCE', 'PITA BREAD', 'PIZZA DIAVOLA', 'PIZZA PROSCIUTTO E FUNGHI', 'PIZZA PUFF PASTRY WITH SALAMI, TOMATOES, GOUDA CHEESE AND BASIL', 'PIZZA SLICE WITH TOMATO SAUCE, HAM, MOZZARELLA AND OREGANO', 'PIZZA SLICE WITH TOMATO SAUCE, SALAMI, MOZZARELLA AND OREGANO', 'PLANE CAKE', 'PLUM CAKE', 'PLUM PIE', 'POLAR VANILLA ICE CREAM SANDWICH', 'POLENTA (MAMALIGA)', 'POM-BAR WITH CHEESE', 'POMANA PORCULUI (ROMANIAN FRIED PORK MEAT AND POLENTA WITH CHEESE)', 'POPCORN WITH CARAMEL', 'PORK CHOP FILLED WITH BACON AND PLEUROTUS WITH CHIMCHURI SALSA AND BAKED POTATOES', 'PORK LOIN STEW WITH GARLIC AND TOMATO SAUCE', 'PORK MEAT PATE', 'PORK MEAT TORTOISE WITH CHEESE AND RICE', 'PORK MEATBALLS', 'PORK SAUSAGES', 'POTATO CHIPS WITH CHEESE AND JALAPENO CHILLI FLAVOUR', 'POTATO CHIPS WITH SOURCREAM AND ONIONS', 'POTATO STEW WITH SAUSAGE SLICES', 'POTATO STEW WITH SMOKED PORK', 'PRAJITURA DESTEAPTA WITH VANILLA', 'PRETZEL WITH SALT', 'PURPLE SWEET POTATO ICECREAM', 'Papaya', 'QUINCE JAM WITH CINNAMON', 'QUOTE CAKE', 'RADAUTEANA SOUP', 'RAFFAELLO BALLS', 'RAHAT LOKUM (TURKISH DELIGHT)', 'RASPBERRY AND CHOCOLATE ICE CREAM DESSERT', 'RASPBERRY EYE PASTRY', 'RASPBERRY ICE CREAM DESSERT', 'RASPBERRY JAFFA CAKE', 'RASPBERRY LOG PASTRY', 'RECTANGULAR PASTRY', 'RED BEEF BURGER', 'RED CAR CAKE', 'RED PORK BURGER', 'RIDGED POTATO CHIPS WITH CHILLI', 'RIDGED POTATO CHIPS WITH SOURCREAM AND PAPRIKA', 'RIFFLED POTATO CHIPS WITH CHEESE', 'RIFFLED POTATO CHIPS WITH SEA SALT', 'RIFFLED POTATO CHIPS WITH SOURCREAM & ONION', 'RISOTTO WITH CHICKEN GIZZARDS AND HEARTHS', 'ROAST CHICKEN WITH BUTTER AND BASIL', 'ROASTED AND SALTED CORN', 'ROASTED COCONUT COVERED CARAMEL WAFER BISCUIT', 'ROASTED PIG', 'ROLO CHOCOLATE CANDY FILLED WITH CARAMEL CREAM', 'ROSES CAKE', 'SALTED CHEESE', 'SALTED CHEESE WITH HERBS', 'SAMOSA WITH VEGETABLES', 'SANDWICH WHOLEGRAIN BAGUETTE WITH FLAX SEEDS, KAIZER AND BUTTER', 'SARMALE (PORK MEAT)', 'SCRAMBLED EGG WITH CROUTONS', 'SCRAMBLED EGG WITH FRIED PROSCIUTTO', 'SCRAMBLED EGGS', 'SCRAMBLED EGGS WITH SALAMI', 'SEASONED GRILLED PORK', 'SEMOLINA PUDDING WITH RASPBERRY', 'SIMPLE COOKED COUSCOUS', 'SIMPLE CROUTONS', 'SIMPLE CUPCAKES WITH SUGAR', 'SIMPLE DONUTS', 'SKEWER', 'SMOKED LARD', 'SMOKED PORK LOIN FILLET', 'SNICKERS ICE CREAM', 'SOFT CAKE', 'SOFT CAKE WITH MERINGUE ON TOP', 'SOUR CHERRY JAM', 'SPANISH MADELEINE', 'SPICY BAKED HAKE', 'SPICY PINEAPPLE SAUCE', 'SPINACH', 'SPINACH AND RICOTTA TORTELLONI IN TOMATO SAUCE', 'SPINACH AND RICOTTA TORTELLONI IN TOMATO SAUCE SPRINKLED WITH  CHEESE', 'STEAM MUSSELS IN WHITE WINE BROTH', 'STEAMED FISH (PASTRAV)', "STEAUA'S CAKE", 'STRAWBERRY CHEESECAKE', 'STRAWBERRY MOUSSE CAKE', 'STROOPWAFELS', 'STRUDEL WITH APPLE JAM', 'STRUDEL WITH SALTED CHEESE AND DILL', 'STUFFED PEPPERS AND SMOKED PORK MEAT SOUP', 'SUBEREK (TURKISH PIE)', 'SUGUS MILK TOFFEE', 'SUV', 'SWEEET CORN PUFFS WITH MILK POWDER', 'Sad', 'TAGLIATELLE ALLA CARBONARA', 'THOUSAND ISLANDS SAUCE', 'TIC-TAC WITH STRAWBERRY AND MINT', 'TIRAMISU', 'TOFFEE AND CRISPED CEREAL CHOCOLATE BAR', 'TOMATO KETCHUP', 'TOMATOES AND ONION LEAVES SALAD', 'TORTELLINI WITH MUSHROOM AND TOMATO SAUCE', 'TRIANGLE PASTRY', 'TURKEY AND CHICKEN LIVER PATE', 'TURKEY BREAST WITH PEACH SAUCE', 'TURKEY HAM', 'TURKEY LIVER MEATLOAF', 'TURKISH GUMMY BALLS', 'TWIX ICE CREAM', 'Tambourine', 'Tambourine (1)', 'VEAL GOULASH', 'VEGETABLE CURRY', 'VEGETABLE CURRY AND BASMATI RICE', 'VEGETABLE SAUTE', 'VERDENS BESTE', 'VERDENS BESTE CAKE', 'Violet', 'WHIPPED CREAM ICE CREAM', 'WHISKEY CAKE', 'WHITE BREAD SLICE WITH VEGETABLE PASTE WITH MUSHROOMS', 'WHOLE WHEAT OAT MUFFINS', 'WHOLE WHEAT OATMEAL CHOCOLATE CHIP MUFFINS', 'WHOLEGRAIN BAGUETTE WITH FLAX SEEDS', 'WUDY WURSTEL AL FORMAGGIO', 'White', 'Xylophone', 'Xylophone (1)', 'YELLOW MUSTARD', 'YOGURT SAUCE (MOUSTARD, GARLIC, GINGER POWDER, FRESH DILL)', 'YORKIE CHUNKY MILK CHOCOLATE', 'ZACUSCA WITH EGGPLANT', 'ZEBRA CAKE', 'ZUCCHINI BOATS STUFFED WITH PORK', 'ZUCCHINI SOUP', 'acordian', 'acordian (1)', 'alphorn', 'alphorn (1)', 'apple_6', 'apple_braeburn_1', 'apple_crimson_snow_1', 'apple_golden_1', 'apple_golden_2', 'apple_golden_3', 'apple_granny_smith_1', 'apple_hit_1', 'apple_pink_lady_1', 'apple_red_1', 'apple_red_2', 'apple_red_3', 'apple_red_delicios_1', 'apple_red_yellow_1', 'bagpipes', 'bagpipes (1)', 'banjo', 'banjo (1)', 'bed', 'bed (1)', 'bongo drum', 'bongo drum (1)', 'bus', 'butterflies', 'casaba', 'casaba (1)', 'castanets', 'castanets (1)', 'chair', 'circle', 'clarinet', 'clarinet (1)', 'clavichord', 'clavichord (1)', 'clothing', 'concertina', 'concertina (1)', 'daisy', 'dandelion', 'dew', 'dog', 'drums', 'drums (1)', 'dulcimer', 'dulcimer (1)', 'elephant', 'family sedan', 'fire engine', 'flute', 'flute (1)', 'fogsmog', 'guiro', 'guiro (1)', 'guitar', 'guitar (1)', 'harmonica', 'harmonica (1)', 'harp', 'harp (1)', 'heavy truck', 'horses', 'images', 'jeep', 'kite', 'marakas', 'minibus', 'ocarina', 'orange', 'parallelogram', 'piano', 'racing car', 'rectangle', 'red', 'rhombus', 'roses', 'saxaphone', 'sitar', 'sofa', 'square', 'steel drum', 'swivelchair', 'table', 'taxi', 'trapezoid', 'triangle', 'trombone', 'trumpet', 'tuba', 'tulips', 'violin', 'yellow']


UPLOAD_FOLDER = "https://raw.githubusercontent.com/ife-gsaola/imgclassification/main/"

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load trained model
MODEL_PATH = "PROJECT4.h5"
model = load_model(MODEL_PATH, compile=False)

@app.route('/')
def index():
    return render_template("indexx.html", data="hey")


@app.route("/predict", methods=["POST"])
def predict():

    image_data = request.json.get('image_data')
    image = Image.open(BytesIO(base64.b64decode(image_data)))

    # Preprocess the image
    image = image.resize((64, 64))  # Resize image to match model input shape
    image_array = img_to_array(image)
    image_array = preprocess_input(image_array)
    image_array = np.expand_dims(image_array, axis=0)

    # Make prediction
    predictions = model.predict(image_array)
    predicted_class_index = np.argmax(predictions)
    predicted_class = class_names[predicted_class_index]
    confidence = float(predictions[0][predicted_class_index])  # Convert to float

    return jsonify({"prediction": predicted_class, "confidence": confidence})


@app.route("/prediction", methods=["POST"])
def prediction():
    im_path = os.path.join(app.config['UPLOAD_FOLDER'], "img.jpg")  # Path to save uploaded image

    img = request.files['img']
    img.save(im_path)

    img = image.load_img(im_path, target_size=(64, 64))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    # Predict the class probabilities
    predictions = model.predict(img_array)

    confidence_threshold = 0.6
    predicted_class_index = np.argmax(predictions)
    predicted_class = class_names[predicted_class_index]
    confidence = np.max(predictions)

    if confidence < confidence_threshold:
        return render_template("production.html", data=f"Out of scope {confidence}")
    else:
        return render_template("production.html", data=f"{predicted_class}", data1=f"{confidence}")


if __name__ == "__main__":
    app.run(debug=True)
