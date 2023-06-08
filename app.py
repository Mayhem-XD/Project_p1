from flask import Flask, render_template, request
import json

import package as pk
app = Flask(__name__)

@app.route('/index')
def home():
    return render_template('/index.html')

@app.route('/heatmap',methods=['GET','POST'])
def heatmap():
    if request.method == 'GET':
        return render_template('/landing.html')
    else:
        line = request.form['line']
        target = request.form['target']
        smonth_ = request.form['sm']
        emonth_ = request.form['em']
        smonth = int(smonth_.replace("-", ""))
        emonth = int(emonth_.replace("-", ""))
        temp = pk.show_heatmap(app=app,line=line,target=target,smonth=smonth,emonth=emonth)
        return json.dumps(temp)
    
@app.route('/tour', methods=['GET', 'POST'])
def tour():
    if request.method == 'GET':
        return render_template('/tour.html')
    else:
        station_name = request.form['target']
        cat = request.form['cat']
        temp = pk.show_tour_map(app=app,station_name=station_name,cat=cat)
        return json.dumps(temp)

@app.route('/generic')
def generic():
    return render_template('/generic.html')


# @app.route('/self_intr')
# def self_intr():
#     menu = {'ho':0,'us':1,'cr':0,'sc':0}
#     return render_template('prototype/self_intr.html')

# @app.route('/crawling/interpark',methods=['GET','POST'])
# def interpark():
#     return render_template('prototype/interpark.html')

# @app.route('/crawling/genie',methods=['GET','POST'])
# def genie():
#     return render_template('prototype/genie.html')

# @app.route('/crawling/siksin',methods=['GET','POST'])
# def siksin():
#     menu = {'ho':0,'us':0,'cr':1,'sc':0}
#     if request.method == 'GET':
#         return render_template('prototype/siksin.html')
#     else:
#         place = request.form['place']
#         siksin_list = ut.siksin_search(place)
#         return render_template('prototype/siksin_res.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)