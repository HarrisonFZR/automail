# -*- coding: utf-8 -*
# import necessary packages.
import pandas as pd
import numpy as np
import zipfile
import re
import datetime

def getYesterday():
      today = datetime.date.today()
      oneday = datetime.timedelta(days = 1)
      yesterday = today - oneday
      return yesterday

# 1. read csv files.
if getYesterday().day<10:
      
  df_ios = pd.read_csv('UTF-8\'\'HD_iOS_Daily_Auto_Final_r1%s%s0%s.csv'%(getYesterday().year, getYesterday().month, getYesterday().day))
  df_android = pd.read_csv('UTF-8\'\'HD_And_Auto_Final_r1%s%s0%s.csv'%(getYesterday().year, getYesterday().month, getYesterday().day))
  #UTF-8\'\'
  with zipfile.ZipFile('UTF-8\'\'HD_Web_Daily_Auto_Final%s%s0%s.zip'%(getYesterday().year, getYesterday().month, getYesterday().day)) as z:
    f = z.open('HD_Web_Daily_Auto_Final%s%s0%s.csv'%(getYesterday().year, getYesterday().month, getYesterday().day))
    t = pd.read_csv(f)
    t.to_csv('HD_Web_Daily_Auto_Final%s%s0%s.csv'%(getYesterday().year, getYesterday().month, getYesterday().day), encoding='utf_8_sig')
    f.close()
    z.close()

  df_web = pd.read_csv('HD_Web_Daily_Auto_Final%s%s0%s.csv'%(getYesterday().year, getYesterday().month, getYesterday().day))
  
else:
  df_ios = pd.read_csv('UTF-8\'\'HD_iOS_Daily_Auto_Final_r1%s%s%s.csv'%(getYesterday().year, getYesterday().month, getYesterday().day))
  df_android = pd.read_csv('UTF-8\'\'HD_And_Auto_Final_r1%s%s%s.csv'%(getYesterday().year, getYesterday().month, getYesterday().day))

  with zipfile.ZipFile('UTF-8\'\'HD_Web_Daily_Auto_Final%s%s%s.zip'%(getYesterday().year, getYesterday().month, getYesterday().day)) as z:
    f = z.open('HD_Web_Daily_Auto_Final%s%s%s.csv'%(getYesterday().year, getYesterday().month, getYesterday().day))
    t = pd.read_csv(f)
    t.to_csv('HD_Web_Daily_Auto_Final%s%s%s.csv'%(getYesterday().year, getYesterday().month, getYesterday().day), encoding='utf_8_sig')
    f.close()
    z.close()

  df_web = pd.read_csv('HD_Web_Daily_Auto_Final%s%s%s.csv'%(getYesterday().year, getYesterday().month, getYesterday().day))
  
      


#
# 2. calculate sum of pv and uv.
df_ios.rename(columns={'Article Name/ID (prop4)':'Article Name', 'Site Section (evar2)':'Site Section'},inplace=True)
df_android.rename(columns={'Article Name (evar4)':'Article Name', 'Site Section (evar2)':'Site Section'},inplace = True)
df_web.rename(columns={'Article Name (evar5)':'Article Name', 'Site Section (evar3)':'Site Section'},inplace = True)

df_ios = df_ios.fillna(0)
df_android = df_android.fillna(0)
df_web = df_web.fillna(0)

df_web.drop(['Page Name (prop1)','Page URL (evar2)', 'Unnamed: 0'],axis=1,inplace=True)
df_ios.drop(['Article ID (prop22)'], axis=1, inplace = True)
df_android.drop(['Article ID (prop22)'], axis=1, inplace = True)

#2.1 Article name cleaning part.
def filter_tags(htmlstr):
  re_cdata=re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I)
  re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)
  re_style=re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)
  re_br=re.compile('<br\s*?/?>')
  re_h=re.compile('</?\w+[^>]*>')
  re_comment=re.compile('<!--[^>]*-->')
  s=re_cdata.sub('',htmlstr)
  s=re_script.sub('',s)
  s=re_style.sub('',s)
  s=re_br.sub('\n',s)
  s=re_h.sub('',s)
  s=re_comment.sub('',s)
  blank_line=re.compile('\n+')
  s=blank_line.sub('\n',s)
  s=replaceCharEntity(s)
  return s

