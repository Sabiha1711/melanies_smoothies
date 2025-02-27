#Import python packages
import streamlit as st
import requests
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

helpful_links = [
    "https://docs.streamlit.io",
    "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
    "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
    "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
]

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw::smiling_face_with_3_hearts:")

st.write("Choose the fruits you want in your smoothie!")
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

#session = get_active_session()
cnx= st.connection("snowflake")
session =cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_Name'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list =st.multiselect('Choose upto 5 ingredients:',my_dataframe,max_selections =5)
if ingredients_list:   
   ingredients_string =''    
   for fruit_chosen in ingredients_list:
       ingredients_string += fruit_chosen + ' '
       st.subheader(fruit_chosen + 'Nutrition Information')
       smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")  
       sf_df = st.dataframe(data=smoothiefroot_response.json(),use_container_width =True)
   #st.write(ingredients_string)

   my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string +"""','"""+name_on_order + """')"""
   time_to_insert =st.button("Submit Order")

   #st.write(my_insert_stmt)
   if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered, '+ name_on_order+'!', icon="✅")

























