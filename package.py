import numpy as np
import pandas as pd
import os,glob
from urllib.parse import quote 
import requests,json,os

main_datafile_path = 'data/'
temp_files_path = 'data/temp_files/'
main_file_name = f'{main_datafile_path}metro_ridership_by_line_stn_time.csv'
xlsx_path = 'data/total_stn_info_20230317.xlsx'
temp_info_name = f'{temp_files_path}temp_info.csv'
key_path = 'data/key/kakaoapikey.txt'
heatmap_data = f'{main_datafile_path}merged_lines.csv'

def stn_name_modification(name=main_file_name):
    if name == main_file_name:
        df_st = pd.read_csv(name,encoding='euc-kr')
        df_st['지하철역'] = df_st['지하철역'].str.replace('(', ' ',regex=False,).str.split().str[0]
        for i in df_st.index:
            if df_st.loc[i, '지하철역'][-1] == '역':
                df_st.loc[i, '지하철역'] = df_st.loc[i, '지하철역'][:-1]
        return df_st
    else:
        df_st = pd.read_csv(name,encoding='euc-kr')
        df_st.drop(columns=['등록일자'],inplace=True)
        df_st.rename(columns={'역명': '지하철역'},inplace=True)
        df_st['지하철역'] = df_st['지하철역'].str.replace('(', ' ',regex=False,).str.split().str[0]
        for i in df_st.index:
            if df_st.loc[i, '지하철역'][-1] == '역':
                df_st.loc[i, '지하철역'] = df_st.loc[i, '지하철역'][:-1]
        return df_st
    
def line_sep_preproc_main():
    si_list = '오이도 정왕 신길오천 안산 초지 고잔 중앙 한대앞'.split()
    copy_list = []
    df = stn_name_modification()
    lines = df.호선명.unique().tolist()
    df_dict = {line: df[df['호선명'] == line].copy() for line in lines}
    for line, frame in df_dict.items():
        frame['새벽 승차인원'] = frame.loc[:,['04시-05시 승차인원','05시-06시 승차인원']].sum(axis=1)
        frame['새벽 하차인원'] = frame.loc[:,['04시-05시 하차인원','05시-06시 하차인원']].sum(axis=1)

        frame['출근시간 승차인원'] = frame.loc[:,['06시-07시 승차인원','07시-08시 승차인원','08시-09시 승차인원']].sum(axis=1)
        frame['09-16시 승차인원'] = frame.loc[:,['09시-10시 승차인원','10시-11시 승차인원','11시-12시 승차인원',
                                                '12시-13시 승차인원','13시-14시 승차인원','14시-15시 승차인원','16시-17시 승차인원']].sum(axis=1)
        frame['퇴근시간 승차인원'] = frame.loc[:,['17시-18시 승차인원','18시-19시 승차인원','19시-20시 승차인원']].sum(axis=1)
        frame['야간 승차인원'] = frame.loc[:,['20시-21시 승차인원','21시-22시 승차인원','22시-23시 승차인원',
                                            '23시-24시 승차인원','00시-01시 승차인원','01시-02시 승차인원']].sum(axis=1)
        frame['출근시간 하차인원'] = frame.loc[:,['06시-07시 하차인원','07시-08시 하차인원','08시-09시 하차인원']].sum(axis=1)
        frame['퇴근시간 하차인원'] = frame.loc[:,['17시-18시 하차인원','18시-19시 하차인원','19시-20시 하차인원']].sum(axis=1)
        frame['09-16시 하차인원'] = frame.loc[:,['09시-10시 하차인원','10시-11시 하차인원','11시-12시 하차인원',
                                                '12시-13시 하차인원','13시-14시 하차인원','14시-15시 하차인원','16시-17시 하차인원']].sum(axis=1)
        frame['야간 하차인원'] = frame.loc[:,['20시-21시 하차인원','21시-22시 하차인원','22시-23시 하차인원',
                                            '23시-24시 하차인원','00시-01시 하차인원','01시-02시 하차인원']].sum(axis=1)
        frame['총 승차인원'] = frame.loc[:,['새벽 승차인원','출근시간 승차인원','09-16시 승차인원','야간 승차인원']].sum(axis=1)
        frame['총 하차인원'] = frame.loc[:,['새벽 하차인원','출근시간 하차인원','09-16시 하차인원','야간 하차인원']].sum(axis=1)
        frame = frame[['사용월', '호선명', '지하철역', '출근시간 승차인원', '출근시간 하차인원', 
                        '09-16시 승차인원', '09-16시 하차인원', '퇴근시간 승차인원', '퇴근시간 하차인원',
                        '새벽 승차인원','새벽 하차인원','야간 승차인원', '야간 하차인원','총 승차인원','총 하차인원']]
        
        frame.loc[(frame['호선명'] == '2호선') & (frame['지하철역'] == '신천'), '지하철역'] = '잠실새내'
        # 수인선 누락 추가
        frame_copy = frame[(frame['호선명']=='안산선')&(frame['지하철역'].isin(si_list))].copy()
        frame_copy['호선명'] = frame_copy['호선명'].apply(lambda x: '수인선_누락')
        frame_copy = frame_copy.reset_index(drop=True)
        copy_list.append(frame_copy)
        frame.to_csv(f'{temp_files_path}{line}.csv',index=False,encoding='utf-8')
    pd.concat(copy_list).to_csv(f'{temp_files_path}수인선_누락.csv',index=False,encoding='utf-8')
    return None