def replaceCharEntity(htmlstr):
  CHAR_ENTITIES={'nbsp':' ','160':' ',
        'lt':'<','60':'<',
        'gt':'>','62':'>',
        'amp':'&','38':'&',
        'quot':'"','34':'"', '039':'\'', 
        'mdash':'-', 'ensp':' ',
        'hellip':'…','middot':'·', #'hellip':'…','middot':'·','hellip':'...','middot':'.'
        'deg':'°', 'ndash':'–',
        'bull':'•', '-':'—'}
   
  re_charEntity = re.compile(r'&#?(?P<name>\w+);')
  sz = re_charEntity.search(htmlstr)
    
  while sz:
    entity = sz.group()
    key = sz.group('name')
    try:
      htmlstr = re_charEntity.sub(CHAR_ENTITIES[key],htmlstr,1)
      sz = re_charEntity.search(htmlstr)
    except KeyError:
      htmlstr = re_charEntity.sub('',htmlstr,1)
      sz = re_charEntity.search(htmlstr)
  return (htmlstr)

def replace(s,re_exp,repl_string):
  return (re_exp.sub(repl_string,s))

if __name__=='__main__':

  for i in range(len(df_ios['Article Name'])):
    if df_ios['Article Name'][i] == 0:
      continue
    else:
      df_ios['Article Name'][i] = filter_tags(df_ios['Article Name'][i])
      
  for i in range(len(df_android['Article Name'])):
    if df_android['Article Name'][i] == 0:
      continue
    else:
      df_android['Article Name'][i] = filter_tags(df_android['Article Name'][i])
      
  for i in range(len(df_web['Article Name'])):
    if df_web['Article Name'][i] == 0:
      continue
    else:
      df_web['Article Name'][i] = filter_tags(df_web['Article Name'][i])
    
  df_ios['Article Name'] = df_ios['Article Name'].str.strip()
  df_android['Article Name'] = df_android['Article Name'].str.strip()
  df_web['Article Name'] = df_web['Article Name'].str.strip()

#2.2 merge all datasets
df = pd.concat([df_ios, df_android, df_web])
df_sum1 = df.groupby(['Article Name', 'Site Section', 'Date']).sum()
df_sum1 = df_sum1.fillna(0)
df_sum1.reset_index(inplace = True, drop = False)
df_sum1.rename(columns={'Page Views':'Page Views Sum', 'Unique Visitors':'Unique Visitors Sum'},inplace=True)


# 3. merge the SUM file with the ios, android and web file.
df_ios = df_ios.groupby(['Article Name', 'Site Section', 'Date']).sum()
df_ios.reset_index(inplace = True, drop = False)
df_ios = df_ios.fillna(0)

df_sum2 = pd.merge(df_sum1,df_ios,on=['Article Name','Site Section', 'Date'], how = 'outer')
df_sum2.rename(columns={'Page Views':'Page Views ios', 'Unique Visitors':'Unique Visitors ios'},inplace=True)
df_sum2 = df_sum2.fillna(0)

df_android = df_android.groupby(['Article Name', 'Site Section', 'Date']).sum()
df_android.reset_index(inplace = True, drop = False)
df_android = df_android.fillna(0)

df_sum3 = pd.merge(df_sum2,df_android,on=['Article Name','Site Section', 'Date'], how = 'outer')
df_sum3.rename(columns={'Page Views':'Page Views android', 'Unique Visitors':'Unique Visitors android'},inplace=True)
df_sum3 = df_sum3.fillna(0)

df_web = df_web.groupby(['Article Name', 'Site Section']).sum()
df_web.reset_index(inplace = True, drop = False)
df_web = df_web.fillna(0)

df_sum4 = pd.merge(df_sum3,df_web,on=['Article Name','Site Section'], how = 'outer')
df_sum4.rename(columns={'Page Views':'Page Views Web', 'Unique Visitors':'Unique Visitors Web'},inplace=True)
df_sum4 = df_sum4.fillna(0)

#5. add up pv_ios and pv_android
df_sum_pv_app=[]
for i in range(len(df_sum4)):
      df_app_pv = df_sum4['Page Views ios'][i]+df_sum4['Page Views android'][i]
      df_sum_pv_app.append(df_app_pv)
df_sum4['Page Views App'] = df_sum_pv_app

