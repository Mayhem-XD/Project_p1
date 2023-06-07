from flask import Flask, render_template, request
import folium
import pandas as pd
import os
import json
from urllib.parse import quote

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello Flask'

@app.route('/tour', methods=['GET', 'POST'])
def tour():
    tour = pd.read_csv('../data/수도권.csv')
    stn = pd.read_csv('../../main_code_test/data/stn_r_addr_final.csv')

    if request.method == 'GET':
        return render_template('tour.html')

    else:
        station_name = request.form['station']
        cat = request.form['cat']
        df = tour[tour.분류 == cat]
        lat = stn[stn.지하철역 == station_name].lat.iloc[0]
        lng = stn[stn.지하철역 == station_name].lng.iloc[0]
        print(tour.shape, df.shape)

        map = folium.Map(location=[lat, lng],zoom_start=15, width='100%', height='100%')
        for i in df.index:
            logo = folium.CustomIcon(f'data/icons/{df.분류[i]}.png', icon_size=(30,30))
            folium.Marker(
                location=[df.lat[i],df.lng[i]],
                popup=folium.Popup(df.도로명주소[i], max_width=200),
                tooltip=df.관광지명[i],
                icon=logo
            ).add_to(map)

        folium.Circle(
            location=[lat,lng],
            tooltip=station_name,
            radius=500,
            color="#ff7800",
            fill_color='#ffff00',
            fill_opacity=0.1
        ).add_to(map)
        map.save(os.path.join(app.static_folder, 'map/station.html'))

        return json.dumps('station.html')

if __name__ == '__main__':
    app.run(debug=True)