# 미리 정해둔 양식으로 호선을 분리
# 2019 이후 자료에는 9호선 2단계가 없어서 따로 처리
def rtn_line_info(year):
    path = temp_files_path
    line_info = [
        ([f'{path}1호선.csv', f'{path}경부선.csv', f'{path}경원선.csv', f'{path}경인선.csv', f'{path}장항선.csv'], '1호선'),
        ([f'{path}2호선.csv'], '2호선'),
        ([f'{path}3호선.csv', f'{path}일산선.csv'], '3호선'),
        ([f'{path}4호선.csv', f'{path}과천선.csv', f'{path}안산선.csv'], '4호선'),
        ([f'{path}5호선.csv'], '5호선'),
        ([f'{path}6호선.csv'], '6호선'),
        ([f'{path}7호선.csv'], '7호선'),
        ([f'{path}8호선.csv'], '8호선'),
        ([f'{path}수인선.csv',f'{path}수인선_누락.csv', f'{path}분당선.csv'], '수인분당선'),
        ([f'{path}경의선.csv', f'{path}중앙선.csv'], '경의중앙선'),
        ([f'{path}공항철도 1호선.csv'], '공항철도')
    ]
    if year >= 2019:
        line_info.append(([f'{path}9호선.csv', f'{path}9호선2~3단계.csv'], '9호선'))
    else:
        line_info.append(([f'{path}9호선.csv', f'{path}9호선2단계.csv', f'{path}9호선2~3단계.csv'], '9호선'))
    return line_info

def rm_temp_files():
    temp_path = os.path.join('data', 'temp_files', '*.csv')
    for file in glob.glob(temp_path):
        os.remove(file)
    return None

def rm_temp_info_files(year,ck_week):
    file = os.path.join('data',  f'{year}_{ck_week}_sub_info.csv')
    os.remove(file)
    return None

def preprocessing_lines(year=2019):
    line_list = []
    line_info = rtn_line_info(year)
    for df_list, line_name in line_info:
        df_copies = []
        for file in df_list:
            df = pd.read_csv(file)
            df_copies.append(df.copy())
        result = pd.concat(df_copies, axis=0)
        result = result.reset_index(drop=True)
        result.호선명 = line_name
        cols = list(result.columns)[:3]
        target = list(result.columns)[3:]
        res = result.groupby(cols)[target].agg('sum').reset_index()
        line_list.append(res)
    final = pd.concat(line_list,axis=0)
    rm_temp_files()
    return final

def preproc_main():
    line_sep_preproc_main()
    final = preprocessing_lines()
    final.to_csv(f'{main_datafile_path}merged_lines.csv',index=False)
    return None

