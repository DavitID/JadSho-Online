from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime
import os, json, requests, time

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
	kot = request.args.get("kota")
	if not kot:
		return render_template("index.html")
		
	return redirect(url_for("otw_res",kota = kot))

	
@app.errorhandler(json.decoder.JSONDecodeError)
def error(e):
    return render_template("handel_error.html")
    
@app.errorhandler(requests.exceptions.ConnectionError)
def network(e):
    return "NETWORK ERROR :)"
    
@app.route("/berhasil_ditemukan/<kota>", methods=['GET'])
def otw_res(kota):
	time = datetime.today().strftime('%Y-%m-%d')
	url = f"https://api.pray.zone/v2/times/day.json?city={kota}&date={time}"
	req = requests.get(url)
	jeson = json.loads(req.text)
	if jeson["code"] == 200:
	   	for hasil in jeson["results"]["datetime"]:
	   	  	tanggal = hasil["date"]["gregorian"]
	   	  	hijriah = hasil["date"]["hijri"]
	   	  	dzuhur = hasil["times"]["Dhuhr"]
	   	  	ashar = hasil["times"]["Asr"]
	   	  	maghrib = hasil["times"]["Maghrib"]
	   	  	isya = hasil["times"]["Isha"]
	   	  	subuh = hasil["times"]["Imsak"]
	   	  	
	   	  	return render_template("berhasil.html",tanggal = tanggal,hijriah = hijriah,kota = kota,subuh = subuh,duhur = dzuhur,ashar = ashar,maghrib = maghrib,isya = isya)

        
if __name__ == "__main__":
	app.run(debug = True)