from bs4 import BeautifulSoup
import requests
import time
from pyGoogleSearch import *
#هنا المعلومات التي نحتاجها في البحث تلاحظ استخدامي لدالة str و int وذلك لتجنب كثير من المشاكل:)
#هنا نطلب نطاق البحث مثل simple.com
Domain_websit = str(input("Type the website you want to search >>"))
Domain_email = str(input("enter Domain email like hotmail.com >>"))
#عدد صفحات البحث في جوجل
page_search = int(input("Enter the number of search pages >>"))
#اسم الملف الخاص بنتائج البحث
file_name= str(input("Enter the namesave file >>"))
#هنا نفتح ملف الي راح نكتب في النتائج
file= open('{}.txt'.format(file_name), 'w+')
#هذي اليست مدري وش سالفتها
list_email=[]
email_encryption=[]
#نفتح ليست عشان نظيف فيها الروابط فقط
list_search_websit=[]

#هنا نبحث بستخدام المكتبة ونسندها لم المتغير search1
search1 = Google(Domain_email, site='{}'.format(Domain_websit),pages=10).search()
#هنا راح يحط النتائج البحث في جوجل في ليست غير مرتبه و يحط معها معلومات ما نحتاجها
#وتذكر اننا نحتاج الروابط فقط في عملية البحث :)
output_web_data = DataHandler(search1).aggregate_data()
#نستخدم دالة len حتى نحسب عدد النتائج البحث ونستخدمها في لوب for
t=len(output_web_data)
#في لوب for بدأنا من 1 لان نتيجة 0 غير مهمة فيها فقط معلومات الترتيب الخاص بالبحث
for i in range(1,t-1):
    q=output_web_data[i][0]
    list_search_websit.append(q)
#الان بعدما انتهينا من الروابط نحتاج ان نكتب الدوال الخاصة بستخراج الايميل منها
#سنحتاج اكثر من دالة وقد نزيد في المستقبل لان المواقع تختلف في طريقة عرض الايميلات
#وفي هذا الكود سنقوم بكتابة دالتين دالة للمواقع التي تعرض الايميل كارابط ودالة للمواقع التي تستخدم حماية تشفير عرض الايميل :)
#هذي الدالة تبحث عن الايميلات التي يتم عرضها كا روابط
def search_email(i):
    try:
        #هنا نقوم بطلب الرابط
        req = requests.get(str(i))
        bs = BeautifulSoup(req.text,"html.parser")
        print("Processing {}".format(i))
    except:
        print("erorr requests {}".format(i))
    #هذا لوب لاستخراج الروابط الموجودة في صفحة سوى كانت ايميلات او غيره
    for link in bs.findAll('a'):
        s =link.get("href")
        #هنا نضع شرط if حتى نستطيع فصل الايميلات عن الروابط الاخرى
        if "@" in str(s):
            q=s.split(":")
            try:
                #هنا نستخدم شرط if حتى نتاكد ان الايميل غير مكرر
                if q[1] not in list_email:
                    list_email.append(q[1])
                else:
                    continue
            except:
                continue
#قد تستغرب من استخدامي الكثير لدالة try وسبب هو كثرة المشاكل الي قد تمر عليك في هذي العملية وحتى تتخطها بدون كتابة سطور اضافية اسستخدم هذي الدالة

#هذي الدالة للايميلات المشفرة
def search_email_protection(i):
    req = requests.get(str(i))
    bs = BeautifulSoup(req.text,"html.parser")
    print("Processing {}".format(i))
    for i in bs.findAll('a'):
        #print(i.get("href"))
        z=i.get("href")
        #نبحث عن اليميل المشفر
        if 'email-protection' in z:
            try:
                k=z.split("#")
                #نقوم باضافة الايميل المشفر الى لسته حتى نستطيع فكه
                email_encryption.append(k[1])
            except:
                print("erorr {}".format(i))
                continue
        else:
            continue
    #هنا نقوم بفك تشفير الايميلات
    for email in email_encryption:
        email2 = cfDecodeEmail(email)
        #هنا نتاكد ان لايميل غير مكرر
        if email2 not in list_email:
            list_email.append(email2)
        else:
            continue

#هنا دالة فك تشفير الايميل وهي من برمجة ()
def cfDecodeEmail(encodedString):
    r = int(encodedString[:2],16)
    email = ''.join([chr(int(encodedString[i:i+2], 16) ^ r) for i in range(2, len(encodedString), 2)])
    return email
#اخير نقوم بكتابة لوب للبحث عن الايميل داخل الصفحة
for i in list_search_websit:
    req = requests.get(str(i))
    bs = BeautifulSoup(req.text, "html.parser")
    #سنحتاج هذا المتغيرين حتى نعرف نوع الصفحة ونوع الدالة التي سنستخدمها عليها
    source = []
    protection =0
    for c in bs.findAll('a'):
        # print(i.get("href"))
        z = c.get("href")
        source.append(z)
    for v in source:
        #بعد ان جمعت الروابط ابحث عن كلمة email-protection اذا كانت موجودة سنستخدم دالة الايميلات المشفرة
        try:
            if 'email-protection' in v:
   #هنا خطوة مهمة وتفيدنا مستقبلا اذا اردنا ان نظيف اكثر من طريقة بحث لكن الان نقول له اجعل protection يساوي 1 اذا كان الموقع يستخدم التشفير
                protection=1
                break
        except:
            continue
#هنا واضح حيث قلت له اذا كان protection يساوي 1 نقوم بستخدام دالة الايميلات المسفرة واذا كان غير ذلك نستخدم الدالة العادية
    if protection ==1:
        search_email_protection(i)
    else:
        search_email(i)
#هنا نقوم بكتابة النتائج الخاصة بالبحث في ملف عن طريق لوب
t_email=len(list_email)
for i in range(0,t_email-1):
    file.write(list_email[i])
    #نضيف سطر جديد حتى لا تكون النتائج في سطر واحد
    file.write("\n")

file.close()