def stn_sub_modification(year,ck_week):
    name = f'{main_datafile_path}{year}.csv'
    
    df1 = stn_name_modification(name)
    cols = list(df1.columns)[:3]
    target = list(df1.columns)[3:]
    df1['사용일자'] = pd.to_datetime(df1['사용일자'], format='%Y%m%d')
    # 평일과 주말 구분하는 새로운 열 생성
    df1['주중/주말'] = df1['사용일자'].apply(lambda x: '주말' if x.weekday() >= 5 else '주중')
    # 주중/주말 선택    나중에 에러방지 추가해야함
    rtn_week = '주중' if ck_week == '주중' else '주말'
    weekday_df = df1[df1['주중/주말'] == rtn_week]
    week_df = weekday_df.copy()
    week_df['사용일자'] = pd.to_datetime(weekday_df['사용일자']).dt.strftime('%Y%m%d').astype(int)
    df_list = []
    for i in range(1, 13):
        start_date = year*10000 + i*100
        end_date = start_date + 100
        df_temp = week_df[(week_df['사용일자'] >= start_date) & (week_df['사용일자'] < end_date)].copy()
        df_temp['사용일자'] = year*100 + i
        df_temp = df_temp.groupby(cols)[target].agg('sum').reset_index()
        df_list.append(df_temp)
    df_res = pd.concat(df_list, axis=0)
    df_res.to_csv(f'{main_datafile_path}{year}_{ck_week}_sub_info.csv', index=False)
    return None

def preproc_sub(year,ck_week):
    
    stn_sub_modification(year,ck_week)
    df = pd.read_csv(f'{main_datafile_path}{year}_{ck_week}_sub_info.csv')
    df = df.rename(columns={'역명': '지하철역', '노선명':'호선명', '사용일자':'사용월'})
    
    lines = df.호선명.unique().tolist()
    df_dict = {line: df[df['호선명'] == line].copy() for line in lines}
    for line, frame in df_dict.items():
        frame.loc[(frame['호선명'] == '2호선') & (frame['지하철역'] == '신천'), '지하철역'] = '잠실새내'
        frame.to_csv(f'{temp_files_path}{line}.csv',index=False,encoding='utf-8')

    final = preprocessing_lines(year)
    rm_temp_files()
    rm_temp_info_files(year,ck_week)
    final.to_csv(f'{main_datafile_path}{year}_{ck_week}_merged_lines.csv',index=False)

def kakao_location(place):
    with open({key_path}) as f_:
        kakao_key = f_.read()
    base_url = "https://dapi.kakao.com/v2/local/search/address.json"
    url = f'{base_url}?query={quote(place)}'
    header = {'Authorization':f'KakaoAK {kakao_key}'}
    result = requests.get(url, headers=header).json()
    lat_ = float(result['documents'][0]['y'])
    lng_ = float(result['documents'][0]['x'])
    return lat_,lng_

def rtn_addr(df,target):
    str_addr = df[df.지하철역 == target].도로명주소.values[-1]
    return str_addr.strip()

def get_stn_lat_lng():
    df = pd.read_excel(xlsx_path,engine='openpyxl')
    df.to_csv(temp_info_name,index=False)
    df = pd.read_csv(temp_info_name)
    df = df[['역사명','역사도로명주소','운영기관명']]
    df.rename(columns={'역사명':'지하철역','역사도로명주소':'도로명주소'},inplace=True)
    exclude_list = ['대전교통공사', '대구도시철도공사', '부산광역시 부산교통공사', '부산-김해경전철㈜','광주광역시 도시철도공사']
    for exclude in exclude_list:
        df = df[df['운영기관명'] != exclude]
    df.drop(columns=['운영기관명'],inplace=True)
    df['지하철역'] = df['지하철역'].str.replace('(', ' ',regex=False,).str.split().str[0]
    for i in df.index:
        if df['지하철역'][i][-1] == '역':
            df['지하철역'][i] = df['지하철역'][i][:-1]
    df.drop_duplicates(subset=['지하철역'],keep='first',inplace=True)
    df = df[~df['도로명주소'].str.contains('부산|울산')]
    df.reset_index(drop=True,inplace=True)
    
    temp1 =[]
    for i in df.index:
        try:
            target = df['지하철역'][i].strip()
            temp1.append(kakao_location(rtn_addr(df,target)))
        except:
            print(i, df.지하철역[i])
            
    df_test = pd.DataFrame(temp1,columns=('lat','lng'))
    df2 = pd.concat([df, df_test], axis=1)
    df2.to_csv(f'{main_datafile_path}stn_r_addr_final.csv',index=False)
    return None


def add_lat_lng(name=heatmap_data):
    df_latlng = pd.read_csv(f'{main_datafile_path}stn_r_addr_final.csv')
    df_latlng.drop(columns=['도로명주소'], inplace=True)

    df_main = pd.read_csv(name)
    res = pd.merge(df_main, df_latlng, on='지하철역', how='left')
    res.to_csv(f'{main_datafile_path}lines_4heatmap_{name[5:9]}.csv', index=False)
    return None