import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Menu')

streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free Range Egg')
streamlit.text('🥑🍞 Avacado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

#make it so that fruit names appear rather than numbers
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

#New section to display fruitvice API response
streamlit.header('Fruityvice Fruit Advice!')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
      streamlit.error("Please select a fruit to get information.")
  else:
      fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
      # take json version of the response and normalize it
      fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
      # output to screen as a table
      streamlit.dataframe(fruityvice_normalized)

except URLError as e:
  streamlit.error()
  
#streamlit.text(fruityvice_response.json()) #just writes data to screen
# take json version of the response and normalize it
#fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())


#DON'T RUN ANYTHING PAST HERE WHILE WE TROUBLESHOOT
streamlit.stop()
#query trial account metadata
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

#What fruit would you like to add? allow end user to add a fruit to the list
add_my_fruit = streamlit.text_input('What fruit would you like to add?','jackfruit')
  #streamlit.write('The user entered ', add_my_fruit)
add_fruit_response = streamlit.text("Thanks for adding " +  add_my_fruit)

#insert input text into database
my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values ('from streamlit')")
