from flask import Flask, render_template, request, jsonify
import json

import package as pk
app = Flask(__name__)

@app.route('/index', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('/index.html')
    else:
        timep = request.form['timep']
        target = request.form['stn']
        dn,up = pk.show_cong(timep=timep,target=target)
        return jsonify({'dn': dn, 'up': up})

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




if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)