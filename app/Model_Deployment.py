# import streamlit as st
# from PIL import Image
# from keras.preprocessing.image import load_img, img_to_array # type: ignore
# import numpy as np
# from keras.models import load_model # type: ignore
# import requests
# from bs4 import BeautifulSoup
# import webbrowser
# import base64
# import os

# # Load the model
# model = load_model('FV.h5')

# # Mapping of class indices to labels
# labels = {
#     0: 'apple', 1: 'banana', 2: 'beetroot', 3: 'capsicum', 4: 'cabbage',
#     5: 'capsicum', 6: 'carrot', 7: 'cauliflower', 8: 'chilli pepper', 9: 'corn',
#     10: 'cucumber', 11: 'eggplant', 12: 'garlic', 13: 'ginger', 14: 'grapes',
#     15: 'jalapeno', 16: 'kiwi', 17: 'lemon', 18: 'lettuce', 19: 'mango',
#     20: 'onion', 21: 'orange', 22: 'paprika', 23: 'pear', 24: 'peas',
#     25: 'pineapple', 26: 'pomegranate', 27: 'potato', 28: 'raddish',
#     29: 'soy beans', 30: 'spinach', 31: 'sweetcorn', 32: 'sweetpotato',
#     33: 'tomato', 34: 'turnip', 35: 'watermelon'
# }

# # Categories
# fruits = ['Apple', 'Banana', 'Chilli Pepper', 'Grapes', 'Jalapeno', 'Kiwi', 'Lemon', 'Mango', 'Orange', 'Paprika', 'Pear', 'Pineapple', 'Pomegranate', 'Watermelon']
# vegetables = ['Beetroot', 'Cabbage', 'Capsicum', 'Carrot', 'Cauliflower', 'Corn', 'Cucumber', 'Eggplant', 'Ginger', 'Lettuce', 'Onion', 'Peas', 'Potato', 'Raddish', 'Soy Beans', 'Spinach', 'Sweetcorn', 'Sweetpotato', 'Tomato', 'Turnip']

# def fetch_calories(prediction):
#     try:
#         url = 'https://www.google.com/search?&q=calories in ' + prediction + ' 100g'
#         headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
#         req = requests.get(url, headers=headers)

#         if req.status_code != 200:
#             print("Error: Unable to fetch data from Google.")
#             return None
        
#         soup = BeautifulSoup(req.text, 'html.parser')
#         calories_info = soup.find_all("div", class_="BNeawe iBp4i AP7Wnd")

#         if calories_info:
#             for info in calories_info:
#                 text = info.get_text()
#                 if "calories" in text.lower():
#                     return text
#             print("Calories not found in the response.")
#             return None
#         else:
#             print("No relevant data found.")
#             return None
        
#     except Exception as e:
#         print("Error fetching calories:", e)
#         return None

# def fetch_fat(prediction):
#     try:
#         url = 'https://www.google.com/search?&q=fat in ' + prediction
#         headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
#         req = requests.get(url, headers=headers).text
#         scrap = BeautifulSoup(req, 'html.parser')
#         fat_info = scrap.find("div", class_="BNeawe iBp4i AP7Wnd")

#         if fat_info:
#             return fat_info.text
#         else:
#             print("Fat information not found.")
#             return None
#     except Exception as e:
#         print("Error fetching fat information:", e)
#         return None

# def get_base64_of_bin_file(bin_file):
#     with open(bin_file, 'rb') as f:
#         data = f.read()
#     return base64.b64encode(data).decode()

# def set_bg_hack(main_bg):
#     main_bg_ext = "png"
#     st.markdown(
#         f"""
#         <style>
#         .stApp {{
#             background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
#             background-size: cover
#         }}
#         </style>
#         """,
#         unsafe_allow_html=True
#     )

# def processed_img(img_path):
#     img = load_img(img_path, target_size=(224, 224))
#     img = img_to_array(img)
#     img = img / 255
#     img = np.expand_dims(img, [0])
#     answer = model.predict(img)
#     y_class = answer.argmax(axis=-1)
#     y = int(y_class[0])
#     res = labels[y]
#     return res.capitalize()

# def run():
#     upload_dir = './upload_images'
#     if not os.path.exists(upload_dir):
#         os.makedirs(upload_dir)

#     bg_image_path = r"C:\\Users\\mas_r\\OneDrive\\Desktop\\Major project\\Images\\bg_image.jpg"
#     if os.path.exists(bg_image_path):
#         set_bg_hack(bg_image_path)

#     st.title("Calorie Predictor & Diet Plan Recommender")
    
#     if st.button('Go to diet plans'):
#         webbrowser.open_new_tab(r"C:\\Users\\mas_r\\OneDrive\\Desktop\\Major project\\index1.html")

#     img_file = st.file_uploader("Choose an Image", type=["jpg", "png"])
    
#     if img_file is not None:
#         img = Image.open(img_file).resize((250, 250))
#         st.image(img, use_column_width=False)
        
#         save_image_path = os.path.join(upload_dir, img_file.name)
#         with open(save_image_path, "wb") as f:
#             f.write(img_file.getbuffer())

#         try:
#             result = processed_img(save_image_path)
#             st.write("Predicted Result:", result)

#             if result in vegetables:
#                 st.info('**Category: Vegetables**')
#             else:
#                 st.info('**Category: Fruits**')

#             st.success("**Predicted: " + result + '**')

