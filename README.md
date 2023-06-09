# 역이어때
* 팀장 주건혁   
* 조원 도현명
* 조원 이지혜   
* 조원 이형준  

<h1>수도권 지하철 유동인구 데이터 기반 분석 프로젝트</h1>

<h3>프로젝트 소개</h3>

> 많은 사람들이 이용하는 지하철의 유동인구 데이터를 수집, 가공</br>
> 그 데이터를 분석해서 어떻게 활용할 수 있는지 알아본다
> 
<h3>개발 과정</h3>

>   * 협업툴<br>
>   ![gicon1](https://github.com/Mayhem-XD/Project_p1/assets/116787370/395b6da2-606f-450e-8ded-f01f406e1e64) ![gd](https://github.com/Mayhem-XD/Project_p1/assets/116787370/150ffdc3-049c-47ba-b3d6-81a49b8c2b5c)<br>
>   * 기본 라우팅 테이블<br>
>   ![table](https://github.com/Mayhem-XD/Project_p1/assets/116787370/2dcdfcd6-3465-4c5e-95a0-f4922cc8c841)
>   * 개발도구<br>
>   ![python](https://github.com/Mayhem-XD/Project_p1/assets/116787370/8b7153e0-e96e-42c8-97da-dac77852ea70)
>   ![flask](https://github.com/Mayhem-XD/Project_p1/assets/116787370/ad564b8b-287a-4444-bfb5-d554668e546e)
>   ![vscode](https://github.com/Mayhem-XD/Project_p1/assets/116787370/5c1215e8-01f9-4f42-8d02-aed1e5842c24)<br>
>   * 웹 화면<br>
>   ![index](https://github.com/Mayhem-XD/Project_p1/assets/116787370/4414759c-3645-49e3-86ff-c3d4e4188d90)<br>
>   ![cong](https://github.com/Mayhem-XD/Project_p1/assets/116787370/08ce7029-d0ce-4c51-a6e2-bc8c9849ac4d)<br>
>   ![cong2](https://github.com/Mayhem-XD/Project_p1/assets/116787370/0dd58280-4cb1-4fef-a15b-ba04aac54013)<br>
>   ![h](https://github.com/Mayhem-XD/Project_p1/assets/116787370/c2d55ef8-653d-49cc-b67e-60d3fb83d1dc)<br>
>   ![h2](https://github.com/Mayhem-XD/Project_p1/assets/116787370/1889b017-efff-4fd7-82c3-343a81706f33)<br>
>   ![tour](https://github.com/Mayhem-XD/Project_p1/assets/116787370/66858cf8-a5d6-4c88-bdb4-0dff254af704)<br>



프로젝트 코드 일부

~~~ javascript
<script>
// timepicker를 사용하고 10분 단위,24시간 단위로 입력을 받고 시작 시간을 04:00 하기 위한 옵션을 줌
    $(document).ready(function () {
        $('input.timepicker').timepicker({
                timeFormat: 'HH:mm',
                interval: 10,
                startTime: '04:00',
                dynamic: false,
                dropdown: true,
                scrollbar: true
                });
});
</script>
~~~

~~~ javascript
    function send_val() {
        let timep = $('#timep').val();
        let stn = $('#input_stn').val();
        $.ajax({
            type: 'POST',
            url: '/index',
            data: { timep: timep, stn: stn },
            // ajax가 정상적으로 동작하면 실행되는 부분
            success: function (result) {
            $('#init_img').css('display', 'none');
            $('#show_img').css('display', 'block');
            let dn = result.dn;
            let up = result.up;
            $('#i1').attr('src', '/static/img/stage_' + dn + '.png');
            $('#i2').attr('src', '/static/img/stage_' + up + '.png');
        }
      });
    }
               
~~~

~~~ python
# 전체 데이터와 일일 데이터 두 가지의 타입의 데이터를 구분해서 전처리 시작하는 함수
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
~~~

~~~ python
# 전체 데이터에 특정 조건의 열로 변경
# 다음 단계에서 일반적으로 사용하는 호선으로 다듬기 위해서 여기서 각 호선별로 분리
def line_sep_preproc_main():
    # 수인분당선에서 누락되는 역명들
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
                                                '12시-13시 승차인원','13시-14시 승차인원','14시-15시 승차인원','15시-16시 승차인원','16시-17시 승차인원']].sum(axis=1)
        frame['퇴근시간 승차인원'] = frame.loc[:,['17시-18시 승차인원','18시-19시 승차인원','19시-20시 승차인원']].sum(axis=1)
        frame['야간 승차인원'] = frame.loc[:,['20시-21시 승차인원','21시-22시 승차인원','22시-23시 승차인원',
                                            '23시-24시 승차인원','00시-01시 승차인원','01시-02시 승차인원']].sum(axis=1)
        frame['출근시간 하차인원'] = frame.loc[:,['06시-07시 하차인원','07시-08시 하차인원','08시-09시 하차인원']].sum(axis=1)
        frame['퇴근시간 하차인원'] = frame.loc[:,['17시-18시 하차인원','18시-19시 하차인원','19시-20시 하차인원']].sum(axis=1)
        frame['09-16시 하차인원'] = frame.loc[:,['09시-10시 하차인원','10시-11시 하차인원','11시-12시 하차인원',
                                                '12시-13시 하차인원','13시-14시 하차인원','14시-15시 하차인원','15시-16시 하차인원','16시-17시 하차인원']].sum(axis=1)
        frame['야간 하차인원'] = frame.loc[:,['20시-21시 하차인원','21시-22시 하차인원','22시-23시 하차인원',
                                            '23시-24시 하차인원','00시-01시 하차인원','01시-02시 하차인원']].sum(axis=1)
        frame['총 승차인원'] = frame.loc[:,['새벽 승차인원','출근시간 승차인원','09-16시 승차인원','퇴근시간 승차인원','야간 승차인원']].sum(axis=1)
        frame['총 하차인원'] = frame.loc[:,['새벽 하차인원','출근시간 하차인원','09-16시 하차인원','퇴근시간 하차인원','야간 하차인원']].sum(axis=1)
        frame = frame[['사용월', '호선명', '지하철역', '출근시간 승차인원', '출근시간 하차인원', 
                        '09-16시 승차인원', '09-16시 하차인원', '퇴근시간 승차인원', '퇴근시간 하차인원',
                        '새벽 승차인원','새벽 하차인원','야간 승차인원', '야간 하차인원','총 승차인원','총 하차인원']]
        # 2호선 신천역이 잠실새내역으로 바뀌고 새로운 신천역 생겨서 예전 자료에서의 2호선 신천역 잠실새내 역으로 변경
        frame.loc[(frame['호선명'] == '2호선') & (frame['지하철역'] == '신천'), '지하철역'] = '잠실새내'
        # 수인분당선에서 누락된 안산선의 역들 따로 추출
        frame_copy = frame[(frame['호선명']=='안산선')&(frame['지하철역'].isin(si_list))].copy()
        frame_copy['호선명'] = frame_copy['호선명'].apply(lambda x: '수인선_누락')
        frame_copy = frame_copy.reset_index(drop=True)
        copy_list.append(frame_copy)
        frame.to_csv(f'{temp_files_path}{line}.csv',index=False,encoding='utf-8')
    pd.concat(copy_list).to_csv(f'{temp_files_path}수인선_누락.csv',index=False,encoding='utf-8')
    return None
~~~

~~~ python
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
        ([f'{path}경춘선.csv'], '경춘선'),
        ([f'{path}수인선.csv',f'{path}수인선_누락.csv', f'{path}분당선.csv'], '수인분당선'),
        ([f'{path}경의선.csv', f'{path}중앙선.csv'], '경의중앙선'),
        ([f'{path}공항철도 1호선.csv'], '공항철도')
    ]
    # 19년도 이후 자료에는 9호선 2단계가 없음
    if year >= 2019:
        line_info.append(([f'{path}9호선.csv', f'{path}9호선2~3단계.csv'], '9호선'))
    else:
        line_info.append(([f'{path}9호선.csv', f'{path}9호선2단계.csv', f'{path}9호선2~3단계.csv'], '9호선'))
    return line_info

~~~

~~~ python
# rtn_line_info(year) 함수에서 만들어진 임시파일들을 일괄제거하는 함수
def rm_temp_files():
    temp_path = os.path.join('static','data', 'temp_files', '*.csv')
    for file in glob.glob(temp_path):
        os.remove(file)
    return None
~~~


<h5>참조</h5>

Link: [GoogleDriver][googledriverlink]

Link: [공공데이터포탈][datalink]


[googledriverlink]: https://google.com "Go google](https://drive.google.com/drive/folders/14KeS5I5Wr6hWilykOGmXlK5aB1wZ73js"

[datalink]: https://www.data.go.kr/