df_sum_uv_app=[]
for i in range(len(df_sum4)):
      df_app_uv = df_sum4['Unique Visitors ios'][i]+df_sum4['Unique Visitors android'][i]
      df_sum_uv_app.append(df_app_uv)
df_sum4['Unique Visitors App'] = df_sum_uv_app

#6. remove ios and android
df_sum4.drop(['Page Views ios', 'Page Views android', 'Unique Visitors ios', 'Unique Visitors android'], axis=1, inplace = True)

#7. remove rows containing useless site sections
''' df_site = pd.read_csv('Site.csv')
df_site_N = list(df_site.loc[df_site['Y/N']=='N']['Site'])
df_sum4_site = df_sum4[~df_sum4['Site Section'].isin(df_site_N)]
df_sum5 = df_sum4_site
df_sum5.reset_index(inplace = True, drop = True) '''
df_sum5 = df_sum4
#8. adding all together, extracting all Chinese char in 'Article Name' as key to group by articles.
#df_sum4_site['Site Section'] = df_sum4_site['Site Section'].astype(str)
#df_sum5 = df_sum4_site.groupby(['Article Name', 'Date'],as_index=False).agg(lambda x : x.str.cat(sep=', ') if x.dtype == 'object' else x.sum())
ch = []
pattern="[\u4e00-\u9fa5]+" 
regex = re.compile(pattern)
for i in range(len(df_sum5)):
    result =  regex.findall(df_sum5['Article Name'][i])
    ch.append(result)
    
df_sum5['key'] = ch

for i in range(len(df_sum5)):
    df_sum5['key'][i] = ''.join(df_sum5['key'][i])
    
df_sum6 = df_sum5.groupby(['Date', 'key'],as_index=False).agg(lambda x : x.str.cat(sep='//// ') if x.dtype == 'object' else x.sum())
df_sum8 = df_sum6[~df_sum6['key'].isin([''])]
df_sum8.reset_index(inplace = True, drop = False)

one_name = []
for i in range(len(df_sum8)):
    one = df_sum8['Article Name'][i].split('////')[0]
    one_name.append(one)

df_sum8['Article Name'] = one_name

#9. descending order
df_sum8 = df_sum8.sort_values(by='Page Views Sum',ascending=False,axis=0)
df_sum8.reset_index(inplace = True, drop = False)
df_sum7 = df_sum8.head(500)
df_sum7['Headline'] = range(500)
df_sum7.drop(['key'], axis=1, inplace = True)

#10. columns re-ordering
#df_sum5 = df_sum5[['Top 400','Article Name',	'Site Section',	'Date',	'Page Views Sum',	'Page Views App',	'Page Views Web',	'Unique Visitors Sum',	'Unique Visitors App',	'Unique Visitors Web']]
df_sum7 = df_sum7[['Headline','Article Name', 'Date',	'Page Views Sum',	'Page Views App',	'Page Views Web',	'Unique Visitors Sum',	'Unique Visitors App',	'Unique Visitors Web']]
#df_sum7.reset_index(inplace = True, drop = True)

#11. subtract '0, ' from 'Site Section'
#for i in range(len(df_sum5['Site Section'])):
#    df_sum5['Site Section'][i] = re.sub('0, ','',df_sum5['Site Section'][i])

#12. remove 'Top 400' and 'Site Section' column.
#df_sum5.drop(['Top 400', 'Site Section'], axis=1, inplace = True)
df_sum7.drop(['Date'], axis=1, inplace = True)
df_sum7.set_index(['Headline'],inplace=True)


if getYesterday().day<10:
  file = open('HD_Data_Report_%s%s0%s.csv'%(getYesterday().year, getYesterday().month, getYesterday().day), "w", encoding='utf_8_sig')
  #df_sum5.to_csv(, encoding='utf_8_sig')
else:
  file = open('HD_Data_Report_%s%s%s.csv'%(getYesterday().year, getYesterday().month, getYesterday().day), 'w', encoding='utf_8_sig')
#df_sum5.to_csv(, encoding='utf_8_sig')
#df_sum5.to_csv('sum_mess.csv', encoding = 'utf_8_sig')
df_sum7.to_csv(file)
file.close()

#df_sum6.to_csv('sum_mess.csv', encoding = 'utf_8_sig')