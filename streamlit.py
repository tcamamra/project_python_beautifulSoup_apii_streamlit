


from pathlib import Path
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from apii import *
import seaborn as sns
from matplotlib.pyplot import pie, axis, show
import requests
import plotly.express as px
from PIL import Image

st.title("bienvenue sur mon Dashboard de lirary")
st.image("t.png")
db = Dbconnect()

req = f'select * from lib'
db.dbcursor.execute(req)
results = db.dbcursor.fetchall()
columns = ["id","titles","notations","prices","availability"]
df = pd.DataFrame(results,columns=columns)
df.set_index("id",inplace = True)

def main():
    menu = ["Read","insert","update","Delete","view","about"]
    choice = st.sidebar.selectbox("Menu",menu)
  
   
    if choice == "Read":
          if st.checkbox('Show raw data'):
              st.subheader('Raw data')
              load_state = st.text('Loading Data..')
              st.write(df)
              load_state.text('Loading Completed!')
          
          valuet = st.text_input("entre la valeur a rechercher")
          search_choice= st.radio("Field to search by",df.columns)
          if st.button("Search"):
               if search_choice == "titles":
                    df[df["titles"]==valuet]
               elif search_choice == "notations":
                    df[df["notations"]==valuet]
               elif search_choice == "prices":
                    df[df["prices"]==valuet]
               elif search_choice == "availability":
                    df[df["availability"]==valuet]
                    
    elif choice == "insert":
         with st.form("my_form"):
               title = st.text_input('nom du livre')
               notations = st.text_input('notations du livre')
               prices = st.text_input('prices du livre')
               stock = st.text_input(' disponibilité')
               submit = st.form_submit_button("Submit")
               st.write('le livre est bien ajouter')
               def insertPage():
                    st.title("Ajouter un livre")
                    di = {"id": 1000,"titles":title,"notations":notations,"prices":prices,"availability":stock}
                    if submit:
                         requests.post("http://127.0.0.1:5000/record/{id}",json=di)
                         #st.write('le livre est bien ajoute')
         st.session_state.runpage = insertPage()

     
    elif choice == "update":
         valuet = st.text_input("entre la valeur a rechercher")
         search_choice= st.radio("Field to search by",df.columns)
         if st.button("Search"):
               if search_choice == "titles":
                    df[df["titles"]==valuet]
                    res = df[df["titles"]==valuet] 
               elif search_choice == "notations":
                    df[df["notations"]==valuet]
                    res = df[df["notations"]==valuet] 
               elif search_choice == "prices":
                    df[df["prices"]==valuet]
                    res = df[df["prices"]==valuet] 
               elif search_choice == "availability":
                    df[df["availability"]==valuet]
                    res = df[df["availability"]==valuet] 
                    def updatePage():
                         st.title("metre a jour un livre")
                         dii = {"id": _id,"titles":title,"notations":notations,"prices":prices,"availability":stock}
                         requests.put(f"http://127.0.0.1:5000/record/{_id}",json=dii)
                        
               with st.form("my_form"):
                    _id = st.text_input('ID title', res.index.values.astype(int)[0])
                    title = st.text_input('Movie title', res["titles"].values[0])
                    notations = st.text_input('notations title', res["notations"].values[0])
                    prices = st.text_input('prices title', res["prices"].values[0])
                    stock = st.text_input(' availability', res["availability"].values[0])
                    update = st.form_submit_button("submit")
                    if update:
                         updatePage()
                         st.write('lib est mis a jour')
               
               
      
    elif choice == "Delete":
        st.session_state.runpage = DeletePage()
    elif choice == "view":
         prices=st.slider("l'intervale des prix:",10,1000)
         st.write(f"le prix des livres {prices}")
         st.subheader(" Top 10 des livres ")
         grp_data = df
         grp_data['Count'] = 1
         k = pd.DataFrame(grp_data.groupby(['notations'], sort=False)['prices'].count().rename_axis(["Type of Crime"]).nlargest(10))
         Crime = pd.Series(k.index[:])
         Count = list(k['prices'][:])
         Crime_Count = pd.DataFrame(list(zip(Crime, Count)),
                               columns=['notations', 'prices'])
         fig = px.bar(Crime_Count, x='notations', y='prices', color='prices',
                 labels={'notations': 'livre_notation', 'prices': 'prix_livre'})
         st.plotly_chart(fig)

         fig, ax = plt.subplots()
         df.hist(
              bins=8,
              column="prices",
              grid=False,
              figsize=(8, 8),
              color="#86bf91",
              zorder=2,
              rwidth=0.9,
              ax=ax,
              )
         st.write(fig)
         fig = plt.figure(figsize=(30,30))
         sums = df.groupby("notations").sum()["prices"]
         axis('equal');
         pie(sums, labels=sums.index,autopct = "%1f%%" );
         fig = plt.gcf()
         fig.set_size_inches(30,12)
         sns.set(font_scale = 2)
          
         st.write(fig)

         

    else:
         
        ab= HelloWorld.apropos(HelloWorld)
        ab



    
def DeletePage():
     st.title("supprimer un livre")
     id = st.text_input("les informations du tuple que tu veux supprimer") 
     if st.button("Delete ce tuple"):
          HelloWorld.delete(HelloWorld, id)
          st.write('les informations sont bien suprimer de la librairie')
          
if __name__ == '__main__':
    main()

if st.button('Say hello'):
     st.write('Why hello there')
else:
     st.write('Goodbye')