#             cal = fetch_calories(result)
#             fat = fetch_fat(result)

#             if cal:
#                 st.warning('**' + cal + ' (100 grams)**')
#             if fat:
#                 st.warning('**Total fat: ' + fat + '**')

#         except Exception as e:
#             st.error(f"Error during image processing: {e}")

# if __name__ == "__main__":
#     run()

import streamlit as st
from PIL import Image
from keras.preprocessing.image import load_img, img_to_array
import numpy as np
from keras.models import load_model
import requests
from bs4 import BeautifulSoup
import webbrowser
import os
import base64

# Load the model
model = load_model('FV.h5')

# Mapping of class indices to labels
labels = {
    0: 'apple', 1: 'banana', 2: 'beetroot', 3: 'capsicum', 4: 'cabbage', 5: 'capsicum', 6: 'carrot', 7: 'cauliflower',
    8: 'chilli pepper', 9: 'corn', 10: 'cucumber', 11: 'eggplant', 12: 'garlic', 13: 'ginger', 14: 'grapes',
    15: 'jalapeno', 16: 'kiwi', 17: 'lemon', 18: 'lettuce', 19: 'mango', 20: 'onion', 21: 'orange', 22: 'paprika',
    23: 'pear', 24: 'peas', 25: 'pineapple', 26: 'pomegranate', 27: 'potato', 28: 'raddish', 29: 'soy beans',
    30: 'spinach', 31: 'sweetcorn', 32: 'sweetpotato', 33: 'tomato', 34: 'turnip', 35: 'watermelon'
}

fruits = ['Apple', 'Banana', 'Chilli Pepper', 'Grapes', 'Jalapeno', 'Kiwi', 'Lemon', 'Mango', 'Orange', 'Paprika', 'Pear', 'Pineapple', 'Pomegranate', 'Watermelon']
vegetables = ['Beetroot', 'Cabbage', 'Capsicum', 'Carrot', 'Cauliflower', 'Corn', 'Cucumber', 'Eggplant', 'Ginger', 'Lettuce', 'Onion', 'Peas', 'Potato', 'Raddish', 'Soy Beans', 'Spinach', 'Sweetcorn', 'Sweetpotato', 'Tomato', 'Turnip']

def fetch_calories(prediction):
    try:
        url = 'https://www.google.com/search?&q=calories in ' + prediction + ' 100g'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        req = requests.get(url, headers=headers)
        if req.status_code != 200:
            return None

        soup = BeautifulSoup(req.text, 'html.parser')
        calories_info = soup.find_all("div", class_="BNeawe iBp4i AP7Wnd")
        if calories_info:
            for info in calories_info:
                text = info.get_text()
                if "calories" in text.lower():
                    return text
        return None
    except Exception as e:
        return None

def fetch_fat(prediction):
    try:
        url = 'https://www.google.com/search?&q=fat in ' + prediction
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        req = requests.get(url, headers=headers).text
        scrap = BeautifulSoup(req, 'html.parser')
        fat_info = scrap.find("div", class_="BNeawe iBp4i AP7Wnd")
        if fat_info:
            return fat_info.text
        else:
            return None
    except Exception as e:
        return None

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_bg_hack(main_bg):
    main_bg_ext = "png"
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def processed_img(img_path):
    img = load_img(img_path, target_size=(224, 224))
    img = img_to_array(img)
    img = img / 255
    img = np.expand_dims(img, [0])
    answer = model.predict(img)
    y_class = answer.argmax(axis=-1)
    y = int(y_class[0])
    res = labels[y]
    return res.capitalize()

def run():
    # Set the background image (replace with your own image path)
    bg_image_path = r"C:\\Users\\mas_r\\OneDrive\\Desktop\\Major project\\Images\\bg1.jpg"
    if os.path.exists(bg_image_path):
        set_bg_hack(bg_image_path)

    st.markdown("<h1 style='text-align: center; color: #31c05c;'>Calorie Predictor & Diet Plan Recommender</h1>", unsafe_allow_html=True)
    st.write("### Upload an image to estimate calories and get a diet recommendation!")

    # Image upload
    img_file = st.file_uploader("Choose an Image", type=["jpg", "png"])

    if img_file is not None:
        img = Image.open(img_file).resize((250, 250))
        st.image(img, caption="Uploaded Image", use_column_width=False, width=300)

        # Save uploaded image
        upload_dir = './upload_images'
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        save_image_path = os.path.join(upload_dir, img_file.name)
        with open(save_image_path, "wb") as f:
            f.write(img_file.getbuffer())

        # Predict the category (fruit or vegetable) and fetch related information
        try:
            result = processed_img(save_image_path)
            st.write(f"**Predicted Result:** {result}")

            if result in vegetables:
                st.info(f'**Category:** Vegetables')
            else:
                st.info(f'**Category:** Fruits')

            st.success(f"**Predicted: {result}**")

            cal = fetch_calories(result)
            fat = fetch_fat(result)

            if cal:
                st.warning(f'**{cal} (100 grams)**')
            if fat:
                st.warning(f'**Total fat: {fat}**')

        except Exception as e:
            st.error(f"Error during image processing: {e}")

    # Button to navigate to diet plans
    if st.button('Explore Diet Plans', help="Get personalized diet plans"):
        webbrowser.open_new_tab(r"C:\\Users\\mas_r\\OneDrive\\Desktop\\Major project\\index1.html")

if __name__ == "__main__":
    run()
