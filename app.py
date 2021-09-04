from datetime import datetime
import os
from os.path import dirname, join
import sys
import json
from pdfrw import PdfReader
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from flask import Flask, abort, request, render_template, make_response
from io import BytesIO
from datetime import date, datetime
from flask_qrcode import QRcode
from dateutil.relativedelta import relativedelta


app = Flask(__name__, static_folder='./templates/assets')
app.config["JSON_AS_ASCII"] = False

def checkExistTf(val):
  if val is None:
    return 'false'
  else:
    return val

QRcode(app)

@app.route("/")
def start():
  return render_template("index.html", name="name")

@app.route("/english")
def eng():
  return render_template("english.html", name="name")
@app.route("/reader")
def read():
  return render_template("read.html")

@app.route("/genpdf", methods=["POST"])
def genpdf():
  today = date.today()
  address=request.form.get('address')
  name=request.form.get('name')
  ruby=request.form.get('ruby')
  phone=request.form.get('phone')
  birthdate=request.form.get('birthdate')
  vaccination_date=datetime.strptime(request.form.get('vaccination_date'), '%Y-%m-%d')
  birth = datetime.strptime(birthdate, '%Y-%m-%d')
  age = str(relativedelta(vaccination_date, birth).years)
  sex=checkExistTf(request.form.get('sex'))
  q1=request.form.get('q1')
  q2=request.form.get('q2')
  q3=request.form.get('q3')
  q4=request.form.get('q4')
  underlying_sikkan=request.form.get('underlying_sikkan')
  q5=request.form.get('q5')
  q6=request.form.get('q6')
  sick=request.form.get('sick')
  q7=request.form.get('q7')
  guai=request.form.get('guai')
  q8=request.form.get('q8')
  q9=request.form.get('q9')
  anaphylaxie_item=request.form.get('anaphylaxie_item')
  q10=request.form.get('q10')
  vaccine_item=request.form.get('vaccine_item')
  vaccine_shoujou=request.form.get('vaccine_shoujou')
  q11=request.form.get('q11')
  q12=request.form.get('q12')
  if q12 == 'true':
    vaccinated_type=request.form.get('vaccinated_type')
    vaccinated_when=str(datetime.strptime(request.form.get('vaccinated_when'), '%Y-%m-%d').month)+"/"+str(datetime.strptime(request.form.get('vaccinated_when'), '%Y-%m-%d').day)
  else:
    vaccinated_type=""
    vaccinated_when=""
  q13=request.form.get('q13')
  med = request.form.get('q4-addition-med')
  ov65 = request.form.get('q4-addition-65')
  ov60 = request.form.get('q4-addition-60')
  eld = request.form.get('q4-addition-eld')
  underlying = request.form.get('q4-addition-und')
  q5h = checkExistTf(request.form.get('q5-addition-h'))
  q5k = checkExistTf(request.form.get('q5-addition-k'))
  q5l = checkExistTf(request.form.get('q5-addition-l'))
  q5b = checkExistTf(request.form.get('q5-addition-b'))
  q5n = checkExistTf(request.form.get('q5-addition-n'))
  q5i = checkExistTf(request.form.get('q5-addition-i'))
  q5otc = checkExistTf(request.form.get('q5-addition-otc'))
  q5chiryou = checkExistTf(request.form.get('chiryou'))
  q5sara = checkExistTf(request.form.get('q5-addition-sara'))
  q5mb = checkExistTf(request.form.get('medicine_blood'))
  q5otm = checkExistTf(request.form.get('q5-addition-otm'))
  q5toy = checkExistTf(request.form.get('touyaku'))
  sharepdf = checkExistTf(request.form.get('pdf'))
  maker = checkExistTf(request.form.get('maker'))
  if maker == 'astrazeneca' or maker == 'dontknow':
    q5m = checkExistTf(request.form.get('q5-addition-mousai'))
  else:
    q5m = "false"
  if q1 == 'false':
    firstvac = (datetime.strptime(request.form.get('firstvaccine'), '%Y-%m-%d'))
  else:
    firstvac = date.today()
  if len(str(birth.month)) == 1:
    month = "0"+str(birth.month)
  else :
    month = str(birth.month)
  if len(str(birth.day)) == 1:
    day = "0"+str(birth.day)
  else :
    day = str(birth.day)
  json_file = {"address":address, "name":name, "ruby":ruby, "phone":phone,"year":str(birth.year), "month":month, "day":day, "age": age, "sex": sex, "maker": maker, "q1":[q1, str(firstvac.month), str(firstvac.day)], "q2":q2, "q3":q3, "q4":[q4, med, ov65, ov60, eld, underlying, underlying_sikkan], "q5":[q5,q5h,q5k,q5l,q5b,q5n,q5i,q5m,q5otc,q5chiryou,q5sara,q5mb,q5otm,q5toy], "q6":[q6, sick], "q7":[q7, guai], "q8":q8, "q9":[q9, anaphylaxie_item], "q10":[q10, vaccine_item, vaccine_shoujou], "q11":q11, "q12":[q12, vaccinated_type, vaccinated_when], "q13":q13}
  form_info = json_file
  if sharepdf == 'true':
    fontname_g = "ipag-mona"
    default_font_size = 12
    font_path = "./resource/ipag.ttf"
    if form_info['maker'] == 'astrazeneca' or form_info['maker'] == 'dontknow':
      file_in = "./resource/vaccine_yoshin_astra.pdf"
    else:
      file_in = "./resource/vaccine_yoshin_pfizer_takeda.pdf"
    output = BytesIO()
    cc = canvas.Canvas(output)
    def write_yes_no(x,y,answer):
        if answer == 'true':
            cc.drawString(x,y,'✓')
        else:
            cc.drawString(x + 45,y,'✓')

    def write_checkmark(x,y,answer):
        if answer == 'true':
            cc.drawString(x,y,'✓')

    def write_q1():
        answer = form_info['q1']
        answer = answer
        if answer[0] == 'false':
            cc.drawString(223,616,answer[1])
            cc.drawString(260,616,answer[2])
            # cc.drawString(340,616,answer[3])
            # cc.drawString(375,616,answer[4])
        write_yes_no(442,625,answer[0])
        return

    def write_q4():
        answer = form_info['q4']
        if answer[0] == 'true':
            write_checkmark(38,550,answer[1])
            write_checkmark(118,550,answer[2])
            write_checkmark(181,550,answer[3])
            write_checkmark(246,550,answer[4])
            write_checkmark(38,537,answer[5])
            cc.drawString(150,535,answer[6])

        write_yes_no(442,550,answer[0])

    def write_q5():
        answer = form_info['q5']
        if answer[0] == 'true':
            write_checkmark(86,497,answer[1])
            write_checkmark(132,497,answer[2])
            write_checkmark(181,497,answer[3])
            write_checkmark(228,497,answer[4])
            write_checkmark(284,497,answer[5])
            write_checkmark(384,497,answer[6])
            if form_info['maker'] == 'astrazeneca' or form_info['maker'] == 'dontknow':
              write_checkmark(85,480,answer[7])
              write_checkmark(192,480,answer[8])
              if answer[8] == 'true':
                cc.drawString(240,480,answer[9])
            write_checkmark(86,463,answer[10])
            if answer[10] == 'true':
              cc.drawString(190,463,answer[11])
            write_checkmark(286,463,answer[12])
            if answer[12] == 'true':
              cc.drawString(330,463,answer[13])
            else:
              if answer[8] == 'true':
                write_checkmark(86,480,answer[8])
                cc.drawString(130,480,answer[9])
              write_checkmark(86,463,answer[10])
              if answer[10] == 'true':
                cc.drawString(190,463,answer[11])
              write_checkmark(286,463,answer[12])
              if answer[12] == 'true':
                cc.drawString(330,463,answer[13])
        write_yes_no(442,488,answer[0])


    def write_q6():
        answer = form_info['q6']
        if answer[0] == 'true':
            cc.drawString(300,441,answer[1])

        write_yes_no(442,442,answer[0])

    def write_q7():
        answer = form_info['q7']
        if answer[0] == 'true':
            cc.drawString(240,420,answer[1])

        write_yes_no(442,422,answer[0])

    def write_q9():
        answer = form_info['q9']
        if answer[0] == 'true':
            cc.drawString(170,370,answer[1])

        write_yes_no(442,377,answer[0])

    def write_q10():
        answer = form_info['q10']
        if answer[0] == 'true':
            cc.drawString(70,342,answer[1])
            cc.drawString(280,342,answer[2])
        write_yes_no(442,350,answer[0])

    def write_q12():
        answer = form_info['q12']
        if answer[0] == 'true':
            cc.drawString(227,304,answer[1])
            cc.drawString(380,304,answer[2])
        write_yes_no(442,305,answer[0])

    def write_name(x,y,name):
        cc.setFont(fontname_g,11)
        cc.drawString(x,y,name)
        cc.setFont(fontname_g,default_font_size)

    def write_number(x,y,number):
        number_list = list(number)
        if not '.' in number_list:
            for num in number_list:
                cc.drawString(x,y,num)
                x = x + 16
        else:
            cc.drawString(x,y,number_list[0])
            cc.drawString(x + 16,y,number_list[1])
            cc.drawString(x + 55,y,number_list[3])

    def test_method():
        x = 0
        y = 0
        while x < 600 or y < 800:
            cc.drawString(x,0,str(x / 100))
            cc.drawString(0,y,str(y / 100))
            x = x + 100
            y = y + 100

    pdfmetrics.registerFont(TTFont(fontname_g,font_path))
    cc.setFont(fontname_g,default_font_size)

    page = PdfReader(file_in,decompress=False).pages
    pp = pagexobj(page[0])
    cc.doForm(makerl(cc, pp))

    if int(form_info['age']) < 100:
        form_info['age'] = '0' + form_info['age']

    phone = form_info['phone'].split("-")

    # 予診票に書き込み
    cc.drawString(60,755,form_info['address'])
    if len(form_info['name']) <= 10:
        cc.drawString(60,690,form_info['name'])
    else:
        write_name(60,690,form_info['name'])
    cc.drawString(273,705,phone[0])
    cc.drawString(273,690,phone[1])
    cc.drawString(330,690,phone[2])
    write_number(67,665,form_info['year'])
    write_number(145,665,form_info['month'])
    write_number(188,665,form_info['day'])
    write_number(263,665,form_info['age'])

    cc.setFont(fontname_g,12)
    cc.drawString(65,710,form_info['ruby'])
    if form_info['sex'] == 'male':
        cc.drawString(338,669,'✓')
    elif form_info['sex'] == 'female':
        cc.drawString(373,669,'✓')
    write_q1()
    write_yes_no(442,600,form_info['q2'])
    write_yes_no(442,580,form_info['q3'])
    write_q4()
    write_q5()
    write_q6()
    write_q7()
    write_yes_no(442,402,form_info['q8'])
    write_q9()
    write_q10()
    write_yes_no(442,325,form_info['q11'])
    write_q12()
    write_yes_no(442,285,form_info['q13'])

    cc.drawString(377,186,'✓')

    cc.showPage()
    cc.save()
    pdf_out = output.getvalue()
    output.close()
    response = make_response(pdf_out)
    response.headers['Content-Disposition'] = "attachment; filename=yoshinhyo.pdf"
    response.mimetype = 'application/pdf'
    return response
  else:
    return render_template("share.html", json = json_file)

if __name__ == "__main__":
  app.run(debug=True)
