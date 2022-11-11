import numpy as np
import os
from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd

app = Flask(__name__)
model = pickle.load(open('C:\\Users\\DELL\\PycharmProjects\\rough use\\rfmodel.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('mainpage.html')

@app.route('/predict',methods=['POST','GET'])
def predict():

    sm=[6,7,8]
    wt=[9,10,11]
    sp=[12,1,2,3]
    fl=[4,5]
    farr= [int(x) for x in request.form.values()]
    if farr[1] in sm:
        farr.append(0)
    elif farr[1] in wt:
        farr.append(1)
    elif farr[1] in sp:
        farr.append(2)
    else:
        farr.append(3)
    final_features=np.array(farr,dtype='int64')
    print(final_features)
    payload_scoring = {"input_data": [{"fields": [['QUARTER', 'MONTH', 'DAY_OF_MONTH', 'DAY_OF_WEEK', 'FL_NUM', 'ORIGIN', 'DEST', 'CRS_DEP_TIME.1','CRS_ARR_TIME.1', 'CRS_ELAPSED_TIME', 'DISTANCE', 'SEASON']], "values": [final_features]}]}
    response_scoring = requests.post('http://127.0.0.1:5000',json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    pred = response_scoring.json()
    print(pred)
    prediction = pred['predictions'][0]['values'][0][0]
    prediction = model.predict([final_features])
    print(prediction)

    output = round(prediction[0])

    if output==0:
        return render_template('mainpage.html', prediction_text='No delay will happen {}'.format(output))
    elif output==1:
        return render_template('mainpage.html', prediction_text='There is a chance to departure delay will happen {}'.format(output))
    elif output==2:
        return render_template('mainpage.html', prediction_text='here is a chance to both departure and arrival delay will happen {}'.format(output))
    elif output==3:
        return render_template('mainpage.html', prediction_text='here is a chance to flight  will diverted {}'.format(output))
    elif output==4:
        return render_template('mainpage.html', prediction_text='here is a chance to cancel the flight {}'.format(output))
    else:
        return render_template('mainpage.html', prediction_text='output {}'.format(output))


if __name__ == "__main__":
    os.environ.setdefault('FLASK_ENV', 'development')
    app.run(debug=False)