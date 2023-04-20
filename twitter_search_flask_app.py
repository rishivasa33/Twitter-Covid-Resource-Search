
# Flask App with Python to search Twitter for Covid Resources
# Developed by Rishi Vasa

from flask import Flask, render_template, request
from requests.utils import requote_uri

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/TwitterCovidResourceSearch")
def index():
    return render_template("TwitterCovidResourceSearch.html")

@app.route("/TwitterCovidResourceSearch", methods=["GET", "POST"])
def search():
    errors = ""
    searchURL = ""
    if request.method == "POST":
        cityName = None
        searchParams = None
        otherParams = None
        excludedParams = None
        otherExcludedParams = None
        #Input Validations
        try:
            cityName = request.form["cityName"]
        except:
            errors += "{!r} is not a valid City Name.\n".format(request.form["cityName"])

        if cityName.isalpha() == False:
            errors += "{!r} is not a valid City Name.\n".format(request.form["cityName"])

        try:
            searchParams = request.form.getlist('check')
        except:
            errors += "Invalid Search Parameters Selected.\n"

        try:
            otherParams = request.form["other"]
        except:
            errors += "{!r} is not a valid Search Parameter.\n".format(request.form["other"])

        try:
            excludedParams = request.form.getlist('exclude')
        except:
            errors += "Invalid Search Options Selected.\n"

        try:
            otherExcludedParams = request.form["otherExclude"]
        except:
            errors += "{!r} is not a valid Search Option.\n".format(request.form["otherExclude"])

        #Generate Search URL
        if cityName is not None and searchParams is not None and (searchParams or otherParams):
            if errors is None or errors == "":
                searchURL = getSearchURL(cityName, searchParams, otherParams, excludedParams, otherExcludedParams)
        else:
            errors += "Insufficient Search Parameters Selected.\n"

    #Re-render template with searchURL button to redirect to Twitter
    return render_template("TwitterCovidResourceSearch.html", errors=errors, searchURL=searchURL)



def getSearchURL(cityName, searchParams, otherParams, excludedParams, otherExcludedParams):

    base_url = "https://twitter.com/search?q="
    verifiedStr = ""
    searchParamsStr = ""
    unverifiedStr = ""
    neededStr = ""
    requiredStr = ""
    otherExcludedParamsStr = ""

    if otherParams is not None and otherParams and otherParams != "":
        if searchParams is None or not searchParams or searchParams == "":
            searchParamsStr = " (" + otherParams +")"
        else:
            searchParamsStr = " ("+' OR '.join(searchParams) + " OR " + otherParams +")"
    else:
        searchParamsStr = " ("+' OR '.join(searchParams)+")"

    if 'verified' in excludedParams:
        verifiedStr = "verified "

    if 'unverified' in excludedParams:
        unverifiedStr = """ -"not verified" -"unverified" """

    if 'needed' in excludedParams:
        neededStr = """ -"needed" -"need" -"needs" """

    if 'required' in excludedParams:
        requiredStr = """ -"required" -"require" -"requires" -"requirement" -"requirements" -"reqd" """

    if otherExcludedParams is not None and otherExcludedParams and otherExcludedParams != "":
        otherExcludedParamsStr = """-" """+otherExcludedParams+""" " """

    final_url = requote_uri(base_url + verifiedStr + cityName + searchParamsStr + unverifiedStr + neededStr + requiredStr + otherExcludedParamsStr + "&f=live")

    return final_url